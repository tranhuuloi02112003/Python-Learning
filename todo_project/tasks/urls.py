

from django.urls import path

from . import views
urlpatterns = [
    path('', views.home_page, name = 'home'),
    path('delete/<int:pk>/',views.delete_task, name ='delete_task'),
    path('edit/<int:pk>/',views.edit_task, name = 'edit_task'),
    path('toggle/<int:pk>/',views.toggle_task, name = 'toggle_task'),
    path('create-project/', views.create_project, name = 'create_project'),
]