#!/usr/bin/env python
"""
Простой тест для диагностики файлов
"""
import os
import django
from django.conf import settings

# Настраиваем Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'kfp_reporting.settings')
django.setup()

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework import status
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
import pandas as pd

@method_decorator(csrf_exempt, name='dispatch')
class SimpleFileTestView(APIView):
    """
    Простой тестовый endpoint для диагностики файлов
    """
    parser_classes = (MultiPartParser, FormParser)
    permission_classes = []  # Без аутентификации
    
    def post(self, request, format=None):
        """
        Простое тестирование чтения файла
        """
        if 'file' not in request.FILES:
            return Response(
                {'error': 'Файл не найден'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        uploaded_file = request.FILES['file']
        
        try:
            print(f"🧪 Testing file: {uploaded_file.name}")
            
            # Сохраняем файл временно
            file_path = default_storage.save(
                f'temp_test_{uploaded_file.name}',
                ContentFile(uploaded_file.read())
            )
            
            full_file_path = default_storage.path(file_path)
            print(f"📁 File saved to: {full_file_path}")
            
            result = {
                'file_name': uploaded_file.name,
                'file_size': uploaded_file.size,
                'file_path': file_path,
                'tests': {}
            }
            
            # Тест 1: Простое чтение Excel
            try:
                print("🔍 Test 1: Simple Excel reading...")
                df_raw = pd.read_excel(full_file_path, header=None)
                result['tests']['simple_excel'] = {
                    'success': True,
                    'shape': df_raw.shape,
                    'first_5_rows': df_raw.head().to_dict()
                }
                print(f"✅ Simple Excel read: {df_raw.shape}")
            except Exception as e:
                result['tests']['simple_excel'] = {
                    'success': False,
                    'error': str(e)
                }
                print(f"❌ Simple Excel read failed: {e}")
            
            # Тест 2: Поиск заголовков
            try:
                print("🔍 Test 2: Header detection...")
                REQUIRED_COLUMNS = ['Поле', 'Год', 'Площадь посева', 'Урожайность, ц/га', 'Сорт', 'Конечный продукт']
                
                header_found = False
                for i in range(min(30, len(df_raw))):
                    row_values = [str(val) for val in df_raw.iloc[i].values if val is not None and str(val).strip()]
                    if all(col in row_values for col in REQUIRED_COLUMNS):
                        result['tests']['header_detection'] = {
                            'success': True,
                            'header_row': i,
                            'columns_found': row_values
                        }
                        header_found = True
                        break
                
                if not header_found:
                    result['tests']['header_detection'] = {
                        'success': False,
                        'error': 'Required columns not found in first 30 rows'
                    }
                    
            except Exception as e:
                result['tests']['header_detection'] = {
                    'success': False,
                    'error': str(e)
                }
                print(f"❌ Header detection failed: {e}")
            
            # Тест 3: Чтение с найденными заголовками
            if result['tests'].get('header_detection', {}).get('success'):
                try:
                    print("🔍 Test 3: Reading with headers...")
                    header_row = result['tests']['header_detection']['header_row']
                    df = pd.read_excel(full_file_path, header=header_row)
                    result['tests']['header_reading'] = {
                        'success': True,
                        'shape': df.shape,
                        'columns': list(df.columns),
                        'first_row': df.iloc[0].to_dict() if len(df) > 0 else {}
                    }
                    print(f"✅ Header reading: {df.shape}")
                except Exception as e:
                    result['tests']['header_reading'] = {
                        'success': False,
                        'error': str(e)
                    }
                    print(f"❌ Header reading failed: {e}")
            
            # Удаляем временный файл
            try:
                default_storage.delete(file_path)
            except:
                pass
            
            return Response(result, status=status.HTTP_200_OK)
            
        except Exception as e:
            print(f"❌ Simple test failed: {e}")
            import traceback
            traceback.print_exc()
            return Response(
                {'error': f'Простой тест не удался: {str(e)}'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
