#!/usr/bin/env python
"""
Ультра простой тест для диагностики файлов
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
class UltraSimpleTestView(APIView):
    """
    Ультра простой тест - только чтение файла без pandas
    """
    parser_classes = (MultiPartParser, FormParser)
    permission_classes = []  # Без аутентификации
    
    def post(self, request, format=None):
        """
        Ультра простое тестирование файла
        """
        if 'file' not in request.FILES:
            return Response(
                {'error': 'Файл не найден'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        uploaded_file = request.FILES['file']
        
        try:
            print(f"🧪 Ultra simple test for file: {uploaded_file.name}")
            
            result = {
                'file_name': uploaded_file.name,
                'file_size': uploaded_file.size,
                'file_extension': os.path.splitext(uploaded_file.name)[1],
                'tests': {}
            }
            
            # Тест 1: Простое сохранение файла
            try:
                print("🔍 Test 1: Simple file saving...")
                file_path = default_storage.save(
                    f'ultra_test_{uploaded_file.name}',
                    ContentFile(uploaded_file.read())
                )
                result['tests']['file_saving'] = {
                    'success': True,
                    'file_path': file_path
                }
                print(f"✅ File saved: {file_path}")
            except Exception as e:
                result['tests']['file_saving'] = {
                    'success': False,
                    'error': str(e)
                }
                print(f"❌ File saving failed: {e}")
            
            # Тест 2: Проверка существования файла
            if result['tests'].get('file_saving', {}).get('success'):
                try:
                    print("🔍 Test 2: File existence check...")
                    full_file_path = default_storage.path(file_path)
                    file_exists = os.path.exists(full_file_path)
                    file_size = os.path.getsize(full_file_path) if file_exists else 0
                    
                    result['tests']['file_existence'] = {
                        'success': True,
                        'file_exists': file_exists,
                        'full_path': full_file_path,
                        'file_size': file_size
                    }
                    print(f"✅ File check: exists={file_exists}, size={file_size}")
                except Exception as e:
                    result['tests']['file_existence'] = {
                        'success': False,
                        'error': str(e)
                    }
                    print(f"❌ File existence check failed: {e}")
            
            # Тест 3: Простое чтение с pandas (без обработки)
            if result['tests'].get('file_existence', {}).get('success'):
                try:
                    print("🔍 Test 3: Basic pandas reading...")
                    import pandas as pd
                    
                    # Читаем только первые 5 строк без заголовков
                    df = pd.read_excel(full_file_path, header=None, nrows=5)
                    
                    result['tests']['basic_pandas'] = {
                        'success': True,
                        'shape': df.shape,
                        'first_5_rows': df.to_dict('records')
                    }
                    print(f"✅ Basic pandas read: {df.shape}")
                except Exception as e:
                    result['tests']['basic_pandas'] = {
                        'success': False,
                        'error': str(e)
                    }
                    print(f"❌ Basic pandas read failed: {e}")
            
            # Тест 4: Поиск строк с русскими заголовками
            if result['tests'].get('basic_pandas', {}).get('success'):
                try:
                    print("🔍 Test 4: Russian header search...")
                    # Читаем первые 10 строк
                    df_headers = pd.read_excel(full_file_path, header=None, nrows=10)
                    
                    russian_headers = []
                    for i, row in df_headers.iterrows():
                        row_text = ' '.join([str(cell) for cell in row.values if pd.notna(cell)])
                        # Проверяем наличие русских букв
                        if any('\u0400' <= char <= '\u04FF' for char in row_text):
                            russian_headers.append({
                                'row': i,
                                'content': row_text[:100]  # Первые 100 символов
                            })
                    
                    result['tests']['russian_headers'] = {
                        'success': True,
                        'found_rows': len(russian_headers),
                        'rows_with_russian': russian_headers
                    }
                    print(f"✅ Russian headers found: {len(russian_headers)}")
                except Exception as e:
                    result['tests']['russian_headers'] = {
                        'success': False,
                        'error': str(e)
                    }
                    print(f"❌ Russian header search failed: {e}")
            
            # Удаляем временный файл
            try:
                if 'file_path' in locals():
                    default_storage.delete(file_path)
            except:
                pass
            
            return Response(result, status=status.HTTP_200_OK)
            
        except Exception as e:
            print(f"❌ Ultra simple test failed: {e}")
            import traceback
            traceback.print_exc()
            return Response(
                {'error': f'Ультра простой тест не удался: {str(e)}'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
