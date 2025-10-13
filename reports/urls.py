from django.urls import path
from . import views
from . import simple_views

urlpatterns = [
    path('data/', views.AgriculturalDataListView.as_view(), name='agricultural_data_list'),
    path('yield-comparison/', views.yield_comparison_report, name='yield_comparison_report'),
    path('field-efficiency/', views.field_efficiency_report, name='field_efficiency_report'),
    path('variety-performance/', views.variety_performance_report, name='variety_performance_report'),
    path('templates/', views.report_templates, name='report_templates'),
    path('dashboard-stats/', views.dashboard_stats, name='dashboard_stats'),
    path('simple-test/', views.simple_test, name='simple_test'),
    path('simple-dashboard-stats/', simple_views.simple_dashboard_stats, name='simple_dashboard_stats'),
    path('simple-test-view/', simple_views.simple_test_view, name='simple_test_view'),
    path('simple-yield-comparison/', simple_views.simple_yield_comparison, name='simple_yield_comparison'),
    path('simple-field-efficiency/', simple_views.simple_field_efficiency, name='simple_field_efficiency'),
    path('simple-variety-performance/', simple_views.simple_variety_performance, name='simple_variety_performance'),
    path('simple-users-list/', simple_views.simple_users_list, name='simple_users_list'),
    path('simple-database-status/', simple_views.simple_database_status, name='simple_database_status'),
    path('simple-force-initialize/', simple_views.simple_force_initialize_database, name='simple_force_initialize_database'),
]


