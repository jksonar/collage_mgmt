from django.urls import path
from . import views

app_name = 'students'

urlpatterns = [
    path('', views.student_list, name='student_list'),
    path('register/', views.student_registration, name='student_registration'),
    path('profile/<int:user_id>/', views.student_profile, name='student_profile'),
    path('enroll/<int:user_id>/', views.student_enrollment, name='student_enrollment'),
] 