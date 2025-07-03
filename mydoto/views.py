from django.db.models.query import QuerySet
from django.shortcuts import render, redirect
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormView
from django.urls import reverse_lazy
from django.contrib.auth.views import LoginView

from django.contrib.auth.mixins import LoginRequiredMixin

from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login

from django.contrib.auth.models import User
from django.http import Http404

from . models import Task
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, logout

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .forms import ProfileForm

from .models import Profile  # Dodaj ten import
# Create your views here.

class CustomLoginView(LoginView):
    template_name = "mydoto/login.html"  # Template for login page
    fields = '__all__'  # Use all fields 
    redirect_authenticated_user = True  # Redirect logged-in users away from login page
    
    def get_success_url(self):
        return reverse_lazy('tasks')  # Redirect to 'tasks' page after successful login
    

class RegisterPage(FormView):
    template_name = 'mydoto/register.html'  # Template for registration page
    form_class = UserCreationForm  # Use default user creation form
    redirect_authenticated_user = True  # Redirect logged-in users away from register page
    success_url = reverse_lazy('tasks')  # Redirect to 'tasks' after successful registration
    
    def form_valid(self, form):
        user = form.save()  # Save new user from form data
        if user is not None:
            login(self.request, user)  # Log in the new user
        return super(RegisterPage, self).form_valid(form)  # Continue with normal form_valid processing
    
    def get(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect('tasks')  # Redirect logged-in users to 'tasks' page
        return super(RegisterPage, self).get(*args, **kwargs)  # Otherwise, show registration form
        
    
def logoutUser(request):
    logout(request)  # Log out the current user
    return redirect('tasks')  # Redirect to 'tasks' page

class Tasklist(LoginRequiredMixin, ListView):
    model = Task  # Model to list
    context_object_name = 'tasks'  # Variable name in template
    template_name = 'mydoto/task_list.html'  # Template for task list

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)  # Get default context
        username = self.kwargs.get('username')  # Get username from URL kwargs
                
        search_input_user = self.request.GET.get('search-area-user', '')  # Get user search input from GET params
        
        users = User.objects.exclude(id=self.request.user.id)  # Get all users except current user
        if search_input_user:
            users = users.filter(username__icontains=search_input_user)  # Filter users by username contains search input
        context['all_users'] = users  # Add filtered users to context
            
        if username:
            try:
                viewed_user = User.objects.get(username=username)  # Get user by username from URL
                if viewed_user.profile.is_private:
                    context['private'] = True  # Mark profile as private
                else:
                    context['private'] = False  # Profile is not private
            except User.DoesNotExist:
                raise Http404('user does not exist', {username})  # Raise 404 if user not found
        else:
            viewed_user = self.request.user  # Default to current user
        
        if viewed_user == self.request.user:
            context['private'] = False  # Own profile is not private
        
        context['viewed_user'] = viewed_user  # Add viewed user to context
            
        context['tasks'] = Task.objects.filter(user=viewed_user)  # Get tasks for viewed user
        
        filter_tasks = self.request.GET.get('tasks_filter', '')  # Get task filter from GET params
        
        if filter_tasks == "completed":
            context['tasks'] = context['tasks'].filter(complete=True)  # Filter completed tasks
        elif filter_tasks == "incomplete":
            context['tasks'] = context['tasks'].filter(complete=False)  # Filter incomplete tasks
        elif filter_tasks == "OldToNew":
            context['tasks'] = context['tasks'].order_by('-complete')  # Order tasks by complete descending (likely incorrect)
        elif filter_tasks == "NewToOld":
            context['tasks'] = context['tasks'].order_by('complete')  # Order tasks by complete ascending (likely incorrect)
        elif filter_tasks == "NewCompleted":
            context['tasks'] = context['tasks'].order_by('create').filter(complete=True)  # New completed tasks
        elif filter_tasks == "OldComplete":
            context['tasks'] = context['tasks'].order_by('-create').filter(complete=True)  # Old completed tasks       
            
        context['is_own_tasks'] = (viewed_user == self.request.user)  # Boolean if viewing own tasks
        
        search_input = self.request.GET.get('search-area', '')  # Get task search input
        
        if search_input:
            context['tasks'] = context['tasks'].filter(title__icontains=search_input)  # Filter tasks by title contains
        
        context['count'] = context['tasks'].filter(complete=False).count  # Count incomplete tasks (missing parentheses)
                        
        profile, created = Profile.objects.get_or_create(user=self.request.user)  # Get or create profile for current user
        context['profile_form'] = ProfileForm(instance=profile)  # Add profile form to context

        return context
    
    def post(self, request, *args, **kwargs):
        profile, created = Profile.objects.get_or_create(user=request.user)  # Get or create profile
        form = ProfileForm(request.POST, instance=profile)  # Bind form with POST data
        if form.is_valid():
            form.save()  # Save profile changes
        return redirect('tasks')  # Redirect to tasks page after POST            
class TaskCreate(LoginRequiredMixin, CreateView):
    model = Task  # Model to create
    fields = ['title', 'description', 'complete']  # Fields to show in form
    success_url = reverse_lazy('tasks')  # Redirect after successful creation
    
    def form_valid(self, form):
        form.instance.user = self.request.user  # Assign current user as task owner
        return super(TaskCreate, self).form_valid(form)  # Continue with normal form_valid
    

class TaskUpdate(LoginRequiredMixin, UpdateView):
    model = Task  # Model to update
    fields = ['title', 'description', 'complete']  # Fields to update
    success_url = reverse_lazy('tasks')  # Redirect after successful update

class TaskDelete(DeleteView):
    model = Task  # Model to delete
    context_object_name = 'task'  # Variable name in template
    success_url = reverse_lazy('tasks')  # Redirect after successful deletion
  