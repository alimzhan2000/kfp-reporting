#!/usr/bin/env python
"""
Тест для изоляции проблемы с pandas
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

@method_decorator(csrf_exempt, name='dispatch')
class PandasIsolationTestView(APIView):
    """
    Тест для изоляции проблемы с pandas
    """
    parser_classes = (MultiPartParser, FormParser)
    permission_classes = []  # Без аутентификации
    
    def post(self, request, format=None):
        """
        Изолированное тестирование pandas
        """
        if 'file' not in request.FILES:
            return Response(
                {'error': 'Файл не найден'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        uploaded_file = request.FILES['file']
        
        try:
            print(f"🧪 Pandas isolation test for file: {uploaded_file.name}")
            
            result = {
                'file_name': uploaded_file.name,
                'file_size': uploaded_file.size,
                'file_extension': os.path.splitext(uploaded_file.name)[1],
                'tests': {}
            }
            
            # Сохраняем файл
            file_path = default_storage.save(
                f'pandas_test_{uploaded_file.name}',
                ContentFile(uploaded_file.read())
            )
            full_file_path = default_storage.path(file_path)
            
            # Тест 1: Импорт pandas
            try:
                print("🔍 Test 1: Pandas import...")
                import pandas as pd
                result['tests']['pandas_import'] = {
                    'success': True,
                    'pandas_version': pd.__version__
                }
                print(f"✅ Pandas imported: {pd.__version__}")
            except Exception as e:
                result['tests']['pandas_import'] = {
                    'success': False,
                    'error': str(e)
                }
                print(f"❌ Pandas import failed: {e}")
                return Response(result, status=status.HTTP_200_OK)
            
            # Тест 2: Импорт openpyxl
            try:
                print("🔍 Test 2: Openpyxl import...")
                import openpyxl
                result['tests']['openpyxl_import'] = {
                    'success': True,
                    'openpyxl_version': openpyxl.__version__
                }
                print(f"✅ Openpyxl imported: {openpyxl.__version__}")
            except Exception as e:
                result['tests']['openpyxl_import'] = {
                    'success': False,
                    'error': str(e)
                }
                print(f"❌ Openpyxl import failed: {e}")
            
            # Тест 3: Простое чтение Excel без параметров
            try:
                print("🔍 Test 3: Simple Excel read...")
                df = pd.read_excel(full_file_path)
                result['tests']['simple_excel_read'] = {
                    'success': True,
                    'shape': df.shape,
                    'columns': list(df.columns)[:10]  # Первые 10 колонок
                }
                print(f"✅ Simple Excel read: {df.shape}")
            except Exception as e:
                result['tests']['simple_excel_read'] = {
                    'success': False,
                    'error': str(e)
                }
                print(f"❌ Simple Excel read failed: {e}")
            
            # Тест 4: Чтение с указанием engine
            try:
                print("🔍 Test 4: Excel read with engine...")
                df = pd.read_excel(full_file_path, engine='openpyxl')
                result['tests']['excel_with_engine'] = {
                    'success': True,
                    'shape': df.shape,
                    'columns': list(df.columns)[:10]
                }
                print(f"✅ Excel with engine: {df.shape}")
            except Exception as e:
                result['tests']['excel_with_engine'] = {
                    'success': False,
                    'error': str(e)
                }
                print(f"❌ Excel with engine failed: {e}")
            
            # Тест 5: Чтение без заголовков
            try:
                print("🔍 Test 5: Excel read without headers...")
                df = pd.read_excel(full_file_path, header=None, nrows=5)
                result['tests']['excel_no_headers'] = {
                    'success': True,
                    'shape': df.shape,
                    'first_row': df.iloc[0].tolist() if len(df) > 0 else []
                }
                print(f"✅ Excel no headers: {df.shape}")
            except Exception as e:
                result['tests']['excel_no_headers'] = {
                    'success': False,
                    'error': str(e)
                }
                print(f"❌ Excel no headers failed: {e}")
            
            # Тест 6: Поиск заголовков вручную
            try:
                print("🔍 Test 6: Manual header search...")
                # Читаем первые 20 строк без заголовков
                df_raw = pd.read_excel(full_file_path, header=None, nrows=20)
                
                # Ищем строку с русскими заголовками
                REQUIRED_COLUMNS = ['Поле', 'Год', 'Площадь посева', 'Урожайность, ц/га', 'Сорт', 'Конечный продукт']
                header_row = None
                
                for i in range(len(df_raw)):
                    row_values = [str(val) for val in df_raw.iloc[i].values if pd.notna(val)]
                    if any(col in row_values for col in REQUIRED_COLUMNS):
                        header_row = i
                        break
                
                if header_row is not None:
                    # Читаем с найденным заголовком
                    df_with_headers = pd.read_excel(full_file_path, header=header_row, nrows=5)
                    result['tests']['manual_header_search'] = {
                        'success': True,
                        'header_row': header_row,
                        'shape': df_with_headers.shape,
                        'columns': list(df_with_headers.columns)[:10]
                    }
                    print(f"✅ Manual header search: found at row {header_row}")
                else:
                    result['tests']['manual_header_search'] = {
                        'success': False,
                        'error': 'Required columns not found in first 20 rows'
                    }
                    print("❌ Manual header search: required columns not found")
                    
            except Exception as e:
                result['tests']['manual_header_search'] = {
                    'success': False,
                    'error': str(e)
                }
                print(f"❌ Manual header search failed: {e}")
            
            # Тест 7: Попробуем обработать данные как в оригинальном коде
            try:
                print("🔍 Test 7: Original code simulation...")
                if result['tests'].get('manual_header_search', {}).get('success'):
                    header_row = result['tests']['manual_header_search']['header_row']
                    df = pd.read_excel(full_file_path, header=header_row)
                    
                    # Симулируем оригинальную обработку
                    df_clean = df.dropna(how='all')
                    
                    # Проверяем обязательные колонки
                    required_cols = ['Поле', 'Год', 'Площадь посева', 'Урожайность, ц/га', 'Сорт', 'Конечный продукт']
                    missing_cols = [col for col in required_cols if col not in df_clean.columns]
                    
                    if not missing_cols:
                        # Пробуем нормализацию данных
                        df_clean['Год'] = pd.to_numeric(df_clean['Год'], errors='coerce')
                        df_clean['Площадь посева'] = pd.to_numeric(df_clean['Площадь посева'], errors='coerce')
                        df_clean['Урожайность, ц/га'] = pd.to_numeric(df_clean['Урожайность, ц/га'], errors='coerce')
                        
                        # Очищаем текстовые поля
                        text_columns = ['Поле', 'Культура', 'Сорт', 'Конечный продукт']
                        for col in text_columns:
                            if col in df_clean.columns:
                                df_clean[col] = df_clean[col].apply(lambda x: str(x).strip() if x is not None and str(x) != 'nan' else '')
                        
                        result['tests']['original_code_simulation'] = {
                            'success': True,
                            'shape_after_processing': df_clean.shape,
                            'first_row_processed': df_clean.iloc[0].to_dict() if len(df_clean) > 0 else {}
                        }
                        print(f"✅ Original code simulation: {df_clean.shape}")
                    else:
                        result['tests']['original_code_simulation'] = {
                            'success': False,
                            'error': f'Missing columns: {missing_cols}'
                        }
                        print(f"❌ Original code simulation: missing columns {missing_cols}")
                        
            except Exception as e:
                result['tests']['original_code_simulation'] = {
                    'success': False,
                    'error': str(e)
                }
                print(f"❌ Original code simulation failed: {e}")
            
            # Удаляем временный файл
            try:
                default_storage.delete(file_path)
            except:
                pass
            
            return Response(result, status=status.HTTP_200_OK)
            
        except Exception as e:
            print(f"❌ Pandas isolation test failed: {e}")
            import traceback
            traceback.print_exc()
            return Response(
                {'error': f'Тест изоляции pandas не удался: {str(e)}'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
