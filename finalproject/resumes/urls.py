from django.urls import path
from . import views

urlpatterns = [
    path('', views.match_candidates, name='match_candidates'),
    path('pdf/<str:filename>/', views.serve_pdf_by_filename, name='serve_pdf_by_filename'),
]
