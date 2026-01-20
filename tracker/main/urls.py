from django.urls import path
from .views import *


urlpatterns = [
    path('', HomeListView.as_view(), name='home'),
    path('tasks/', TasksListView.as_view(), name='task'),
    path('tasks/add/', TaskAddView.as_view(), name='task_add'),
    path('habits/', HabitsListView.as_view(), name='habit'),
    path('habits/add/', HabitsAddView.as_view(), name='habit_add'),
    path('habits/<str:slug>/', HabitsDetailView.as_view(), name='habit_detail'),
    path('login/', UserLoginView.as_view(), name='login'),
    path('logout/', UserLogoutView.as_view(), name='logout'),
    path('signup/', UserSignUpView.as_view(), name='signup'),
    path('task/<str:slug>/', TaskDetailView.as_view(), name='task_detail'),
    path('habit/<str:slug>/done/', HabitMarkDoneView.as_view(), name='habit_mark_done'),

]