from django.urls import path
from .views import add_company, search_company, filter_companies, view_choices, home, company_list, update_choices, CompanyDetailView 

urlpatterns = [
    path('', home, name='home'),
    path('add/', add_company, name='add_company'),
    path('search/', search_company, name='search_company'),
    path('filter/', filter_companies, name='filter_companies'),
    path('choices/', view_choices, name='view_choices'), 
    path('companies/', company_list, name='company_list'),
    path('company/<int:pk>/', CompanyDetailView.as_view(), name='company_detail'),
    path('update_choices/', update_choices, name='update_choices'),
]
