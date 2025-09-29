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
  LineChart, 
  Line,
  ResponsiveContainer,
  PieChart,
  Pie,
  Cell
} from 'recharts';
import { 
  Filter, 
  Download, 
  RefreshCw,
  BarChart3,
  TrendingUp,
  PieChart as PieChartIcon
} from 'lucide-react';
import toast from 'react-hot-toast';

const COLORS = ['#0088FE', '#00C49F', '#FFBB28', '#FF8042', '#8884D8', '#82CA9D'];

export const YieldComparisonReport = () => {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [activeTab, setActiveTab] = useState('fields');
  const [filters, setFilters] = useState({
    field_name: '',
    year_from: '',
    year_to: '',
    // crop removed; use final_product
    variety: '',
    final_product: ''
  });

  useEffect(() => {
    fetchReportData();
  }, []);

  const fetchReportData = async (customFilters = null) => {
    setLoading(true);
    try {
      const params = customFilters || filters;
      const response = await reportsAPI.getYieldComparison(params);
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
      field_name: '',
      year_from: '',
      year_to: '',
      variety: '',
      final_product: ''
    };
    setFilters(resetFilters);
    fetchReportData(resetFilters);
  };

  const formatTooltipValue = (value, name) => {
    if (name === 'avg_yield') return [`${value.toFixed(2)} ц/га`, 'Средняя урожайность'];
    if (name === 'total_area') return [`${value.toFixed(2)} га`, 'Общая площадь'];
    if (name === 'total_yield') return [`${value.toFixed(2)} ц`, 'Общий урожай'];
    return [value, name];
  };

  const renderFieldComparison = () => {
    if (!data?.field_comparison?.length) return <div className="text-center text-gray-500 py-8">Нет данных</div>;
    
    return (
      <div className="space-y-6">
        <div className="card">
          <h3 className="text-lg font-medium text-gray-900 mb-4">Сравнение по полям</h3>
          <ResponsiveContainer width="100%" height={400}>
            <BarChart data={data.field_comparison}>
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
              <Bar dataKey="avg_yield" fill="#0088FE" name="Средняя урожайность (ц/га)" />
            </BarChart>
          </ResponsiveContainer>
        </div>

        <div className="card">
          <h3 className="text-lg font-medium text-gray-900 mb-4">Общая площадь по полям</h3>
          <ResponsiveContainer width="100%" height={400}>
            <BarChart data={data.field_comparison}>
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
              <Bar dataKey="total_area" fill="#00C49F" name="Общая площадь (га)" />
            </BarChart>
          </ResponsiveContainer>
        </div>
      </div>
    );
  };

  const renderYearComparison = () => {
    if (!data?.year_comparison?.length) return <div className="text-center text-gray-500 py-8">Нет данных</div>;
    
    return (
      <div className="space-y-6">
        <div className="card">
          <h3 className="text-lg font-medium text-gray-900 mb-4">Динамика урожайности по годам</h3>
          <ResponsiveContainer width="100%" height={400}>
            <LineChart data={data.year_comparison}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="year" />
              <YAxis />
              <Tooltip formatter={formatTooltipValue} />
              <Legend />
              <Line type="monotone" dataKey="avg_yield" stroke="#0088FE" strokeWidth={3} name="Средняя урожайность (ц/га)" />
            </LineChart>
          </ResponsiveContainer>
        </div>

        <div className="card">
          <h3 className="text-lg font-medium text-gray-900 mb-4">Общая площадь по годам</h3>
          <ResponsiveContainer width="100%" height={400}>
            <BarChart data={data.year_comparison}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="year" />
              <YAxis />
              <Tooltip formatter={formatTooltipValue} />
              <Legend />
              <Bar dataKey="total_area" fill="#FFBB28" name="Общая площадь (га)" />
            </BarChart>
          </ResponsiveContainer>
        </div>
      </div>
    );
  };

  const renderProductComparison = () => {
    if (!data?.product_comparison?.length) return <div className="text-center text-gray-500 py-8">Нет данных</div>;
    
    return (
      <div className="space-y-6">
        <div className="card">
          <h3 className="text-lg font-medium text-gray-900 mb-4">Урожайность по конечным продуктам</h3>
          <ResponsiveContainer width="100%" height={400}>
            <BarChart data={data.product_comparison}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis 
                dataKey="final_product" 
                angle={-45}
                textAnchor="end"
                height={100}
                interval={0}
              />
              <YAxis />
              <Tooltip formatter={formatTooltipValue} />
              <Legend />
              <Bar dataKey="avg_yield" fill="#8884D8" name="Средняя урожайность (ц/га)" />
            </BarChart>
          </ResponsiveContainer>
        </div>

        <div className="card">
          <h3 className="text-lg font-medium text-gray-900 mb-4">Распределение площадей по конечным продуктам</h3>
          <ResponsiveContainer width="100%" height={400}>
            <PieChart>
              <Pie
                data={data.product_comparison}
                cx="50%"
                cy="50%"
                labelLine={false}
                label={({ final_product, total_area }) => `${final_product}: ${total_area?.toFixed(1)} га`}
                outerRadius={120}
                fill="#8884d8"
                dataKey="total_area"
              >
                {data.product_comparison.map((entry, index) => (
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

  const renderVarietyComparison = () => {
    if (!data?.variety_comparison?.length) return <div className="text-center text-gray-500 py-8">Нет данных</div>;
    
    return (
      <div className="space-y-6">
        <div className="card">
          <h3 className="text-lg font-medium text-gray-900 mb-4">Урожайность по сортам</h3>
          <ResponsiveContainer width="100%" height={400}>
            <BarChart data={data.variety_comparison}>
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
              <Bar dataKey="avg_yield" fill="#82CA9D" name="Средняя урожайность (ц/га)" />
            </BarChart>
          </ResponsiveContainer>
        </div>
      </div>
    );
  };

  const tabs = [
    { id: 'fields', name: 'По полям', icon: BarChart3 },
    { id: 'years', name: 'По годам', icon: TrendingUp },
    { id: 'products', name: 'По конечным продуктам', icon: PieChartIcon },
    { id: 'varieties', name: 'По сортам', icon: BarChart3 },
  ];

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold text-gray-900">Сравнительный отчет по урожайности</h1>
          <p className="mt-1 text-sm text-gray-500">
            Сравнение урожайности по различным параметрам
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
        <div className="grid grid-cols-1 gap-4 sm:grid-cols-2 lg:grid-cols-3">
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
            <label className="label">Сорт</label>
            <input
              type="text"
              className="input"
              placeholder="Название сорта"
              value={filters.variety}
              onChange={(e) => handleFilterChange('variety', e.target.value)}
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

      {/* Summary */}
      {data && (
        <div className="card bg-blue-50 border-blue-200">
          <h3 className="text-lg font-medium text-blue-900 mb-2">Сводка</h3>
          <p className="text-blue-700">
            Всего обработано записей: <strong>{data.total_records}</strong>
          </p>
        </div>
      )}

      {/* Tabs */}
      <div className="border-b border-gray-200">
        <nav className="-mb-px flex space-x-8">
          {tabs.map((tab) => (
            <button
              key={tab.id}
              onClick={() => setActiveTab(tab.id)}
              className={`flex items-center py-2 px-1 border-b-2 font-medium text-sm ${
                activeTab === tab.id
                  ? 'border-primary-500 text-primary-600'
                  : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
              }`}
            >
              <tab.icon className="h-4 w-4 mr-2" />
              {tab.name}
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
          {activeTab === 'fields' && renderFieldComparison()}
          {activeTab === 'years' && renderYearComparison()}
          {activeTab === 'products' && renderProductComparison()}
          {activeTab === 'varieties' && renderVarietyComparison()}
        </div>
      )}
    </div>
  );
};

