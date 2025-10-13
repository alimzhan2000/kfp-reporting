from django.urls import path
from . import views

urlpatterns = [
    path('data/', views.AgriculturalDataListView.as_view(), name='agricultural_data_list'),
    path('yield-comparison/', views.yield_comparison_report, name='yield_comparison_report'),
    path('field-efficiency/', views.field_efficiency_report, name='field_efficiency_report'),
    path('variety-performance/', views.variety_performance_report, name='variety_performance_report'),
    path('templates/', views.report_templates, name='report_templates'),
    path('dashboard-stats/', views.dashboard_stats, name='dashboard_stats'),
    path('simple-test/', views.simple_test, name='simple_test'),
]


