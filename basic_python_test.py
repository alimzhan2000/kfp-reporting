#!/usr/bin/env python
"""
Тест только с базовыми Python библиотеками
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
import json

@method_decorator(csrf_exempt, name='dispatch')
class BasicPythonTestView(APIView):
    """
    Тест только с базовыми Python библиотеками
    """
    parser_classes = (MultiPartParser, FormParser)
    permission_classes = []  # Без аутентификации
    
    def post(self, request, format=None):
        """
        Тестирование файла только с базовыми Python библиотеками
        """
        if 'file' not in request.FILES:
            return Response(
                {'error': 'Файл не найден'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        uploaded_file = request.FILES['file']
        
        try:
            print(f"🧪 Basic Python test for file: {uploaded_file.name}")
            
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
                    f'basic_test_{uploaded_file.name}',
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
                return Response(result, status=status.HTTP_200_OK)
            
            # Тест 2: Проверка существования файла
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
                return Response(result, status=status.HTTP_200_OK)
            
            # Тест 3: Проверка что это ZIP файл
            try:
                print("🔍 Test 3: ZIP file check...")
                is_zip = zipfile.is_zipfile(full_file_path)
                
                if is_zip:
                    with zipfile.ZipFile(full_file_path, 'r') as zip_file:
                        file_list = zip_file.namelist()
                    
                    result['tests']['zip_check'] = {
                        'success': True,
                        'is_zip': is_zip,
                        'files_in_zip': file_list[:20]  # Первые 20 файлов
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
                return Response(result, status=status.HTTP_200_OK)
            
            # Тест 4: Чтение sharedStrings.xml
            if result['tests'].get('zip_check', {}).get('success') and result['tests']['zip_check']['is_zip']:
                try:
                    print("🔍 Test 4: Reading shared strings...")
                    with zipfile.ZipFile(full_file_path, 'r') as zip_file:
                        if 'xl/sharedStrings.xml' in zip_file.namelist():
                            shared_strings_xml = zip_file.read('xl/sharedStrings.xml').decode('utf-8')
                            root = ET.fromstring(shared_strings_xml)
                            
                            # Найдем первые несколько строк
                            strings = []
                            for si in root.findall('.//{http://schemas.openxmlformats.org/spreadsheetml/2006/main}si')[:10]:
                                text_elements = si.findall('.//{http://schemas.openxmlformats.org/spreadsheetml/2006/main}t')
                                if text_elements:
                                    text = ''.join([elem.text or '' for elem in text_elements])
                                    strings.append(text[:100])  # Первые 100 символов
                            
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
            
            # Тест 5: Чтение worksheet.xml
            try:
                print("🔍 Test 5: Reading worksheet...")
                with zipfile.ZipFile(full_file_path, 'r') as zip_file:
                    worksheet_files = [f for f in zip_file.namelist() if f.startswith('xl/worksheets/sheet')]
                    
                    if worksheet_files:
                        # Читаем первый лист
                        worksheet_xml = zip_file.read(worksheet_files[0]).decode('utf-8')
                        root = ET.fromstring(worksheet_xml)
                        
                        # Найдем первые несколько ячеек
                        cells = []
                        for cell in root.findall('.//{http://schemas.openxmlformats.org/spreadsheetml/2006/main}c')[:20]:
                            cell_ref = cell.get('r', '')
                            cell_value = cell.find('.//{http://schemas.openxmlformats.org/spreadsheetml/2006/main}v')
                            if cell_value is not None:
                                cells.append({
                                    'ref': cell_ref,
                                    'value': cell_value.text
                                })
                        
                        result['tests']['worksheet'] = {
                            'success': True,
                            'worksheet_files': worksheet_files,
                            'sample_cells': cells
                        }
                    else:
                        result['tests']['worksheet'] = {
                            'success': False,
                            'error': 'No worksheet files found'
                        }
                
                print(f"✅ Worksheet read successfully")
            except Exception as e:
                result['tests']['worksheet'] = {
                    'success': False,
                    'error': str(e)
                }
                print(f"❌ Worksheet read failed: {e}")
            
            # Тест 6: Попробуем импортировать pandas
            try:
                print("🔍 Test 6: Pandas import test...")
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
            
            # Тест 7: Попробуем импортировать openpyxl
            try:
                print("🔍 Test 7: Openpyxl import test...")
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
            
            # Удаляем временный файл
            try:
                default_storage.delete(file_path)
            except:
                pass
            
            return Response(result, status=status.HTTP_200_OK)
            
        except Exception as e:
            print(f"❌ Basic Python test failed: {e}")
            import traceback
            traceback.print_exc()
            return Response(
                {'error': f'Базовый Python тест не удался: {str(e)}'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
