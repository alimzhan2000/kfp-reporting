#!/usr/bin/env python
"""
Минимальный тест pandas
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

@method_decorator(csrf_exempt, name='dispatch')
class MinimalPandasTestView(APIView):
    """
    Минимальный тест pandas - только импорт
    """
    parser_classes = (MultiPartParser, FormParser)
    permission_classes = []  # Без аутентификации
    
    def post(self, request, format=None):
        """
        Минимальное тестирование pandas
        """
        try:
            print("🧪 Minimal pandas test...")
            
            result = {
                'test_name': 'minimal_pandas_test',
                'tests': {}
            }
            
            # Тест 1: Импорт pandas
            try:
                print("🔍 Test 1: Importing pandas...")
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
                print("🔍 Test 2: Importing openpyxl...")
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
            
            # Тест 3: Создание простого DataFrame
            try:
                print("🔍 Test 3: Creating simple DataFrame...")
                df = pd.DataFrame({'test': [1, 2, 3]})
                result['tests']['dataframe_creation'] = {
                    'success': True,
                    'shape': df.shape,
                    'data': df.to_dict('records')
                }
                print(f"✅ DataFrame created: {df.shape}")
            except Exception as e:
                result['tests']['dataframe_creation'] = {
                    'success': False,
                    'error': str(e)
                }
                print(f"❌ DataFrame creation failed: {e}")
            
            # Тест 4: Проверка версий
            try:
                print("🔍 Test 4: Version compatibility check...")
                import sys
                result['tests']['version_check'] = {
                    'success': True,
                    'python_version': sys.version,
                    'pandas_version': pd.__version__,
                    'openpyxl_version': openpyxl.__version__ if 'openpyxl' in locals() else 'Not imported'
                }
                print(f"✅ Version check completed")
            except Exception as e:
                result['tests']['version_check'] = {
                    'success': False,
                    'error': str(e)
                }
                print(f"❌ Version check failed: {e}")
            
            return Response(result, status=status.HTTP_200_OK)
            
        except Exception as e:
            print(f"❌ Minimal pandas test failed: {e}")
            import traceback
            traceback.print_exc()
            return Response(
                {'error': f'Минимальный тест pandas не удался: {str(e)}'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
