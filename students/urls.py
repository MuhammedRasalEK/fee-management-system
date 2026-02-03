from django.urls import path
from . import views

urlpatterns = [
    path('', views.login_view, name='login'),
    path('signup/', views.signup_view, name='signup'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('pay/', views.pay_fee, name='pay_fee'),
    path('report/', views.fee_report, name='report'),
    path('profile/', views.profile_view, name='profile'),
    path('logout/', views.logout_view, name='logout'),
]
