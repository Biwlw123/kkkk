from django.urls import path
from .views import car_data_edit, add_car, car_quiz, car_page, car_list, delete_car
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('cars/<int:car_id>/edit', car_data_edit, name='car_data_edit'),
    path('cars/add', add_car, name='add_car'),
    path('cars/<int:car_id>/quiz', car_quiz, name='car_quiz'),
    path('cars/<int:car_id>', car_page, name='car_page'),
    path('cars/', car_list, name='car_list'),
    path('cars/delete/<int:car_id>/', delete_car, name='delete_car'),
]
