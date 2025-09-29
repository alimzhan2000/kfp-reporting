import React, { useState, useRef } from 'react';
import { uploadAPI } from '../services/api';
import { Upload, CheckCircle, AlertCircle, X } from 'lucide-react';
import toast from 'react-hot-toast';

export const FileUpload = () => {
  const [dragActive, setDragActive] = useState(false);
  const [uploading, setUploading] = useState(false);
  const [uploadResult, setUploadResult] = useState(null);
  const fileInputRef = useRef(null);

  const handleDrag = (e) => {
    e.preventDefault();
    e.stopPropagation();
    if (e.type === 'dragenter' || e.type === 'dragover') {
      setDragActive(true);
    } else if (e.type === 'dragleave') {
      setDragActive(false);
    }
  };

  const handleDrop = (e) => {
    e.preventDefault();
    e.stopPropagation();
    setDragActive(false);
    
    if (e.dataTransfer.files && e.dataTransfer.files[0]) {
      handleFile(e.dataTransfer.files[0]);
    }
  };

  const handleFileInput = (e) => {
    if (e.target.files && e.target.files[0]) {
      handleFile(e.target.files[0]);
    }
  };

  const handleFile = async (file) => {
    // Проверяем тип файла
    const allowedTypes = [
      'text/csv',
      'application/vnd.ms-excel',
      'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    ];
    
    if (!allowedTypes.includes(file.type) && !file.name.match(/\.(csv|xlsx|xls)$/i)) {
      toast.error('Неподдерживаемый формат файла. Разрешены: CSV, XLSX, XLS');
      return;
    }

    // Проверяем размер файла (10MB)
    if (file.size > 10 * 1024 * 1024) {
      toast.error('Размер файла не должен превышать 10MB');
      return;
    }

    setUploading(true);
    setUploadResult(null);

    try {
      const formData = new FormData();
      formData.append('file', file);

      const response = await uploadAPI.uploadFile(formData);
      
      if (response.data.message) {
        toast.success(response.data.message);
        setUploadResult({
          success: true,
          data: response.data.upload,
          details: response.data.details
        });
      } else {
        toast.error(response.data.error || 'Ошибка загрузки файла');
        setUploadResult({
          success: false,
          error: response.data.error || 'Неизвестная ошибка',
          details: response.data.details
        });
      }
    } catch (error) {
      const errorMessage = error.response?.data?.error || 'Ошибка загрузки файла';
      toast.error(errorMessage);
      setUploadResult({
        success: false,
        error: errorMessage
      });
    } finally {
      setUploading(false);
    }
  };

  const clearResult = () => {
    setUploadResult(null);
  };

  const openFileDialog = () => {
    fileInputRef.current?.click();
  };

  return (
    <div className="space-y-6">
      {/* Header */}
      <div>
        <h1 className="text-2xl font-bold text-gray-900">Загрузка файлов</h1>
        <p className="mt-1 text-sm text-gray-500">
          Загрузите CSV или XLSX файлы с сельскохозяйственными данными
        </p>
      </div>

      {/* Upload Area */}
      <div className="card">
        <div
          className={`relative border-2 border-dashed rounded-lg p-12 text-center hover:border-gray-400 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary-500 ${
            dragActive
              ? 'border-primary-400 bg-primary-50'
              : 'border-gray-300'
          } ${uploading ? 'opacity-50 cursor-not-allowed' : 'cursor-pointer'}`}
          onDragEnter={handleDrag}
          onDragLeave={handleDrag}
          onDragOver={handleDrag}
          onDrop={handleDrop}
          onClick={uploading ? undefined : openFileDialog}
        >
          <input
            ref={fileInputRef}
            type="file"
            className="hidden"
            accept=".csv,.xlsx,.xls"
            onChange={handleFileInput}
            disabled={uploading}
          />

          {uploading ? (
            <div className="space-y-4">
              <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary-600 mx-auto"></div>
              <div>
                <p className="text-lg font-medium text-gray-900">Обработка файла...</p>
                <p className="text-sm text-gray-500">Пожалуйста, подождите</p>
              </div>
            </div>
          ) : (
            <div className="space-y-4">
              <Upload className="mx-auto h-12 w-12 text-gray-400" />
              <div>
                <p className="text-lg font-medium text-gray-900">
                  Перетащите файл сюда или нажмите для выбора
                </p>
                <p className="text-sm text-gray-500">
                  Поддерживаются форматы: CSV, XLSX, XLS (макс. 10MB)
                </p>
              </div>
            </div>
          )}
        </div>
      </div>

      {/* Required Columns Info */}
      <div className="card bg-blue-50 border-blue-200">
        <h3 className="text-lg font-medium text-blue-900 mb-4">Обязательные колонки</h3>
        <p className="text-sm text-blue-700 mb-4">
          Файл должен содержать следующие колонки:
        </p>
        <div className="grid grid-cols-1 gap-2 sm:grid-cols-2 lg:grid-cols-3">
          {[
            'Поле',
            'Год',
            'Площадь посева',
            'Урожайность, ц/га',
            'Сорт',
            'Конечный продукт'
          ].map((column) => (
            <div key={column} className="flex items-center">
              <CheckCircle className="h-4 w-4 text-blue-600 mr-2" />
              <span className="text-sm text-blue-800">{column}</span>
            </div>
          ))}
        </div>
      </div>

      {/* Upload Result */}
      {uploadResult && (
        <div className="card">
          <div className="flex items-start justify-between">
            <div className="flex items-start">
              {uploadResult.success ? (
                <CheckCircle className="h-6 w-6 text-green-600 mt-1 mr-3" />
              ) : (
                <AlertCircle className="h-6 w-6 text-red-600 mt-1 mr-3" />
              )}
              <div>
                <h3 className={`text-lg font-medium ${uploadResult.success ? 'text-green-900' : 'text-red-900'}`}>
                  {uploadResult.success ? 'Файл успешно обработан' : 'Ошибка обработки файла'}
                </h3>
                {uploadResult.data && (
                  <div className="mt-2 space-y-1 text-sm">
                    <p className="text-gray-600">
                      <strong>Файл:</strong> {uploadResult.data.file_name}
                    </p>
                    <p className="text-gray-600">
                      <strong>Статус:</strong> 
                      <span className={`ml-1 px-2 py-1 rounded-full text-xs ${
                        uploadResult.data.status === 'completed' 
                          ? 'bg-green-100 text-green-800'
                          : uploadResult.data.status === 'failed'
                          ? 'bg-red-100 text-red-800'
                          : 'bg-yellow-100 text-yellow-800'
                      }`}>
                        {uploadResult.data.status === 'completed' && 'Завершено'}
                        {uploadResult.data.status === 'failed' && 'Ошибка'}
                        {uploadResult.data.status === 'processing' && 'Обрабатывается'}
                        {uploadResult.data.status === 'pending' && 'Ожидает'}
                      </span>
                    </p>
                    {uploadResult.data.records_processed && (
                      <p className="text-gray-600">
                        <strong>Обработано записей:</strong> {uploadResult.data.records_processed}
                      </p>
                    )}
                    {uploadResult.data.records_created && (
                      <p className="text-gray-600">
                        <strong>Создано записей:</strong> {uploadResult.data.records_created}
                      </p>
                    )}
                    {uploadResult.data.records_updated && (
                      <p className="text-gray-600">
                        <strong>Обновлено записей:</strong> {uploadResult.data.records_updated}
                      </p>
                    )}
                    {uploadResult.details && (
                      <p className="text-gray-600">
                        <strong>Детали:</strong> {uploadResult.details}
                      </p>
                    )}
                  </div>
                )}
                {uploadResult.error && (
                  <p className="mt-2 text-sm text-red-600">
                    <strong>Ошибка:</strong> {uploadResult.error}
                  </p>
                )}
              </div>
            </div>
            <button
              onClick={clearResult}
              className="text-gray-400 hover:text-gray-600"
            >
              <X className="h-5 w-5" />
            </button>
          </div>
        </div>
      )}
    </div>
  );
};

