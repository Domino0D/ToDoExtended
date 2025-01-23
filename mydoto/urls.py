from django.urls import path
from . import views
from .views import Tasklist, TaskDetail, TaskCreate, TaskUpdate, TaskDelete, CustomLoginView, RegisterPage, UserlistView
from django.contrib.auth.views import LogoutView
urlpatterns = [
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', views.logoutUser, name='logout'),
    path('register/', RegisterPage.as_view(), name='register'),
    path('user_profile/', UserlistView.as_view(), name='UsersList'), 
    # path('edit-profile/', EditProfileView.as_view(), name='edit_profile'), 
    # path('edit-profile/', views.edit_profile, name='edit_profile'),
    
    path('', Tasklist.as_view(), name="tasks"),
    path('task/<int:pk>/', TaskDetail.as_view(), name="task"),
    path('user_profile/<int:pk>/', UserlistView.as_view(), name="UsersProf"),
    path('task-create/', TaskCreate.as_view(), name="task-create"),
    path('task-update/<int:pk>/', TaskUpdate.as_view(), name="task-update"),     
    path('task-delete/<int:pk>/', TaskDelete.as_view(), name="task-delete"),
    path('tasks/user/<str:username>/', Tasklist.as_view(), name='user-tasks'), 
     
    ]
