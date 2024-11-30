# marksheet/urls.py
from django.urls import path
from . import views

app_name = 'marksheet'

urlpatterns = [
    path('', views.homepage, name='homepage'),  # Home page with the form
    path('student/<int:student_id>/', views.student_marksheet, name='student_marksheet'),  # Marksheets page
    path('student/<int:student_id>/download/', views.download_pdf, name='download_pdf'),
]
