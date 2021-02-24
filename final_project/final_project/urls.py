"""final_project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import path, include
from savings_app.views import (
                        LandingPageView,
                        ExpensesListFormView,
                        UserProfileView,
                        AddUserView,
                        AddBudgetFormView,
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),
    path('accounts/profile/', UserProfileView.as_view(), name='profile-view'),
    path('/accounts/logout/', auth_views.LogoutView.as_view(template_name='logout.html'), name='logout'),
    path('', LandingPageView.as_view(), name='landing-page'),
    path('/add_user/', AddUserView.as_view(), name='add-user'),
    # path('periods/', PeriodsListView.as_view(), name='periods-list'),
    path('expenses/', ExpensesListFormView.as_view(), name='expense-list-form'),
    path('budget-add/', AddBudgetFormView.as_view(), name='budget-add'),
]


