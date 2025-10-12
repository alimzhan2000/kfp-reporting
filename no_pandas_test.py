#!/usr/bin/env python
"""
Тест без pandas для диагностики
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
import zipfile
import xml.etree.ElementTree as ET

@method_decorator(csrf_exempt, name='dispatch')
class NoPandasTestView(APIView):
    """
    Тест без pandas - только базовые операции
    """
    parser_classes = (MultiPartParser, FormParser)
    permission_classes = []  # Без аутентификации
    
    def post(self, request, format=None):
        """
        Тестирование файла без pandas
        """
        if 'file' not in request.FILES:
            return Response(
                {'error': 'Файл не найден'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        uploaded_file = request.FILES['file']
        
        try:
            print(f"🧪 No-pandas test for file: {uploaded_file.name}")
            
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
                    f'no_pandas_test_{uploaded_file.name}',
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
            
            # Тест 3: Проверка что это ZIP файл (xlsx это ZIP)
            if result['tests'].get('file_existence', {}).get('success'):
                try:
                    print("🔍 Test 3: ZIP file check...")
                    is_zip = zipfile.is_zipfile(full_file_path)
                    
                    if is_zip:
                        with zipfile.ZipFile(full_file_path, 'r') as zip_file:
                            file_list = zip_file.namelist()
                        
                        result['tests']['zip_check'] = {
                            'success': True,
                            'is_zip': is_zip,
                            'files_in_zip': file_list[:10]  # Первые 10 файлов
                        }
                    else:
                        result['tests']['zip_check'] = {
                            'success': False,
                            'is_zip': is_zip,
                            'error': 'File is not a valid ZIP file'
                        }
                    
                    print(f"✅ ZIP check: is_zip={is_zip}")
                except Exception as e:
                    result['tests']['zip_check'] = {
                        'success': False,
                        'error': str(e)
                    }
                    print(f"❌ ZIP check failed: {e}")
            
            # Тест 4: Чтение sharedStrings.xml (если есть)
            if result['tests'].get('zip_check', {}).get('success') and result['tests']['zip_check']['is_zip']:
                try:
                    print("🔍 Test 4: Reading shared strings...")
                    with zipfile.ZipFile(full_file_path, 'r') as zip_file:
                        if 'xl/sharedStrings.xml' in zip_file.namelist():
                            shared_strings_xml = zip_file.read('xl/sharedStrings.xml').decode('utf-8')
                            root = ET.fromstring(shared_strings_xml)
                            
                            # Найдем первые несколько строк
                            strings = []
                            for si in root.findall('.//{http://schemas.openxmlformats.org/spreadsheetml/2006/main}si')[:5]:
                                text_elements = si.findall('.//{http://schemas.openxmlformats.org/spreadsheetml/2006/main}t')
                                if text_elements:
                                    text = ''.join([elem.text or '' for elem in text_elements])
                                    strings.append(text[:50])  # Первые 50 символов
                            
                            result['tests']['shared_strings'] = {
                                'success': True,
                                'found_strings': len(strings),
                                'sample_strings': strings
                            }
                        else:
                            result['tests']['shared_strings'] = {
                                'success': False,
                                'error': 'sharedStrings.xml not found'
                            }
                    
                    print(f"✅ Shared strings read successfully")
                except Exception as e:
                    result['tests']['shared_strings'] = {
                        'success': False,
                        'error': str(e)
                    }
                    print(f"❌ Shared strings read failed: {e}")
            
            # Тест 5: Попробуем pandas с разными engine
            try:
                print("🔍 Test 5: Pandas with different engines...")
                import pandas as pd
                
                # Пробуем разные engines
                engines = ['openpyxl', 'xlrd', None]
                pandas_results = {}
                
                for engine in engines:
                    try:
                        print(f"  Trying engine: {engine}")
                        if engine:
                            df = pd.read_excel(full_file_path, engine=engine, header=None, nrows=3)
                        else:
                            df = pd.read_excel(full_file_path, header=None, nrows=3)
                        
                        pandas_results[f'engine_{engine or "default"}'] = {
                            'success': True,
                            'shape': df.shape,
                            'sample_data': df.head(2).to_dict('records')
                        }
                        print(f"  ✅ Engine {engine} worked")
                        break  # Если один engine работает, останавливаемся
                        
                    except Exception as e:
                        pandas_results[f'engine_{engine or "default"}'] = {
                            'success': False,
                            'error': str(e)
                        }
                        print(f"  ❌ Engine {engine} failed: {e}")
                
                result['tests']['pandas_engines'] = pandas_results
                
            except Exception as e:
                result['tests']['pandas_engines'] = {
                    'error': f'Pandas test failed completely: {str(e)}'
                }
                print(f"❌ Pandas test failed completely: {e}")
            
            # Удаляем временный файл
            try:
                if 'file_path' in locals():
                    default_storage.delete(file_path)
            except:
                pass
            
            return Response(result, status=status.HTTP_200_OK)
            
        except Exception as e:
            print(f"❌ No-pandas test failed: {e}")
            import traceback
            traceback.print_exc()
            return Response(
                {'error': f'Тест без pandas не удался: {str(e)}'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
