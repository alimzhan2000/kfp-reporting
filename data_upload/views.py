from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.views import APIView
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.db import transaction
import os

# Импортируем простой тест
from simple_test import SimpleFileTestView
from simple_test_view import simple_test_page
from ultra_simple_test import UltraSimpleTestView
from .models import DataUpload
from .serializers import DataUploadSerializer
from .services import DataProcessingService
from reports.models import AgriculturalData


@method_decorator(csrf_exempt, name='dispatch')
class FileUploadView(APIView):
    """
    API для загрузки файлов
    """
    parser_classes = (MultiPartParser, FormParser)
    permission_classes = []  # Убираем требование аутентификации
    
    def post(self, request, format=None):
        """
        Загрузка файла
        """
        if 'file' not in request.FILES:
            return Response(
                {'error': 'Файл не найден'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        uploaded_file = request.FILES['file']
        
        # Проверяем тип файла
        allowed_extensions = ['.csv', '.xlsx', '.xls']
        file_extension = os.path.splitext(uploaded_file.name)[1].lower()
        
        if file_extension not in allowed_extensions:
            return Response(
                {'error': 'Неподдерживаемый формат файла. Разрешены: CSV, XLSX, XLS'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            # Сохраняем файл
            file_path = default_storage.save(
                f'uploads/{uploaded_file.name}',
                ContentFile(uploaded_file.read())
            )
            
            # Создаем запись о загрузке (без пользователя для простоты)
            upload_instance = DataUpload.objects.create(
                file_name=uploaded_file.name,
                file_path=file_path,
                file_size=uploaded_file.size,
                uploaded_by=None  # Убираем привязку к пользователю
            )
            
            # Обрабатываем файл
            full_file_path = default_storage.path(file_path)
            success, message = DataProcessingService.process_file(upload_instance, full_file_path)
            
            if success:
                return Response({
                    'message': 'Файл успешно обработан',
                    'upload': DataUploadSerializer(upload_instance).data,
                    'details': message
                }, status=status.HTTP_201_CREATED)
            else:
                return Response({
                    'error': 'Ошибка обработки файла',
                    'details': message,
                    'upload': DataUploadSerializer(upload_instance).data
                }, status=status.HTTP_400_BAD_REQUEST)
                
        except Exception as e:
            return Response(
                {'error': f'Ошибка загрузки файла: {str(e)}'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def upload_history(request):
    """
    История загрузок
    """
    uploads = DataUpload.objects.filter(uploaded_by=request.user).order_by('-created_at')
    serializer = DataUploadSerializer(uploads, many=True)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def upload_status(request, upload_id):
    """
    Статус конкретной загрузки
    """
    try:
        upload = DataUpload.objects.get(id=upload_id, uploaded_by=request.user)
        serializer = DataUploadSerializer(upload)
        return Response(serializer.data)
    except DataUpload.DoesNotExist:
        return Response(
            {'error': 'Загрузка не найдена'},
            status=status.HTTP_404_NOT_FOUND
        )


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_upload_data(request, upload_id):
    """
    Удаление данных конкретной загрузки (только для администраторов)
    """
    # Проверяем, что пользователь - администратор
    if not request.user.is_staff and not request.user.role == 'admin':
        return Response(
            {'error': 'Недостаточно прав для выполнения операции'},
            status=status.HTTP_403_FORBIDDEN
        )
    
    try:
        upload = DataUpload.objects.get(id=upload_id)
        
        with transaction.atomic():
            # Удаляем все данные, загруженные этим файлом
            deleted_count = AgriculturalData.objects.filter(uploaded_by=upload.uploaded_by).count()
            AgriculturalData.objects.filter(uploaded_by=upload.uploaded_by).delete()
            
            # Удаляем запись о загрузке
            upload.delete()
            
            return Response({
                'message': f'Данные успешно удалены',
                'deleted_records': deleted_count,
                'upload_id': upload_id
            }, status=status.HTTP_200_OK)
            
    except DataUpload.DoesNotExist:
        return Response(
            {'error': 'Загрузка не найдена'},
            status=status.HTTP_404_NOT_FOUND
        )
    except Exception as e:
        return Response(
            {'error': f'Ошибка при удалении данных: {str(e)}'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_all_data(request):
    """
    Удаление всех данных в системе (только для администраторов)
    """
    # Проверяем, что пользователь - администратор
    if not request.user.is_staff and not request.user.role == 'admin':
        return Response(
            {'error': 'Недостаточно прав для выполнения операции'},
            status=status.HTTP_403_FORBIDDEN
        )
    
    try:
        with transaction.atomic():
            # Удаляем все сельскохозяйственные данные
            deleted_count = AgriculturalData.objects.count()
            AgriculturalData.objects.all().delete()
            
            # Удаляем все записи о загрузках
            upload_count = DataUpload.objects.count()
            DataUpload.objects.all().delete()
            
            return Response({
                'message': 'Все данные успешно удалены',
                'deleted_agricultural_records': deleted_count,
                'deleted_upload_records': upload_count
            }, status=status.HTTP_200_OK)
            
    except Exception as e:
        return Response(
            {'error': f'Ошибка при удалении данных: {str(e)}'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@method_decorator(csrf_exempt, name='dispatch')
class TestFileProcessingView(APIView):
    """
    Тестовый endpoint для проверки обработки файлов
    """
    parser_classes = (MultiPartParser, FormParser)
    permission_classes = []  # Без аутентификации для тестирования
    
    def post(self, request, format=None):
        """
        Тестирование обработки файла
        """
        if 'file' not in request.FILES:
            return Response(
                {'error': 'Файл не найден'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        uploaded_file = request.FILES['file']
        
        # Проверяем тип файла
        allowed_extensions = ['.csv', '.xlsx', '.xls']
        file_extension = os.path.splitext(uploaded_file.name)[1].lower()
        
        if file_extension not in allowed_extensions:
            return Response(
                {'error': 'Неподдерживаемый формат файла. Разрешены: CSV, XLSX, XLS'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            # Сохраняем файл
            file_path = default_storage.save(
                f'uploads/test_{uploaded_file.name}',
                ContentFile(uploaded_file.read())
            )
            
            # Создаем запись о загрузке
            upload_instance = DataUpload.objects.create(
                file_name=uploaded_file.name,
                file_path=file_path,
                file_size=uploaded_file.size,
                uploaded_by=None
            )
            
            # Обрабатываем файл
            full_file_path = default_storage.path(file_path)
            success, message = DataProcessingService.process_file(upload_instance, full_file_path)
            
            if success:
                return Response({
                    'message': 'Файл успешно обработан',
                    'upload': DataUploadSerializer(upload_instance).data,
                    'details': message,
                    'file_path': file_path,
                    'logs': 'Check Railway logs for detailed processing information'
                }, status=status.HTTP_201_CREATED)
            else:
                return Response({
                    'error': 'Ошибка обработки файла',
                    'details': message,
                    'upload': DataUploadSerializer(upload_instance).data,
                    'file_path': file_path,
                    'logs': 'Check Railway logs for detailed error information'
                }, status=status.HTTP_400_BAD_REQUEST)
                
        except Exception as e:
            return Response(
                {'error': f'Ошибка загрузки файла: {str(e)}'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

