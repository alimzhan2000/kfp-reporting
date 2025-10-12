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
            print(f"🔧 Processing file: {file_path}")
            upload_instance.status = 'processing'
            upload_instance.save()
            
            # Определяем тип файла и читаем данные
            if file_path.endswith('.csv'):
                print("📄 Reading CSV file...")
                df = cls._read_csv_with_quotes(file_path)
            elif file_path.endswith(('.xlsx', '.xls')):
                print("📊 Reading Excel file...")
                try:
                    df = cls._read_excel_with_header_detection(file_path)
                except Exception as e:
                    print(f"⚠️ Header detection failed, trying simple read: {e}")
                    # Fallback: попробуем простое чтение с разными строками заголовков
                    df = cls._read_excel_simple_fallback(file_path)
            else:
                raise ValueError('Неподдерживаемый формат файла')
            
            print(f"✅ File read successfully. Shape: {df.shape}")
            print(f"📋 Columns: {list(df.columns)}")
            
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
            print(f"❌ Error processing file: {str(e)}")
            import traceback
            traceback.print_exc()
            
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
        print(f"🔍 Detecting headers in Excel file: {file_path}")
        
        # Сначала читаем файл без заголовков, чтобы найти строку с заголовками
        df_raw = pd.read_excel(file_path, header=None)
        print(f"📊 Raw file shape: {df_raw.shape}")
        
        # Ищем строку, которая содержит все обязательные колонки
        header_row = None
        print(f"🔎 Searching for required columns: {cls.REQUIRED_COLUMNS}")
        
        for i in range(min(30, len(df_raw))):  # Увеличили до 30 строк
            row_values = [str(val) for val in df_raw.iloc[i].values if val is not None and str(val).strip()]
            # Проверяем, содержит ли строка все обязательные колонки
            if all(col in row_values for col in cls.REQUIRED_COLUMNS):
                header_row = i
                print(f"✅ Found headers in row {i}: {row_values}")
                break
            elif row_values:  # Логируем только непустые строки
                print(f"❌ Row {i}: {row_values[:5]}... (missing required columns)")
        
        if header_row is None:
            # Если не нашли строку с заголовками, пробуем стандартное чтение
            try:
                return pd.read_excel(file_path)
            except Exception as e:
                # Если стандартное чтение не работает, возвращаем ошибку
                raise ValueError(f'Не удалось найти заголовки в файле. Ошибка: {str(e)}')
        
        # Читаем файл с найденной строкой заголовков
        try:
            df = pd.read_excel(file_path, header=header_row)
            
            # Очищаем данные от пустых строк
            df = df.dropna(how='all')
            
            # Удаляем строки, где все значения NaN
            df = df.dropna(how='all')
            
            return df
        except Exception as e:
            raise ValueError(f'Ошибка при чтении Excel файла с заголовками в строке {header_row}: {str(e)}')
    
    @classmethod
    def _read_excel_simple_fallback(cls, file_path):
        """
        Простой fallback метод для чтения Excel файлов
        """
        print("🔄 Trying simple Excel reading fallback...")
        
        # Пробуем разные строки заголовков
        for header_row in [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]:
            try:
                print(f"📊 Trying header row {header_row}...")
                df = pd.read_excel(file_path, header=header_row)
                
                # Проверяем, есть ли нужные колонки
                if any(col in df.columns for col in cls.REQUIRED_COLUMNS):
                    print(f"✅ Success with header row {header_row}")
                    print(f"📋 Columns: {list(df.columns)}")
                    return df
                    
            except Exception as e:
                print(f"❌ Failed with header row {header_row}: {e}")
                continue
        
        # Если ничего не сработало, пробуем стандартное чтение
        print("🔄 Trying standard Excel reading...")
        try:
            df = pd.read_excel(file_path)
            print(f"✅ Standard reading successful")
            print(f"📋 Columns: {list(df.columns)}")
            return df
        except Exception as e:
            raise ValueError(f'Не удалось прочитать Excel файл: {str(e)}')
    
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
                # Безопасно преобразуем в строку и очищаем
                df.loc[:, col] = df[col].apply(lambda x: str(x).strip() if x is not None and str(x) != 'nan' else '')
        
        return df
    
    @classmethod
    def _save_to_database(cls, df, uploaded_by):
        """
        Сохранение данных в базу данных
        """
        records_created = 0
        records_updated = 0
        
        def safe_str(value):
            """Безопасное преобразование в строку"""
            if value is None or pd.isna(value):
                return ''
            return str(value).strip()
        
        def safe_float(value):
            """Безопасное преобразование в float"""
            try:
                if value is None or pd.isna(value):
                    return None
                return float(value)
            except (ValueError, TypeError):
                return None
        
        def safe_int(value):
            """Безопасное преобразование в int"""
            try:
                if value is None or pd.isna(value):
                    return None
                return int(float(value))  # Сначала в float, потом в int
            except (ValueError, TypeError):
                return None
        
        with transaction.atomic():
            for _, row in df.iterrows():
                try:
                    print(f"🔧 Processing row: {row.get('Поле', 'Unknown')} - {row.get('Год', 'Unknown')}")
                    
                    # Подготавливаем данные для сохранения с безопасными преобразованиями
                    defaults = {
                        'planting_area': safe_float(row['Площадь посева']),
                        'yield_per_hectare': safe_float(row['Урожайность, ц/га']),
                        'final_product': safe_str(row['Конечный продукт']),
                        'uploaded_by': uploaded_by,  # Может быть None
                    }
                    
                    # Добавляем дополнительные поля, если они есть в данных
                    if 'Бригада' in df.columns:
                        brigade_val = safe_str(row['Бригада'])
                        if brigade_val:
                            defaults['brigade'] = brigade_val
                    
                    if 'Поле (старое название)' in df.columns:
                        field_old_val = safe_str(row['Поле (старое название)'])
                        if field_old_val:
                            defaults['field_old_name'] = field_old_val
                    
                    if 'Валовый сбор, тн' in df.columns:
                        gross_val = safe_str(row['Валовый сбор, тн'])
                        if gross_val:
                            # Обрабатываем валовый сбор (может быть в формате "0 0" или числовом)
                            gross_harvest = gross_val.replace(' ', '').replace(',', '.')
                            if gross_harvest and gross_harvest != '00' and gross_harvest != '0':
                                float_val = safe_float(gross_harvest)
                                if float_val is not None:
                                    defaults['gross_harvest'] = float_val
                    
                    if 'Репродукция' in df.columns:
                        repro_val = safe_str(row['Репродукция'])
                        if repro_val:
                            defaults['reproduction'] = repro_val
                    
                    if 'Предшественник' in df.columns:
                        pred_val = safe_str(row['Предшественник'])
                        if pred_val:
                            defaults['predecessor'] = pred_val
                    
                    if 'Балл продуктивности' in df.columns:
                        score_val = safe_int(row['Балл продуктивности'])
                        if score_val is not None:
                            defaults['productivity_score'] = score_val
                    
                    if 'Агрофон' in df.columns:
                        agro_val = safe_str(row['Агрофон'])
                        if agro_val:
                            defaults['agro_background'] = agro_val
                    
                    if 'ПЗР' in df.columns:
                        pzr_val = safe_str(row['ПЗР'])
                        if pzr_val:
                            defaults['pzr'] = pzr_val
                    
                    # Сохраняем культуру, если она присутствует, но не используем её как ключ
                    if 'Культура' in df.columns:
                        crop_val = safe_str(row['Культура'])
                        defaults['crop'] = crop_val
                    else:
                        defaults['crop'] = ''

                    # Безопасные ключи для поиска/создания записи
                    field_name = safe_str(row['Поле'])
                    year = safe_int(row['Год'])
                    final_product = safe_str(row['Конечный продукт'])
                    variety = safe_str(row['Сорт'])
                    
                    if not field_name or not year or not final_product or not variety:
                        print(f"⚠️ Skipping row with missing required fields: field={field_name}, year={year}, product={final_product}, variety={variety}")
                        continue

                    print(f"💾 Saving: {field_name}, {year}, {final_product}, {variety}")
                    
                    data, created = AgriculturalData.objects.update_or_create(
                        field_name=field_name,
                        year=year,
                        final_product=final_product,
                        variety=variety,
                        defaults=defaults
                    )
                    
                    if created:
                        records_created += 1
                        print(f"✅ Created record #{records_created}")
                    else:
                        records_updated += 1
                        print(f"🔄 Updated record #{records_updated}")
                        
                except Exception as e:
                    print(f"❌ Error processing row: {e}")
                    import traceback
                    traceback.print_exc()
                    continue
        
        print(f"📊 Summary: {records_created} created, {records_updated} updated")
        return records_created, records_updated

