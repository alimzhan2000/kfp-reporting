import os
import csv
import pandas as pd  # Восстановлено
from django.core.files.storage import default_storage
from django.utils import timezone
from django.db import transaction
from .models import DataUpload
from reports.models import AgriculturalData


class DataProcessingService:
    """
    Сервис для обработки загруженных файлов
    """
    
    REQUIRED_COLUMNS = [
        'Поле', 'Год', 'Площадь посева', 'Урожайность, ц/га', 
        'Сорт', 'Конечный продукт'
    ]
    
    # Дополнительные колонки из реального файла
    OPTIONAL_COLUMNS = [
        'Бригада', 'Поле (старое название)', 'Валовый сбор, тн',
        'Репродукция', 'Предшественник', 'Балл продуктивности',
        'Агрофон', 'ПЗР'
    ]
    
    @classmethod
    def process_file(cls, upload_instance, file_path):
        """
        Обработка загруженного файла
        """
        try:
            upload_instance.status = 'processing'
            upload_instance.save()
            
            # Определяем тип файла и читаем данные
            if file_path.endswith('.csv'):
                df = cls._read_csv_with_quotes(file_path)
            elif file_path.endswith(('.xlsx', '.xls')):
                df = cls._read_excel_with_header_detection(file_path)
            else:
                raise ValueError('Неподдерживаемый формат файла')
            
            # Проверяем наличие необходимых колонок
            missing_columns = [col for col in cls.REQUIRED_COLUMNS if col not in df.columns]
            if missing_columns:
                raise ValueError(f'Отсутствуют обязательные колонки: {", ".join(missing_columns)}')
            
            # Очищаем данные только по критически важным колонкам
            required_for_validation = ['Поле', 'Год', 'Площадь посева', 'Урожайность, ц/га', 'Конечный продукт']
            present = [c for c in required_for_validation if c in df.columns]
            df = df.dropna(subset=present)
            # Не сужаем до обязательных колонок, чтобы сохранить доп. поля
            
            # Нормализуем данные
            df = cls._normalize_data(df)
            
            # Сохраняем данные в базу
            records_created, records_updated = cls._save_to_database(df, None)
            
            # Обновляем статистику
            upload_instance.records_processed = len(df)
            upload_instance.records_created = records_created
            upload_instance.records_updated = records_updated
            upload_instance.status = 'completed'
            upload_instance.completed_at = timezone.now()
            upload_instance.save()
            
            return True, f'Обработано {len(df)} записей'
            
        except Exception as e:
            upload_instance.status = 'failed'
            upload_instance.error_message = str(e)
            upload_instance.completed_at = timezone.now()
            upload_instance.save()
            return False, str(e)
    
    @classmethod
    def _read_csv_with_quotes(cls, file_path):
        """
        Читает CSV файл, автоматически добавляя кавычки к колонкам с запятыми
        """
        import tempfile
        import os
        import re
        
        # Читаем первую строку для определения заголовков
        with open(file_path, 'r', encoding='utf-8') as f:
            first_line = f.readline().strip()
        
        # Проверяем, есть ли колонки с запятыми без кавычек
        columns_with_commas = [col for col in cls.REQUIRED_COLUMNS if ',' in col]
        
        if columns_with_commas:
            # Создаем временный файл с исправленными заголовками
            temp_file = tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.csv', encoding='utf-8')
            
            try:
                # Используем регулярное выражение для поиска и замены колонок с запятыми
                # Ищем паттерн: начало строки или запятая, затем название колонки с запятой, затем запятая или конец строки
                for col in columns_with_commas:
                    # Экранируем специальные символы в названии колонки
                    escaped_col = re.escape(col)
                    # Заменяем колонку на версию в кавычках
                    pattern = r'(^|,)' + escaped_col + r'(,|$)'
                    replacement = r'\1"' + col + r'"\2'
                    first_line = re.sub(pattern, replacement, first_line)
                
                # Записываем исправленную первую строку
                temp_file.write(first_line + '\n')
                
                # Копируем остальные строки
                with open(file_path, 'r', encoding='utf-8') as original_file:
                    original_file.readline()  # Пропускаем первую строку
                    for line in original_file:
                        temp_file.write(line)
                
                temp_file.close()
                
                # Читаем исправленный файл
                df = pd.read_csv(temp_file.name, encoding='utf-8')
                
                # Удаляем временный файл
                os.unlink(temp_file.name)
                
                return df
                
            except Exception:
                # В случае ошибки удаляем временный файл и читаем оригинальный
                if os.path.exists(temp_file.name):
                    os.unlink(temp_file.name)
                return pd.read_csv(file_path, encoding='utf-8')
        else:
            # Если нет колонок с запятыми, читаем как обычно
            return pd.read_csv(file_path, encoding='utf-8')
    
    @classmethod
    def _read_excel_with_header_detection(cls, file_path):
        """
        Читает Excel файл с автоматическим определением строки заголовков
        """
        # Сначала читаем файл без заголовков, чтобы найти строку с заголовками
        df_raw = pd.read_excel(file_path, header=None)
        
        # Ищем строку, которая содержит все обязательные колонки
        header_row = None
        for i in range(min(20, len(df_raw))):  # Проверяем первые 20 строк
            row_values = [str(val) for val in df_raw.iloc[i].values if val is not None and str(val).strip()]
            # Проверяем, содержит ли строка все обязательные колонки
            if all(col in row_values for col in cls.REQUIRED_COLUMNS):
                header_row = i
                break
        
        if header_row is None:
            # Если не нашли строку с заголовками, пробуем стандартное чтение
            return pd.read_excel(file_path)
        
        # Читаем файл с найденной строкой заголовков
        df = pd.read_excel(file_path, header=header_row)
        
        # Очищаем данные от пустых строк
        df = df.dropna(how='all')
        
        
        return df
    
    @classmethod
    def _normalize_data(cls, df):
        """
        Нормализация данных
        """
        # Приводим к нужным типам данных
        df['Год'] = pd.to_numeric(df['Год'], errors='coerce')
        df['Площадь посева'] = pd.to_numeric(df['Площадь посева'], errors='coerce')
        df['Урожайность, ц/га'] = pd.to_numeric(df['Урожайность, ц/га'], errors='coerce')
        
        # Не удаляем строки целиком: дальнейшая фильтрация выполняется по обязательным полям
        
        # Очищаем текстовые поля
        text_columns = ['Поле', 'Культура', 'Сорт', 'Конечный продукт']
        for col in text_columns:
            if col in df.columns:
                df.loc[:, col] = df[col].astype(str).str.strip()
        
        return df
    
    @classmethod
    def _save_to_database(cls, df, uploaded_by):
        """
        Сохранение данных в базу данных
        """
        records_created = 0
        records_updated = 0
        
        with transaction.atomic():
            for _, row in df.iterrows():
                # Подготавливаем данные для сохранения
                defaults = {
                    'planting_area': float(row['Площадь посева']),
                    'yield_per_hectare': float(row['Урожайность, ц/га']),
                    'final_product': row['Конечный продукт'],
                    'uploaded_by': uploaded_by,  # Может быть None
                }
                
                # Добавляем дополнительные поля, если они есть в данных
                # import pandas as pd  # Временно отключено
                
                if 'Бригада' in df.columns and row['Бригада'] and row['Бригада'].strip():
                    defaults['brigade'] = str(row['Бригада'])
                
                if 'Поле (старое название)' in df.columns and row['Поле (старое название)'] and row['Поле (старое название)'].strip():
                    defaults['field_old_name'] = str(row['Поле (старое название)'])
                
                if 'Валовый сбор, тн' in df.columns and row['Валовый сбор, тн'] and row['Валовый сбор, тн'].strip():
                    # Обрабатываем валовый сбор (может быть в формате "0 0" или числовом)
                    gross_harvest = str(row['Валовый сбор, тн']).replace(' ', '').replace(',', '.')
                    if gross_harvest and gross_harvest != '00' and gross_harvest != '0':
                        try:
                            defaults['gross_harvest'] = float(gross_harvest)
                        except (ValueError, TypeError):
                            pass
                
                if 'Репродукция' in df.columns and row['Репродукция'] and row['Репродукция'].strip():
                    defaults['reproduction'] = str(row['Репродукция'])
                
                if 'Предшественник' in df.columns and row['Предшественник'] and row['Предшественник'].strip():
                    defaults['predecessor'] = str(row['Предшественник'])
                
                if 'Балл продуктивности' in df.columns and row['Балл продуктивности'] and row['Балл продуктивности'].strip():
                    try:
                        defaults['productivity_score'] = int(row['Балл продуктивности'])
                    except (ValueError, TypeError):
                        pass
                
                if 'Агрофон' in df.columns and row['Агрофон'] and row['Агрофон'].strip():
                    defaults['agro_background'] = str(row['Агрофон'])
                
                if 'ПЗР' in df.columns and row['ПЗР'] and row['ПЗР'].strip():
                    defaults['pzr'] = str(row['ПЗР'])
                
                # Сохраняем культуру, если она присутствует, но не используем её как ключ
                if 'Культура' in df.columns and row['Культура'] and row['Культура'].strip():
                    defaults['crop'] = str(row['Культура'])
                else:
                    defaults['crop'] = ''

                data, created = AgriculturalData.objects.update_or_create(
                    field_name=row['Поле'],
                    year=int(row['Год']),
                    final_product=row['Конечный продукт'],
                    variety=row['Сорт'],
                    defaults=defaults
                )
                
                if created:
                    records_created += 1
                else:
                    records_updated += 1
        
        return records_created, records_updated

