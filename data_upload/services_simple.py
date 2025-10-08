import os
import csv
from django.core.files.storage import default_storage
from django.utils import timezone
from django.db import transaction
from .models import DataUpload
from reports.models import AgriculturalData


class DataProcessingService:
    """
    Упрощенный сервис для обработки загруженных файлов без pandas
    """
    
    REQUIRED_COLUMNS = [
        'Поле', 'Год', 'Площадь посева', 'Урожайность, ц/га', 
        'Сорт', 'Конечный продукт'
    ]
    
    @classmethod
    def process_file(cls, upload_instance, file_path):
        """
        Обработка загруженного файла
        """
        try:
            upload_instance.status = 'processing'
            upload_instance.save()
            
            # Читаем данные из файла
            if file_path.endswith('.csv'):
                data = cls._read_csv(file_path)
            elif file_path.endswith(('.xlsx', '.xls')):
                # Для Excel файлов пока возвращаем ошибку
                raise ValueError('Excel файлы временно не поддерживаются без pandas')
            else:
                raise ValueError('Неподдерживаемый формат файла')
            
            # Проверяем наличие необходимых колонок
            if not data:
                raise ValueError('Файл пуст или не содержит данных')
            
            headers = data[0].keys()
            missing_columns = [col for col in cls.REQUIRED_COLUMNS if col not in headers]
            if missing_columns:
                raise ValueError(f'Отсутствуют обязательные колонки: {", ".join(missing_columns)}')
            
            # Сохраняем данные в базу
            records_created, records_updated = cls._save_to_database(data, upload_instance.uploaded_by)
            
            # Обновляем статистику
            upload_instance.records_processed = len(data)
            upload_instance.records_created = records_created
            upload_instance.records_updated = records_updated
            upload_instance.status = 'completed'
            upload_instance.completed_at = timezone.now()
            upload_instance.save()
            
            return True, f'Обработано {len(data)} записей'
            
        except Exception as e:
            upload_instance.status = 'failed'
            upload_instance.error_message = str(e)
            upload_instance.completed_at = timezone.now()
            upload_instance.save()
            return False, str(e)
    
    @classmethod
    def _read_csv(cls, file_path):
        """
        Читает CSV файл и возвращает список словарей
        """
        data = []
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    # Очищаем пустые значения
                    cleaned_row = {k: v.strip() if v else '' for k, v in row.items()}
                    data.append(cleaned_row)
        except Exception as e:
            raise ValueError(f'Ошибка чтения CSV файла: {e}')
        
        return data
    
    @classmethod
    def _save_to_database(cls, data, uploaded_by):
        """
        Сохранение данных в базу данных
        """
        records_created = 0
        records_updated = 0
        
        with transaction.atomic():
            for row in data:
                try:
                    # Подготавливаем данные для сохранения
                    defaults = {
                        'planting_area': float(row['Площадь посева']),
                        'yield_per_hectare': float(row['Урожайность, ц/га']),
                        'final_product': row['Конечный продукт'],
                        'uploaded_by': uploaded_by,
                        'crop': row.get('Культура', ''),
                    }
                    
                    data_obj, created = AgriculturalData.objects.update_or_create(
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
                        
                except (ValueError, TypeError) as e:
                    # Пропускаем строки с некорректными данными
                    continue
        
        return records_created, records_updated
