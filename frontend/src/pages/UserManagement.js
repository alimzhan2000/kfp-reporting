import React, { useState, useEffect } from 'react';
import { authAPI } from '../services/api';
import { Users, Plus, Edit, Trash2, UserPlus, Shield, User } from 'lucide-react';
import toast from 'react-hot-toast';

export const UserManagement = () => {
  const [users, setUsers] = useState([]);
  const [loading, setLoading] = useState(true);
  const [showCreateForm, setShowCreateForm] = useState(false);
  const [formData, setFormData] = useState({
    username: '',
    email: '',
    first_name: '',
    last_name: '',
    role: 'management',
    phone: '',
    department: '',
    password: '',
    password_confirm: ''
  });

  useEffect(() => {
    fetchUsers();
  }, []);

  const fetchUsers = async () => {
    setLoading(true);
    try {
      const response = await authAPI.getUserList();
      setUsers(response.data);
    } catch (error) {
      toast.error('Ошибка загрузки пользователей');
      console.error('Ошибка загрузки пользователей:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleInputChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value
    });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    
    if (formData.password !== formData.password_confirm) {
      toast.error('Пароли не совпадают');
      return;
    }

    try {
      await authAPI.createUser(formData);
      toast.success('Пользователь успешно создан');
      setShowCreateForm(false);
      setFormData({
        username: '',
        email: '',
        first_name: '',
        last_name: '',
        role: 'management',
        phone: '',
        department: '',
        password: '',
        password_confirm: ''
      });
      fetchUsers();
    } catch (error) {
      const message = error.response?.data?.message || 'Ошибка создания пользователя';
      toast.error(message);
    }
  };

  const getRoleIcon = (role) => {
    return role === 'admin' ? <Shield className="h-4 w-4" /> : <User className="h-4 w-4" />;
  };

  const getRoleBadge = (role) => {
    return role === 'admin' ? 'badge-warning' : 'badge-success';
  };

  const getRoleText = (role) => {
    return role === 'admin' ? 'Администратор' : 'Руководство';
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
          <h1 className="text-2xl font-bold text-gray-900">Управление пользователями</h1>
          <p className="mt-1 text-sm text-gray-500">
            Создание и управление учетными записями пользователей
          </p>
        </div>
        <button
          onClick={() => setShowCreateForm(true)}
          className="btn-primary"
        >
          <Plus className="h-4 w-4 mr-2" />
          Создать пользователя
        </button>
      </div>

      {/* Create User Form Modal */}
      {showCreateForm && (
        <div className="fixed inset-0 z-50 overflow-y-auto">
          <div className="flex items-center justify-center min-h-screen pt-4 px-4 pb-20 text-center sm:block sm:p-0">
            <div className="fixed inset-0 bg-gray-500 bg-opacity-75 transition-opacity" onClick={() => setShowCreateForm(false)} />
            
            <div className="inline-block align-bottom bg-white rounded-lg text-left overflow-hidden shadow-xl transform transition-all sm:my-8 sm:align-middle sm:max-w-lg sm:w-full">
              <form onSubmit={handleSubmit}>
                <div className="bg-white px-4 pt-5 pb-4 sm:p-6 sm:pb-4">
                  <div className="sm:flex sm:items-start">
                    <div className="mx-auto flex-shrink-0 flex items-center justify-center h-12 w-12 rounded-full bg-primary-100 sm:mx-0 sm:h-10 sm:w-10">
                      <UserPlus className="h-6 w-6 text-primary-600" />
                    </div>
                    <div className="mt-3 text-center sm:mt-0 sm:ml-4 sm:text-left w-full">
                      <h3 className="text-lg leading-6 font-medium text-gray-900 mb-4">
                        Создать нового пользователя
                      </h3>
                      
                      <div className="space-y-4">
                        <div className="grid grid-cols-1 gap-4 sm:grid-cols-2">
                          <div>
                            <label className="label">Имя пользователя *</label>
                            <input
                              type="text"
                              name="username"
                              required
                              className="input"
                              value={formData.username}
                              onChange={handleInputChange}
                            />
                          </div>
                          <div>
                            <label className="label">Email</label>
                            <input
                              type="email"
                              name="email"
                              className="input"
                              value={formData.email}
                              onChange={handleInputChange}
                            />
                          </div>
                        </div>
                        
                        <div className="grid grid-cols-1 gap-4 sm:grid-cols-2">
                          <div>
                            <label className="label">Имя</label>
                            <input
                              type="text"
                              name="first_name"
                              className="input"
                              value={formData.first_name}
                              onChange={handleInputChange}
                            />
                          </div>
                          <div>
                            <label className="label">Фамилия</label>
                            <input
                              type="text"
                              name="last_name"
                              className="input"
                              value={formData.last_name}
                              onChange={handleInputChange}
                            />
                          </div>
                        </div>
                        
                        <div>
                          <label className="label">Роль *</label>
                          <select
                            name="role"
                            required
                            className="input"
                            value={formData.role}
                            onChange={handleInputChange}
                          >
                            <option value="management">Руководство</option>
                            <option value="admin">Администратор</option>
                          </select>
                        </div>
                        
                        <div className="grid grid-cols-1 gap-4 sm:grid-cols-2">
                          <div>
                            <label className="label">Телефон</label>
                            <input
                              type="tel"
                              name="phone"
                              className="input"
                              value={formData.phone}
                              onChange={handleInputChange}
                            />
                          </div>
                          <div>
                            <label className="label">Отдел</label>
                            <input
                              type="text"
                              name="department"
                              className="input"
                              value={formData.department}
                              onChange={handleInputChange}
                            />
                          </div>
                        </div>
                        
                        <div className="grid grid-cols-1 gap-4 sm:grid-cols-2">
                          <div>
                            <label className="label">Пароль *</label>
                            <input
                              type="password"
                              name="password"
                              required
                              className="input"
                              value={formData.password}
                              onChange={handleInputChange}
                            />
                          </div>
                          <div>
                            <label className="label">Подтверждение пароля *</label>
                            <input
                              type="password"
                              name="password_confirm"
                              required
                              className="input"
                              value={formData.password_confirm}
                              onChange={handleInputChange}
                            />
                          </div>
                        </div>
                      </div>
                    </div>
                  </div>
                </div>
                
                <div className="bg-gray-50 px-4 py-3 sm:px-6 sm:flex sm:flex-row-reverse">
                  <button
                    type="submit"
                    className="btn-primary sm:ml-3 sm:w-auto"
                  >
                    Создать
                  </button>
                  <button
                    type="button"
                    onClick={() => setShowCreateForm(false)}
                    className="btn-outline mt-3 sm:mt-0 sm:w-auto"
                  >
                    Отмена
                  </button>
                </div>
              </form>
            </div>
          </div>
        </div>
      )}

      {/* Users List */}
      <div className="card">
        <div className="overflow-x-auto">
          <table className="table">
            <thead>
              <tr>
                <th>Пользователь</th>
                <th>Email</th>
                <th>Роль</th>
                <th>Телефон</th>
                <th>Отдел</th>
                <th>Действия</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-gray-200">
              {users.map((user) => (
                <tr key={user.id}>
                  <td>
                    <div className="flex items-center">
                      <div className="h-10 w-10 rounded-full bg-primary-600 flex items-center justify-center">
                        <span className="text-sm font-medium text-white">
                          {user.first_name?.[0] || user.username?.[0] || 'U'}
                        </span>
                      </div>
                      <div className="ml-4">
                        <div className="text-sm font-medium text-gray-900">
                          {user.first_name} {user.last_name}
                        </div>
                        <div className="text-sm text-gray-500">
                          @{user.username}
                        </div>
                      </div>
                    </div>
                  </td>
                  <td className="text-sm text-gray-900">
                    {user.email || '-'}
                  </td>
                  <td>
                    <div className="flex items-center">
                      {getRoleIcon(user.role)}
                      <span className={`ml-2 ${getRoleBadge(user.role)}`}>
                        {getRoleText(user.role)}
                      </span>
                    </div>
                  </td>
                  <td className="text-sm text-gray-900">
                    {user.phone || '-'}
                  </td>
                  <td className="text-sm text-gray-900">
                    {user.department || '-'}
                  </td>
                  <td>
                    <div className="flex space-x-2">
                      <button className="text-primary-600 hover:text-primary-800" title="Редактировать">
                        <Edit className="h-4 w-4" />
                      </button>
                      <button className="text-red-600 hover:text-red-800" title="Удалить">
                        <Trash2 className="h-4 w-4" />
                      </button>
                    </div>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>

      {/* Summary Stats */}
      <div className="grid grid-cols-1 gap-5 sm:grid-cols-2 lg:grid-cols-3">
        <div className="card">
          <div className="flex items-center">
            <div className="flex-shrink-0">
              <Users className="h-8 w-8 text-blue-500" />
            </div>
            <div className="ml-5 w-0 flex-1">
              <dl>
                <dt className="text-sm font-medium text-gray-500 truncate">Всего пользователей</dt>
                <dd className="text-lg font-medium text-gray-900">{users.length}</dd>
              </dl>
            </div>
          </div>
        </div>
        
        <div className="card">
          <div className="flex items-center">
            <div className="flex-shrink-0">
              <Shield className="h-8 w-8 text-yellow-500" />
            </div>
            <div className="ml-5 w-0 flex-1">
              <dl>
                <dt className="text-sm font-medium text-gray-500 truncate">Администраторы</dt>
                <dd className="text-lg font-medium text-gray-900">
                  {users.filter(u => u.role === 'admin').length}
                </dd>
              </dl>
            </div>
          </div>
        </div>
        
        <div className="card">
          <div className="flex items-center">
            <div className="flex-shrink-0">
              <User className="h-8 w-8 text-green-500" />
            </div>
            <div className="ml-5 w-0 flex-1">
              <dl>
                <dt className="text-sm font-medium text-gray-500 truncate">Руководство</dt>
                <dd className="text-lg font-medium text-gray-900">
                  {users.filter(u => u.role === 'management').length}
                </dd>
              </dl>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

