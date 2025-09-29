import React, { useState, useEffect } from 'react';
import { reportsAPI } from '../../services/api';
import { 
  BarChart, 
  Bar, 
  XAxis, 
  YAxis, 
  CartesianGrid, 
  Tooltip, 
  Legend, 
  ResponsiveContainer,
  ScatterChart,
  Scatter,
  Cell
} from 'recharts';
import { 
  Filter, 
  Download, 
  RefreshCw,
  MapPin,
  TrendingUp,
  Activity
} from 'lucide-react';
import toast from 'react-hot-toast';

export const FieldEfficiencyReport = () => {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [activeView, setActiveView] = useState('heatmap');
  const [filters, setFilters] = useState({
    year_from: '',
    year_to: '',
    final_product: ''
  });

  useEffect(() => {
    fetchReportData();
  }, []);

  const fetchReportData = async (customFilters = null) => {
    setLoading(true);
    try {
      const params = customFilters || filters;
      const response = await reportsAPI.getFieldEfficiency(params);
      setData(response.data);
    } catch (error) {
      toast.error('Ошибка загрузки данных отчета');
      console.error('Ошибка загрузки данных:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleFilterChange = (key, value) => {
    setFilters(prev => ({ ...prev, [key]: value }));
  };

  const handleApplyFilters = () => {
    fetchReportData();
  };

  const handleResetFilters = () => {
    const resetFilters = {
      year_from: '',
      year_to: '',
      final_product: ''
    };
    setFilters(resetFilters);
    fetchReportData(resetFilters);
  };

  const formatTooltipValue = (value, name) => {
    if (name === 'avg_yield') return [`${value.toFixed(2)} ц/га`, 'Средняя урожайность'];
    if (name === 'total_area') return [`${value.toFixed(2)} га`, 'Общая площадь'];
    if (name === 'total_yield') return [`${value.toFixed(2)} ц`, 'Общий урожай'];
    if (name === 'product_count') return [value, 'Количество продуктов'];
    if (name === 'year_count') return [value, 'Количество лет'];
    if (name === 'record_count') return [value, 'Количество записей'];
    return [value, name];
  };

  const renderHeatmap = () => {
    if (!data?.field_data?.length) return <div className="text-center text-gray-500 py-8">Нет данных</div>;
    
    return (
      <div className="space-y-6">
        <div className="card">
          <h3 className="text-lg font-medium text-gray-900 mb-4">Тепловая карта эффективности полей</h3>
          <div className="grid grid-cols-1 gap-4 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4">
            {data.field_data.map((field, index) => (
              <div
                key={field.field_name}
                className={`p-4 rounded-lg border-2 transition-all hover:shadow-md cursor-pointer ${
                  field.efficiency_level === 'high' 
                    ? 'bg-green-50 border-green-200 hover:border-green-300'
                    : field.efficiency_level === 'medium'
                    ? 'bg-yellow-50 border-yellow-200 hover:border-yellow-300'
                    : 'bg-red-50 border-red-200 hover:border-red-300'
                }`}
                title={`Урожайность: ${field.avg_yield?.toFixed(2)} ц/га`}
              >
                <div className="flex items-center justify-between mb-2">
                  <h4 className="font-medium text-gray-900 truncate">{field.field_name}</h4>
                  <div 
                    className="w-4 h-4 rounded-full"
                    style={{ backgroundColor: field.color }}
                  />
                </div>
                <div className="space-y-1 text-sm text-gray-600">
                  <p><strong>Урожайность:</strong> {field.avg_yield?.toFixed(2)} ц/га</p>
                  <p><strong>Площадь:</strong> {field.total_area?.toFixed(1)} га</p>
                  <p><strong>Продуктов:</strong> {field.product_count}</p>
                  <p><strong>Лет:</strong> {field.year_count}</p>
                </div>
                <div className="mt-2">
                  <span className={`inline-flex items-center px-2 py-1 rounded-full text-xs font-medium ${
                    field.efficiency_level === 'high' 
                      ? 'bg-green-100 text-green-800'
                      : field.efficiency_level === 'medium'
                      ? 'bg-yellow-100 text-yellow-800'
                      : 'bg-red-100 text-red-800'
                  }`}>
                    {field.efficiency_level === 'high' && 'Высокая эффективность'}
                    {field.efficiency_level === 'medium' && 'Средняя эффективность'}
                    {field.efficiency_level === 'low' && 'Низкая эффективность'}
                  </span>
                </div>
              </div>
            ))}
          </div>
        </div>

        {/* Legend */}
        <div className="card">
          <h3 className="text-lg font-medium text-gray-900 mb-4">Легенда</h3>
          <div className="flex flex-wrap gap-4">
            <div className="flex items-center">
              <div className="w-4 h-4 rounded-full bg-green-500 mr-2"></div>
              <span className="text-sm text-gray-600">Высокая эффективность (≥80% от максимума)</span>
            </div>
            <div className="flex items-center">
              <div className="w-4 h-4 rounded-full bg-yellow-500 mr-2"></div>
              <span className="text-sm text-gray-600">Средняя эффективность (≥среднего)</span>
            </div>
            <div className="flex items-center">
              <div className="w-4 h-4 rounded-full bg-red-500 mr-2"></div>
              <span className="text-sm text-gray-600">Низкая эффективность (&lt;среднего)</span>
            </div>
          </div>
        </div>
      </div>
    );
  };

  const renderBarChart = () => {
    if (!data?.field_data?.length) return <div className="text-center text-gray-500 py-8">Нет данных</div>;
    
    return (
      <div className="space-y-6">
        <div className="card">
          <h3 className="text-lg font-medium text-gray-900 mb-4">Рейтинг полей по урожайности</h3>
          <ResponsiveContainer width="100%" height={400}>
            <BarChart data={data.field_data.slice(0, 15)}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis 
                dataKey="field_name" 
                angle={-45}
                textAnchor="end"
                height={100}
                interval={0}
              />
              <YAxis />
              <Tooltip formatter={formatTooltipValue} />
              <Legend />
              <Bar dataKey="avg_yield" name="Средняя урожайность (ц/га)">
                {data.field_data.slice(0, 15).map((entry, index) => (
                  <Cell key={`cell-${index}`} fill={entry.color} />
                ))}
              </Bar>
            </BarChart>
          </ResponsiveContainer>
        </div>
      </div>
    );
  };

  const renderScatterPlot = () => {
    if (!data?.field_data?.length) return <div className="text-center text-gray-500 py-8">Нет данных</div>;
    
    return (
      <div className="space-y-6">
        <div className="card">
          <h3 className="text-lg font-medium text-gray-900 mb-4">Соотношение площади и урожайности</h3>
          <ResponsiveContainer width="100%" height={400}>
            <ScatterChart data={data.field_data}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis 
                type="number" 
                dataKey="total_area" 
                name="Площадь"
                unit=" га"
              />
              <YAxis 
                type="number" 
                dataKey="avg_yield" 
                name="Урожайность"
                unit=" ц/га"
              />
              <Tooltip 
                cursor={{ strokeDasharray: '3 3' }}
                formatter={(value, name) => [
                  `${value.toFixed(2)} ${name === 'avg_yield' ? 'ц/га' : 'га'}`,
                  name === 'avg_yield' ? 'Урожайность' : 'Площадь'
                ]}
                labelFormatter={(value, payload) => {
                  if (payload && payload[0]) {
                    return `Поле: ${payload[0].payload.field_name}`;
                  }
                  return '';
                }}
              />
              <Scatter dataKey="avg_yield" fill="#8884d8">
                {data.field_data.map((entry, index) => (
                  <Cell key={`cell-${index}`} fill={entry.color} />
                ))}
              </Scatter>
            </ScatterChart>
          </ResponsiveContainer>
        </div>
      </div>
    );
  };

  const views = [
    { id: 'heatmap', name: 'Тепловая карта', icon: MapPin },
    { id: 'barchart', name: 'Рейтинг полей', icon: BarChart },
    { id: 'scatter', name: 'Площадь vs Урожайность', icon: Activity },
  ];

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold text-gray-900">Отчет по эффективности полей</h1>
          <p className="mt-1 text-sm text-gray-500">
            Анализ производительности каждого поля за определенный период
          </p>
        </div>
        <div className="flex space-x-3">
          <button
            onClick={() => fetchReportData()}
            disabled={loading}
            className="btn-outline"
          >
            <RefreshCw className={`h-4 w-4 mr-2 ${loading ? 'animate-spin' : ''}`} />
            Обновить
          </button>
          <button className="btn-secondary">
            <Download className="h-4 w-4 mr-2" />
            Экспорт
          </button>
        </div>
      </div>

      {/* Filters */}
      <div className="card">
        <div className="flex items-center mb-4">
          <Filter className="h-5 w-5 text-gray-400 mr-2" />
          <h3 className="text-lg font-medium text-gray-900">Фильтры</h3>
        </div>
        <div className="grid grid-cols-1 gap-4 sm:grid-cols-3">
          <div>
            <label className="label">Год от</label>
            <input
              type="number"
              className="input"
              placeholder="2020"
              value={filters.year_from}
              onChange={(e) => handleFilterChange('year_from', e.target.value)}
            />
          </div>
          <div>
            <label className="label">Год до</label>
            <input
              type="number"
              className="input"
              placeholder="2024"
              value={filters.year_to}
              onChange={(e) => handleFilterChange('year_to', e.target.value)}
            />
          </div>
          <div>
            <label className="label">Конечный продукт</label>
            <input
              type="text"
              className="input"
              placeholder="Название продукта"
              value={filters.final_product}
              onChange={(e) => handleFilterChange('final_product', e.target.value)}
            />
          </div>
        </div>
        <div className="flex justify-end space-x-3 mt-4">
          <button onClick={handleResetFilters} className="btn-outline">
            Сбросить
          </button>
          <button onClick={handleApplyFilters} className="btn-primary">
            Применить
          </button>
        </div>
      </div>

      {/* Statistics */}
      {data?.statistics && (
        <div className="grid grid-cols-1 gap-5 sm:grid-cols-2 lg:grid-cols-4">
          <div className="card">
            <div className="flex items-center">
              <div className="flex-shrink-0">
                <TrendingUp className="h-8 w-8 text-blue-500" />
              </div>
              <div className="ml-5 w-0 flex-1">
                <dl>
                  <dt className="text-sm font-medium text-gray-500 truncate">Мин. урожайность</dt>
                  <dd className="text-lg font-medium text-gray-900">{data.statistics.min_yield?.toFixed(2)} ц/га</dd>
                </dl>
              </div>
            </div>
          </div>
          
          <div className="card">
            <div className="flex items-center">
              <div className="flex-shrink-0">
                <TrendingUp className="h-8 w-8 text-green-500" />
              </div>
              <div className="ml-5 w-0 flex-1">
                <dl>
                  <dt className="text-sm font-medium text-gray-500 truncate">Макс. урожайность</dt>
                  <dd className="text-lg font-medium text-gray-900">{data.statistics.max_yield?.toFixed(2)} ц/га</dd>
                </dl>
              </div>
            </div>
          </div>
          
          <div className="card">
            <div className="flex items-center">
              <div className="flex-shrink-0">
                <Activity className="h-8 w-8 text-yellow-500" />
              </div>
              <div className="ml-5 w-0 flex-1">
                <dl>
                  <dt className="text-sm font-medium text-gray-500 truncate">Средняя урожайность</dt>
                  <dd className="text-lg font-medium text-gray-900">{data.statistics.avg_yield?.toFixed(2)} ц/га</dd>
                </dl>
              </div>
            </div>
          </div>
          
          <div className="card">
            <div className="flex items-center">
              <div className="flex-shrink-0">
                <MapPin className="h-8 w-8 text-purple-500" />
              </div>
              <div className="ml-5 w-0 flex-1">
                <dl>
                  <dt className="text-sm font-medium text-gray-500 truncate">Всего полей</dt>
                  <dd className="text-lg font-medium text-gray-900">{data.statistics.total_fields}</dd>
                </dl>
              </div>
            </div>
          </div>
        </div>
      )}

      {/* View Tabs */}
      <div className="border-b border-gray-200">
        <nav className="-mb-px flex space-x-8">
          {views.map((view) => (
            <button
              key={view.id}
              onClick={() => setActiveView(view.id)}
              className={`flex items-center py-2 px-1 border-b-2 font-medium text-sm ${
                activeView === view.id
                  ? 'border-primary-500 text-primary-600'
                  : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
              }`}
            >
              <view.icon className="h-4 w-4 mr-2" />
              {view.name}
            </button>
          ))}
        </nav>
      </div>

      {/* Content */}
      {loading ? (
        <div className="flex items-center justify-center h-64">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary-600"></div>
        </div>
      ) : (
        <div className="animate-fade-in">
          {activeView === 'heatmap' && renderHeatmap()}
          {activeView === 'barchart' && renderBarChart()}
          {activeView === 'scatter' && renderScatterPlot()}
        </div>
      )}
    </div>
  );
};

