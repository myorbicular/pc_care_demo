from django.urls import path
from . import views

app_name = 'quizapp'

urlpatterns = [
    path('', views.index, name='index'),
    path('create_customer/', views.create_customer, name='create_customer'),
    path('skin_quiz/', views.skin_quiz, name='skin_quiz'),
    path('skin_concerns/<str:user_name>/', views.skin_concerns, name='skin_concerns'),
    path('quiz_answers/', views.quiz_answers, name='quiz_answers'),
    path('products/<str:user_name>/', views.products, name='products'),
    path('water_info/',views.water_info),
]
