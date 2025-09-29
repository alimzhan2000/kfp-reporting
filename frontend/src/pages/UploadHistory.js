import React, { useState, useEffect } from 'react';
import { uploadAPI } from '../services/api';
import { FileText, CheckCircle, AlertCircle, Clock, RefreshCw, Trash2, Trash } from 'lucide-react';
import toast from 'react-hot-toast';

export const UploadHistory = () => {
  const [uploads, setUploads] = useState([]);
  const [loading, setLoading] = useState(true);
  const [deleting, setDeleting] = useState(false);
  const [showDeleteAllModal, setShowDeleteAllModal] = useState(false);

  useEffect(() => {
    fetchUploadHistory();
  }, []);

  const fetchUploadHistory = async () => {
    setLoading(true);
    try {
      const response = await uploadAPI.getUploadHistory();
      setUploads(response.data);
    } catch (error) {
      toast.error('Ошибка загрузки истории');
      console.error('Ошибка загрузки истории:', error);
    } finally {
      setLoading(false);
    }
  };

  const getStatusIcon = (status) => {
    switch (status) {
      case 'completed':
        return <CheckCircle className="h-5 w-5 text-green-500" />;
      case 'failed':
        return <AlertCircle className="h-5 w-5 text-red-500" />;
      case 'processing':
        return <RefreshCw className="h-5 w-5 text-blue-500 animate-spin" />;
      case 'pending':
        return <Clock className="h-5 w-5 text-yellow-500" />;
      default:
        return <Clock className="h-5 w-5 text-gray-500" />;
    }
  };

  const getStatusBadge = (status) => {
    switch (status) {
      case 'completed':
        return 'badge-success';
      case 'failed':
        return 'badge-danger';
      case 'processing':
        return 'badge-warning';
      case 'pending':
        return 'badge-secondary';
      default:
        return 'badge-secondary';
    }
  };

  const getStatusText = (status) => {
    switch (status) {
      case 'completed':
        return 'Завершено';
      case 'failed':
        return 'Ошибка';
      case 'processing':
        return 'Обрабатывается';
      case 'pending':
        return 'Ожидает';
      default:
        return 'Неизвестно';
    }
  };

  const formatFileSize = (bytes) => {
    if (bytes === 0) return '0 Bytes';
    const k = 1024;
    const sizes = ['Bytes', 'KB', 'MB', 'GB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
  };

  const formatDate = (dateString) => {
    return new Date(dateString).toLocaleString('ru-RU');
  };

  const handleDeleteUpload = async (uploadId, fileName) => {
    if (!window.confirm(`Вы уверены, что хотите удалить данные из файла "${fileName}"? Это действие нельзя отменить.`)) {
      return;
    }

    setDeleting(true);
    try {
      const response = await uploadAPI.deleteUploadData(uploadId);
      toast.success(`Данные из файла "${fileName}" успешно удалены`);
      fetchUploadHistory(); // Обновляем список
    } catch (error) {
      toast.error('Ошибка при удалении данных');
      console.error('Ошибка удаления:', error);
    } finally {
      setDeleting(false);
    }
  };

  const handleDeleteAllData = async () => {
    if (!window.confirm('Вы уверены, что хотите удалить ВСЕ данные в системе? Это действие нельзя отменить.')) {
      return;
    }

    setDeleting(true);
    try {
      const response = await uploadAPI.deleteAllData();
      toast.success('Все данные успешно удалены');
      fetchUploadHistory(); // Обновляем список
      setShowDeleteAllModal(false);
    } catch (error) {
      toast.error('Ошибка при удалении данных');
      console.error('Ошибка удаления:', error);
    } finally {
      setDeleting(false);
    }
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary-600"></div>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold text-gray-900">История загрузок</h1>
          <p className="mt-1 text-sm text-gray-500">
            История всех загруженных файлов и их статус обработки
          </p>
        </div>
        <div className="flex space-x-3">
          {uploads.length > 0 && (
            <button
              onClick={() => setShowDeleteAllModal(true)}
              disabled={deleting}
              className="btn-danger"
            >
              <Trash className="h-4 w-4 mr-2" />
              Удалить все данные
            </button>
          )}
          <button
            onClick={fetchUploadHistory}
            disabled={loading}
            className="btn-outline"
          >
            <RefreshCw className={`h-4 w-4 mr-2 ${loading ? 'animate-spin' : ''}`} />
            Обновить
          </button>
        </div>
      </div>

      {/* Uploads List */}
      {uploads.length === 0 ? (
        <div className="card text-center py-12">
          <FileText className="mx-auto h-12 w-12 text-gray-400" />
          <h3 className="mt-2 text-sm font-medium text-gray-900">Нет загрузок</h3>
          <p className="mt-1 text-sm text-gray-500">
            Здесь будут отображаться все загруженные файлы
          </p>
        </div>
      ) : (
        <div className="card">
          <div className="overflow-x-auto">
            <table className="table">
              <thead>
                <tr>
                  <th>Файл</th>
                  <th>Размер</th>
                  <th>Статус</th>
                  <th>Обработано записей</th>
                  <th>Создано записей</th>
                  <th>Обновлено записей</th>
                  <th>Дата загрузки</th>
                  <th>Завершено</th>
                  <th>Действия</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-gray-200">
                {uploads.map((upload) => (
                  <tr key={upload.id}>
                    <td>
                      <div className="flex items-center">
                        <FileText className="h-5 w-5 text-gray-400 mr-3" />
                        <div>
                          <div className="text-sm font-medium text-gray-900">
                            {upload.file_name}
                          </div>
                          <div className="text-sm text-gray-500">
                            {upload.uploaded_by_name}
                          </div>
                        </div>
                      </div>
                    </td>
                    <td className="text-sm text-gray-900">
                      {formatFileSize(upload.file_size)}
                    </td>
                    <td>
                      <div className="flex items-center">
                        {getStatusIcon(upload.status)}
                        <span className={`ml-2 ${getStatusBadge(upload.status)}`}>
                          {getStatusText(upload.status)}
                        </span>
                      </div>
                    </td>
                    <td className="text-sm text-gray-900">
                      {upload.records_processed || 0}
                    </td>
                    <td className="text-sm text-gray-900">
                      {upload.records_created || 0}
                    </td>
                    <td className="text-sm text-gray-900">
                      {upload.records_updated || 0}
                    </td>
                    <td className="text-sm text-gray-900">
                      {formatDate(upload.created_at)}
                    </td>
                    <td className="text-sm text-gray-900">
                      {upload.completed_at ? formatDate(upload.completed_at) : '-'}
                    </td>
                    <td>
                      <div className="flex space-x-2">
                        {upload.error_message && (
                          <button
                            className="text-red-600 hover:text-red-800"
                            title={upload.error_message}
                          >
                            <AlertCircle className="h-4 w-4" />
                          </button>
                        )}
                        {upload.status === 'completed' && (
                          <button
                            onClick={() => handleDeleteUpload(upload.id, upload.file_name)}
                            disabled={deleting}
                            className="text-red-600 hover:text-red-800 disabled:opacity-50"
                            title="Удалить данные из этого файла"
                          >
                            <Trash2 className="h-4 w-4" />
                          </button>
                        )}
                      </div>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      )}

      {/* Summary Stats */}
      {uploads.length > 0 && (
        <div className="grid grid-cols-1 gap-5 sm:grid-cols-2 lg:grid-cols-4">
          <div className="card">
            <div className="flex items-center">
              <div className="flex-shrink-0">
                <FileText className="h-8 w-8 text-blue-500" />
              </div>
              <div className="ml-5 w-0 flex-1">
                <dl>
                  <dt className="text-sm font-medium text-gray-500 truncate">Всего загрузок</dt>
                  <dd className="text-lg font-medium text-gray-900">{uploads.length}</dd>
                </dl>
              </div>
            </div>
          </div>
          
          <div className="card">
            <div className="flex items-center">
              <div className="flex-shrink-0">
                <CheckCircle className="h-8 w-8 text-green-500" />
              </div>
              <div className="ml-5 w-0 flex-1">
                <dl>
                  <dt className="text-sm font-medium text-gray-500 truncate">Успешно обработано</dt>
                  <dd className="text-lg font-medium text-gray-900">
                    {uploads.filter(u => u.status === 'completed').length}
                  </dd>
                </dl>
              </div>
            </div>
          </div>
          
          <div className="card">
            <div className="flex items-center">
              <div className="flex-shrink-0">
                <AlertCircle className="h-8 w-8 text-red-500" />
              </div>
              <div className="ml-5 w-0 flex-1">
                <dl>
                  <dt className="text-sm font-medium text-gray-500 truncate">С ошибками</dt>
                  <dd className="text-lg font-medium text-gray-900">
                    {uploads.filter(u => u.status === 'failed').length}
                  </dd>
                </dl>
              </div>
            </div>
          </div>
          
          <div className="card">
            <div className="flex items-center">
              <div className="flex-shrink-0">
                <Clock className="h-8 w-8 text-yellow-500" />
              </div>
              <div className="ml-5 w-0 flex-1">
                <dl>
                  <dt className="text-sm font-medium text-gray-500 truncate">В процессе</dt>
                  <dd className="text-lg font-medium text-gray-900">
                    {uploads.filter(u => u.status === 'processing' || u.status === 'pending').length}
                  </dd>
                </dl>
              </div>
            </div>
          </div>
        </div>
      )}

      {/* Delete All Data Modal */}
      {showDeleteAllModal && (
        <div className="fixed inset-0 bg-gray-600 bg-opacity-50 overflow-y-auto h-full w-full z-50">
          <div className="relative top-20 mx-auto p-5 border w-96 shadow-lg rounded-md bg-white">
            <div className="mt-3 text-center">
              <div className="mx-auto flex items-center justify-center h-12 w-12 rounded-full bg-red-100">
                <Trash className="h-6 w-6 text-red-600" />
              </div>
              <h3 className="text-lg font-medium text-gray-900 mt-4">
                Удалить все данные
              </h3>
              <div className="mt-2 px-7 py-3">
                <p className="text-sm text-gray-500">
                  Вы уверены, что хотите удалить ВСЕ данные в системе? Это действие нельзя отменить.
                  <br /><br />
                  Будет удалено:
                  <br />• Все сельскохозяйственные данные
                  <br />• Вся история загрузок
                </p>
              </div>
              <div className="items-center px-4 py-3">
                <button
                  onClick={handleDeleteAllData}
                  disabled={deleting}
                  className="px-4 py-2 bg-red-600 text-white text-base font-medium rounded-md w-24 mr-2 hover:bg-red-700 focus:outline-none focus:ring-2 focus:ring-red-300 disabled:opacity-50"
                >
                  {deleting ? 'Удаление...' : 'Удалить'}
                </button>
                <button
                  onClick={() => setShowDeleteAllModal(false)}
                  disabled={deleting}
                  className="px-4 py-2 bg-gray-300 text-gray-800 text-base font-medium rounded-md w-24 hover:bg-gray-400 focus:outline-none focus:ring-2 focus:ring-gray-300 disabled:opacity-50"
                >
                  Отмена
                </button>
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

