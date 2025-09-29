import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { reportsAPI } from '../services/api';
import { 
  TrendingUp, 
  MapPin, 
  Sprout, 
  FileText, 
  BarChart3,
  Calendar,
  Activity
} from 'lucide-react';
import toast from 'react-hot-toast';

export const Dashboard = () => {
  const [stats, setStats] = useState(null);
  const [loading, setLoading] = useState(true);
  const navigate = useNavigate();

  useEffect(() => {
    fetchDashboardStats();
  }, []);

  const fetchDashboardStats = async () => {
    try {
      const response = await reportsAPI.getDashboardStats();
      setStats(response.data);
    } catch (error) {
      toast.error('Ошибка загрузки статистики');
      console.error('Ошибка загрузки статистики:', error);
    } finally {
      setLoading(false);
    }
  };

  const statCards = [
    {
      name: 'Всего записей',
      value: stats?.total_records || 0,
      icon: FileText,
      color: 'bg-blue-500',
      href: '/upload-history'
    },
    {
      name: 'Количество полей',
      value: stats?.unique_fields || 0,
      icon: MapPin,
      color: 'bg-green-500',
      href: '/reports/field-efficiency'
    },
    {
      name: 'Конечные продукты',
      value: stats?.unique_products || 0,
      icon: Sprout,
      color: 'bg-yellow-500',
      href: '/reports/variety-performance'
    },
    {
      name: 'Сорта',
      value: stats?.unique_varieties || 0,
      icon: Activity,
      color: 'bg-purple-500',
      href: '/reports/variety-performance'
    }
  ];

  const quickActions = [
    {
      name: 'Загрузить файл',
      description: 'Загрузить новые данные CSV/XLSX',
      icon: FileText,
      href: '/upload',
      color: 'bg-primary-500'
    },
    {
      name: 'Сравнительный отчет',
      description: 'Сравнить урожайность по различным параметрам',
      icon: BarChart3,
      href: '/reports/yield-comparison',
      color: 'bg-green-500'
    },
    {
      name: 'Эффективность полей',
      description: 'Анализ производительности полей',
      icon: MapPin,
      href: '/reports/field-efficiency',
      color: 'bg-blue-500'
    },
    {
      name: 'Производительность сортов',
      description: 'Сравнение сортов в рамках культур',
      icon: TrendingUp,
      href: '/reports/variety-performance',
      color: 'bg-purple-500'
    }
  ];

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
      <div>
        <h1 className="text-2xl font-bold text-gray-900">Дашборд</h1>
        <p className="mt-1 text-sm text-gray-500">
          Обзор сельскохозяйственных данных и отчетов
        </p>
      </div>

      {/* Stats */}
      <div className="grid grid-cols-1 gap-5 sm:grid-cols-2 lg:grid-cols-4">
        {statCards.map((stat) => (
          <div
            key={stat.name}
            className="relative bg-white pt-5 px-4 pb-12 sm:pt-6 sm:px-6 shadow rounded-lg overflow-hidden cursor-pointer hover:shadow-md transition-shadow"
            onClick={() => navigate(stat.href)}
          >
            <dt>
              <div className={`absolute ${stat.color} rounded-md p-3`}>
                <stat.icon className="h-6 w-6 text-white" />
              </div>
              <p className="ml-16 text-sm font-medium text-gray-500 truncate">
                {stat.name}
              </p>
            </dt>
            <dd className="ml-16 pb-6 flex items-baseline sm:pb-7">
              <p className="text-2xl font-semibold text-gray-900">
                {stat.value}
              </p>
            </dd>
          </div>
        ))}
      </div>

      {/* Additional Info */}
      {stats && (
        <div className="bg-white shadow rounded-lg p-6">
          <h3 className="text-lg font-medium text-gray-900 mb-4">Дополнительная информация</h3>
          <div className="grid grid-cols-1 gap-4 sm:grid-cols-3">
            <div className="flex items-center">
              <Calendar className="h-5 w-5 text-gray-400 mr-2" />
              <span className="text-sm text-gray-500">Последний год данных:</span>
              <span className="ml-2 text-sm font-medium text-gray-900">{stats.latest_year || 'Нет данных'}</span>
            </div>
            <div className="flex items-center">
              <TrendingUp className="h-5 w-5 text-gray-400 mr-2" />
              <span className="text-sm text-gray-500">Средняя урожайность:</span>
              <span className="ml-2 text-sm font-medium text-gray-900">{stats.avg_yield} ц/га</span>
            </div>
            <div className="flex items-center">
              <MapPin className="h-5 w-5 text-gray-400 mr-2" />
              <span className="text-sm text-gray-500">Общая площадь:</span>
              <span className="ml-2 text-sm font-medium text-gray-900">{stats.total_area} га</span>
            </div>
          </div>
        </div>
      )}

      {/* Quick Actions */}
      <div className="bg-white shadow rounded-lg p-6">
        <h3 className="text-lg font-medium text-gray-900 mb-4">Быстрые действия</h3>
        <div className="grid grid-cols-1 gap-4 sm:grid-cols-2 lg:grid-cols-4">
          {quickActions.map((action) => (
            <div
              key={action.name}
              className="relative group bg-white p-6 focus-within:ring-2 focus-within:ring-inset focus-within:ring-primary-500 rounded-lg border border-gray-200 hover:border-gray-300 cursor-pointer transition-colors"
              onClick={() => navigate(action.href)}
            >
              <div>
                <span className={`${action.color} rounded-lg inline-flex p-3 ring-4 ring-white`}>
                  <action.icon className="h-6 w-6 text-white" />
                </span>
              </div>
              <div className="mt-8">
                <h3 className="text-lg font-medium">
                  <span className="absolute inset-0" />
                  {action.name}
                </h3>
                <p className="mt-2 text-sm text-gray-500">
                  {action.description}
                </p>
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};

