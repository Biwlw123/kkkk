from django.urls import path
from .views import CustomLoginView, signup, profile_view, profile_edit, car_detail, ai_list, service_list
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='logout.html'), name='logout'),
    path('signup/', signup, name='signup'),
    path('profile/', profile_view, name='profile_view'),
    path('profile/edit/', profile_edit, name='profile_edit'),
    path('ai/', ai_list, name='ai_list'),
]