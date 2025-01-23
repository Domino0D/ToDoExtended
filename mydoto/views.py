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
    template_name = "mydoto/login.html"
    fields = '__all__'
    redirect_authenticated_user = True
    
    def get_success_url(self):
        return reverse_lazy('tasks')
    

class RegisterPage(FormView):
    template_name = 'mydoto/register.html'
    form_class = UserCreationForm
    redirect_authenticated_user = True
    success_url = reverse_lazy('tasks')
    
    def form_valid(self, form):
        user = form.save()
        if user is not None:
            login(self.request, user)
        return super(RegisterPage, self).form_valid(form)
    
    def get(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect('tasks')
        return super(RegisterPage, self).get(*args, **kwargs)
        
        

class UserlistView(LoginRequiredMixin, ListView):
    model = Task
    context_object_name = 'users'
    template_name = 'mydoto/user_profile.html'
    
    def get_queryset(self):
        return User.objects.all
    
    
    
def logoutUser(request):
    logout(request)
    return redirect('tasks')



    
class Tasklist(LoginRequiredMixin, ListView):
    model = Task
    context_object_name = 'tasks'
    template_name = 'mydoto/task_list.html'

    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        username = self.kwargs.get('username')
                
                
        search_input_user = self.request.GET.get('search-area-user', '') 
        
        users = User.objects.exclude(id=self.request.user.id)
        if search_input_user:
            users = users.filter(username__icontains=search_input_user)
        context['all_users'] = users
            
        if username:
            try:
                viewed_user = User.objects.get(username=username)
                if viewed_user.profile.is_private:
                    context['private'] = True  # Rzuć wyjątek, jeśli profil jest prywatny
                else:
                    context['private'] = False
            except User.DoesNotExist:
                raise Http404('user does not exist', {username})
        else:
            viewed_user = self.request.user
        
        if viewed_user == self.request.user:
            context['private'] = False        
            
        context['viewed_user'] = viewed_user
            
        context['tasks'] = Task.objects.filter(user=viewed_user)
        
        filter_tasks = self.request.GET.get('tasks_filter', '')
        
        if filter_tasks == "completed":
            context['tasks'] = context['tasks'].filter(complete=True)
        elif filter_tasks == "incomplete":
            context['tasks'] = context['tasks'].filter(complete=False)
        elif filter_tasks == "OldToNew":
            context['tasks'] = context['tasks'].order_by('-complete')
        elif filter_tasks == "NewToOld":
            context['tasks'] = context['tasks'].order_by('complete')
        elif filter_tasks == "NewCompleted":
            context['tasks'] = context['tasks'].order_by('create').filter(complete=True)
        elif filter_tasks == "OldComplete":
            context['tasks'] = context['tasks'].order_by('-create').filter(complete=True)
        # elif filter_tasks == "NewUnCompleted":
        #     context['tasks'] = context['tasks'].order_by('create').filter(complete=False)
        # elif filter_tasks == "OldUnComplete":
        #     context['tasks'] = context['tasks'].filter(complete=False).order_by('create')  # Nieukończone, od najstarszych           
            
        context['is_own_tasks'] = (viewed_user == self.request.user)
        
        
        search_input = self.request.GET.get('search-area', '')
        
        if search_input:
            context['tasks'] = context['tasks'].filter(title__icontains=search_input)

        context['count'] = context['tasks'].filter(complete=False).count
                        
        profile, created = Profile.objects.get_or_create(user=self.request.user) 
        context['profile_form'] = ProfileForm(instance=profile)

        return context
    
    def post(self, request, *args, **kwargs):
        profile, created = Profile.objects.get_or_create(user=request.user)
        form = ProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
        return redirect('tasks')  
            
        

        
class TaskDetail(LoginRequiredMixin, DetailView):
    model = Task
    context_object_name = 'task'
    template_name = 'mydoto/task.html'
    

class TaskCreate(LoginRequiredMixin, CreateView):
    model = Task
    fields = ['title', 'description', 'complete']
    success_url = reverse_lazy('tasks')
    
    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(TaskCreate, self).form_valid(form)
        
    
class TaskUpdate(LoginRequiredMixin, UpdateView):
    model = Task
    fields = ['title', 'description', 'complete']
    success_url = reverse_lazy('tasks')
    
    

class TaskDelete(DeleteView):
    model = Task
    context_object_name = 'task'
    success_url = reverse_lazy('tasks')
    
  
# class Tasklist(LoginRequiredMixin, ListView):
#     model = Task
#     context_object_name = 'tasks'
#     template_name = 'mydoto/task_list.html'

    
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         username = self.kwargs.get('username')
                
#         search_input_user = self.request.GET.get('search-area-user', '') 
        
#         users = User.objects.exclude(id=self.request.user.id)
#         if search_input_user:
#             users = users.filter(username__icontains=search_input_user)
#         context['all_users'] = users
            
#         if username:
#             try:
#                 viewed_user = User.objects.get(username=username)
#             except:
#                 raise Http404('user does not exist', {username})
#         else:
#             viewed_user = self.request.user
            
            
#         context['viewed_user'] = viewed_user
#         context['tasks'] = Task.objects.filter(user=viewed_user)
#         context['is_own_tasks'] = (viewed_user == self.request.user)
        
        
#         search_input = self.request.GET.get('search-area', '')
        
#         if search_input:
#             context['tasks'] = context['tasks'].filter(title__icontains=search_input)
        
#         context['count'] = context['tasks'].filter(complete=False).count
                        
#         profile, created = Profile.objects.get_or_create(user=self.request.user) 
#         context['profile_form'] = ProfileForm(instance=profile)

#         return context
    
#     def post(self, request, *args, **kwargs):
#         profile, created = Profile.objects.get_or_create(user=request.user)
#         form = ProfileForm(request.POST, instance=profile)
#         if form.is_valid():
#             form.save()
#         return redirect('tasks')  