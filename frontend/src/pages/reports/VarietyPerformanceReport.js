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
  PieChart,
  Pie,
  Cell
} from 'recharts';
import { 
  Filter, 
  Download, 
  RefreshCw,
  Sprout,
  TrendingUp,
  BarChart3
} from 'lucide-react';
import toast from 'react-hot-toast';

const COLORS = ['#0088FE', '#00C49F', '#FFBB28', '#FF8042', '#8884D8', '#82CA9D', '#FF6B6B', '#4ECDC4'];

export const VarietyPerformanceReport = () => {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [activeView, setActiveView] = useState('varieties');
  const [selectedProduct, setSelectedProduct] = useState('');
  const [filters, setFilters] = useState({
    final_product: '',
    year_from: '',
    year_to: '',
    field_name: ''
  });

  useEffect(() => {
    fetchReportData();
  }, []);

  const fetchReportData = async (customFilters = null) => {
    setLoading(true);
    try {
      const params = customFilters || filters;
      const response = await reportsAPI.getVarietyPerformance(params);
      setData(response.data);
      
      // Если не выбрана культура, выбираем первую доступную
      if (!selectedProduct && response.data.product_summary?.length > 0) {
        setSelectedProduct(response.data.product_summary[0].final_product);
      }
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
      final_product: '',
      year_from: '',
      year_to: '',
      field_name: ''
    };
    setFilters(resetFilters);
    setSelectedProduct('');
    fetchReportData(resetFilters);
  };

  const formatTooltipValue = (value, name) => {
    if (name === 'avg_yield') return [`${value.toFixed(2)} ц/га`, 'Средняя урожайность'];
    if (name === 'total_area') return [`${value.toFixed(2)} га`, 'Общая площадь'];
    if (name === 'total_yield') return [`${value.toFixed(2)} ц`, 'Общий урожай'];
    if (name === 'field_count') return [value, 'Количество полей'];
    if (name === 'year_count') return [value, 'Количество лет'];
    if (name === 'record_count') return [value, 'Количество записей'];
    if (name === 'variety_count') return [value, 'Количество сортов'];
    return [value, name];
  };

  const renderVarietyComparison = () => {
    if (!data?.variety_data?.length) return <div className="text-center text-gray-500 py-8">Нет данных</div>;
    
    // Фильтруем данные по выбранной культуре
    const filteredData = selectedProduct 
      ? data.variety_data.filter(item => item.final_product === selectedProduct)
      : data.variety_data;
    
    return (
      <div className="space-y-6">
        {/* Product Selector */}
        {data.product_summary?.length > 1 && (
          <div className="card">
            <h3 className="text-lg font-medium text-gray-900 mb-4">Выберите конечный продукт для анализа</h3>
            <div className="grid grid-cols-2 gap-3 sm:grid-cols-3 lg:grid-cols-4">
              {data.product_summary.map((prod) => (
                <button
                  key={prod.final_product}
                  onClick={() => setSelectedProduct(prod.final_product)}
                  className={`p-3 rounded-lg border-2 text-left transition-colors ${
                    selectedProduct === prod.final_product
                      ? 'border-primary-500 bg-primary-50'
                      : 'border-gray-200 hover:border-gray-300'
                  }`}
                >
                  <div className="font-medium text-gray-900">{prod.final_product}</div>
                  <div className="text-sm text-gray-500">
                    {prod.variety_count} сортов, {prod.avg_yield?.toFixed(1)} ц/га
                  </div>
                </button>
              ))}
            </div>
          </div>
        )}

        <div className="card">
          <h3 className="text-lg font-medium text-gray-900 mb-4">
            Сравнение сортов {selectedProduct && `- ${selectedProduct}`}
          </h3>
          <ResponsiveContainer width="100%" height={400}>
            <BarChart data={filteredData}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis 
                dataKey="variety" 
                angle={-45}
                textAnchor="end"
                height={100}
                interval={0}
              />
              <YAxis />
              <Tooltip formatter={formatTooltipValue} />
              <Legend />
              <Bar dataKey="avg_yield" name="Средняя урожайность (ц/га)">
                {filteredData.map((entry, index) => (
                  <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                ))}
              </Bar>
            </BarChart>
          </ResponsiveContainer>
        </div>

        {/* Statistics for selected product */}
        {selectedProduct && data.product_variety_stats?.[selectedProduct] && (
          <div className="card">
            <h3 className="text-lg font-medium text-gray-900 mb-4">Статистика по {selectedProduct}</h3>
            <div className="grid grid-cols-1 gap-4 sm:grid-cols-3">
              <div className="bg-blue-50 p-4 rounded-lg">
                <div className="text-sm font-medium text-blue-700">Минимальная урожайность</div>
                <div className="text-2xl font-bold text-blue-900">
                  {data.product_variety_stats[selectedProduct].min_yield?.toFixed(2)} ц/га
                </div>
              </div>
              <div className="bg-green-50 p-4 rounded-lg">
                <div className="text-sm font-medium text-green-700">Максимальная урожайность</div>
                <div className="text-2xl font-bold text-green-900">
                  {data.product_variety_stats[selectedProduct].max_yield?.toFixed(2)} ц/га
                </div>
              </div>
              <div className="bg-yellow-50 p-4 rounded-lg">
                <div className="text-sm font-medium text-yellow-700">Средняя урожайность</div>
                <div className="text-2xl font-bold text-yellow-900">
                  {data.product_variety_stats[selectedProduct].avg_yield?.toFixed(2)} ц/га
                </div>
              </div>
            </div>
          </div>
        )}

        {/* Variety Details Table */}
        <div className="card">
          <h3 className="text-lg font-medium text-gray-900 mb-4">Детальная информация по сортам</h3>
          <div className="overflow-x-auto">
            <table className="table">
              <thead>
                <tr>
                  <th>Конечный продукт</th>
                  <th>Сорт</th>
                  <th>Урожайность (ц/га)</th>
                  <th>Площадь (га)</th>
                  <th>Общий урожай (ц)</th>
                  <th>Поля</th>
                  <th>Лет</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-gray-200">
                {filteredData.map((item, index) => (
                  <tr key={`${item.final_product}-${item.variety}`}>
                    <td className="font-medium">{item.final_product}</td>
                    <td className="font-medium">{item.variety}</td>
                    <td className="font-semibold text-green-600">
                      {item.avg_yield?.toFixed(2)}
                    </td>
                    <td>{item.total_area?.toFixed(1)}</td>
                    <td className="font-medium">
                      {item.total_yield?.toFixed(1)}
                    </td>
                    <td>{item.field_count}</td>
                    <td>{item.year_count}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      </div>
    );
  };

  const renderCropComparison = () => {
    if (!data?.crop_summary?.length) return <div className="text-center text-gray-500 py-8">Нет данных</div>;
    
    return (
      <div className="space-y-6">
        <div className="card">
          <h3 className="text-lg font-medium text-gray-900 mb-4">Сравнение культур по средней урожайности</h3>
          <ResponsiveContainer width="100%" height={400}>
            <BarChart data={data.crop_summary}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis 
                dataKey="crop" 
                angle={-45}
                textAnchor="end"
                height={100}
                interval={0}
              />
              <YAxis />
              <Tooltip formatter={formatTooltipValue} />
              <Legend />
              <Bar dataKey="avg_yield" name="Средняя урожайность (ц/га)" fill="#8884d8" />
            </BarChart>
          </ResponsiveContainer>
        </div>

        <div className="card">
          <h3 className="text-lg font-medium text-gray-900 mb-4">Распределение сортов по культурам</h3>
          <ResponsiveContainer width="100%" height={400}>
            <PieChart>
              <Pie
                data={data.crop_summary}
                cx="50%"
                cy="50%"
                labelLine={false}
                label={({ crop, variety_count }) => `${crop}: ${variety_count} сортов`}
                outerRadius={120}
                fill="#8884d8"
                dataKey="variety_count"
              >
                {data.crop_summary.map((entry, index) => (
                  <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                ))}
              </Pie>
              <Tooltip formatter={formatTooltipValue} />
            </PieChart>
          </ResponsiveContainer>
        </div>
      </div>
    );
  };

  const renderAreaDistribution = () => {
    if (!data?.variety_data?.length) return <div className="text-center text-gray-500 py-8">Нет данных</div>;
    
    return (
      <div className="space-y-6">
        <div className="card">
          <h3 className="text-lg font-medium text-gray-900 mb-4">Распределение площадей по сортам</h3>
          <ResponsiveContainer width="100%" height={400}>
            <BarChart data={data.variety_data.slice(0, 20)}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis 
                dataKey="variety" 
                angle={-45}
                textAnchor="end"
                height={100}
                interval={0}
              />
              <YAxis />
              <Tooltip formatter={formatTooltipValue} />
              <Legend />
              <Bar dataKey="total_area" name="Общая площадь (га)" fill="#00C49F" />
            </BarChart>
          </ResponsiveContainer>
        </div>
      </div>
    );
  };

  const views = [
    { id: 'varieties', name: 'Сравнение сортов', icon: Sprout },
    { id: 'crops', name: 'Сравнение продуктов', icon: BarChart3 },
    { id: 'areas', name: 'Распределение площадей', icon: TrendingUp },
  ];

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold text-gray-900">Отчет по производительности сортов</h1>
          <p className="mt-1 text-sm text-gray-500">
            Сравнение урожайности различных сортов в рамках культур
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
        <div className="grid grid-cols-1 gap-4 sm:grid-cols-2 lg:grid-cols-4">
          <div>
            <label className="label">Культура</label>
            <input
              type="text"
              className="input"
              placeholder="Название культуры"
              value={filters.crop}
              onChange={(e) => handleFilterChange('crop', e.target.value)}
            />
          </div>
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
            <label className="label">Поле</label>
            <input
              type="text"
              className="input"
              placeholder="Название поля"
              value={filters.field_name}
              onChange={(e) => handleFilterChange('field_name', e.target.value)}
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

      {/* Summary */}
      {data && (
        <div className="card bg-blue-50 border-blue-200">
          <h3 className="text-lg font-medium text-blue-900 mb-2">Сводка</h3>
          <div className="grid grid-cols-1 gap-2 sm:grid-cols-3">
            <p className="text-blue-700">
              Всего обработано записей: <strong>{data.total_records}</strong>
            </p>
            <p className="text-blue-700">
              Уникальных культур: <strong>{data.crop_summary?.length || 0}</strong>
            </p>
            <p className="text-blue-700">
              Уникальных сортов: <strong>{data.variety_data?.length || 0}</strong>
            </p>
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
          {activeView === 'varieties' && renderVarietyComparison()}
          {activeView === 'crops' && renderCropComparison()}
          {activeView === 'areas' && renderAreaDistribution()}
        </div>
      )}
    </div>
  );
};

