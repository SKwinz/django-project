from django.urls import path

from . import views

app_name = 'polls'
urlpatterns = [
    path('', views.index, name='index'),
    path('<int:question_id>/', views.detail, name='detail'),
    path('<int:question_id>/results/', views.results, name='results'),
    path('<int:question_id>/vote/', views.vote, name='vote'),
    path('questions/', views.get_questions),
    path('choices/', views.get_choices),
    path('projects/', views.get_projects),
    path('employees/', views.get_employees),
]