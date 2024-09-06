from django.urls import path
from .views import add_company, filter_companies, home, update_choices, signup, toggle_favorite, logout_view, add_favorite, search_companies, favorite_list, set_preference, add_edit_note, CompanyUpdateView, CompanyDeleteView, CompanyDetailView, CompanyListView
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('', home, name='home'),
    path('signup/', signup, name='signup'),
    path('login/', auth_views.LoginView.as_view(template_name='app/login.html'), name='login'),
    path('logout/', logout_view, name='logout'),
    path('add_company/', add_company, name='add_company'),
    path('search/', search_companies, name='search_company'),
    path('filter/', filter_companies, name='filter_companies'),
    path('update_choices/', update_choices, name='update_choices'),
    path('company/<int:pk>/', CompanyDetailView.as_view(), name='company_detail'),
    path('companies/', CompanyListView.as_view(), name='company_list'),
    path('company/<int:pk>/toggle_favorite/', toggle_favorite, name='toggle_favorite'),
    path('add_favorite/<int:company_id>/', add_favorite, name='add_favorite'),
    path('favorites/', favorite_list, name='favorite_list'),
    path('search/', search_companies, name='search_companies'),
    path('set_preference/', set_preference, name='set_preference'),
    path('company/<int:company_id>/note/', add_edit_note, name='add_edit_note'),
    path('company/<int:pk>/edit/', CompanyUpdateView.as_view(), name='company_edit'),
    path('company/<int:pk>/delete/', CompanyDeleteView.as_view(), name='company_delete'),
]
