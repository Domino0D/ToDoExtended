from django.urls import path
from . import views
from .views import Tasklist, TaskCreate, TaskUpdate, TaskDelete, CustomLoginView, RegisterPage
from django.contrib.auth.views import LogoutView
urlpatterns = [
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', views.logoutUser, name='logout'),
    path('register/', RegisterPage.as_view(), name='register'),
    
    path('', Tasklist.as_view(), name="tasks"),
    path('task-create/', TaskCreate.as_view(), name="task-create"),
    path('task-update/<int:pk>/', TaskUpdate.as_view(), name="task-update"),     
    path('task-delete/<int:pk>/', TaskDelete.as_view(), name="task-delete"),
    path('tasks/user/<str:username>/', Tasklist.as_view(), name='user-tasks'), 
     
    ]
