from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView
from .forms import *
from .models import *
from django.views.generic import ListView, DetailView, CreateView
from django.utils import timezone
from datetime import timedelta



class HomeListView(LoginRequiredMixin, ListView):
    model = Task
    template_name = 'main/home.html'
    context_object_name = 'tasks'
    paginate_by = 7
    form_class = TaskFilterForm

    def get_queryset(self):
        queryset = Task.objects.filter(user=self.request.user)

        form = self.form_class(self.request.GET)
        if form.is_valid():
            cd = form.cleaned_data

            if cd.get('search'):
                queryset = queryset.filter(title__icontains=cd['search'])

            if cd.get('status'):
                queryset = queryset.filter(status=cd['status'])

            if cd.get('sort'):
                queryset = queryset.order_by(cd['sort'])

        return queryset

    def get_habit_progress(self, user):
        week_ago = timezone.now().date() - timedelta(days=7)

        total = HabitLog.objects.filter(
            habit__user=user,
            date__gte=week_ago
        ).count()

        done = HabitLog.objects.filter(
            habit__user=user,
            date__gte=week_ago,
            is_done=True
        ).count()

        if total == 0:
            return 0

        return int(done / total * 100)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        user = self.request.user

        context['title'] = 'Главная страница'
        # форма
        context['form'] = self.form_class(self.request.GET)

        # активные привычки
        context['habits'] = Habit.objects.filter(
            user=user,
            is_active=True
        )

        # ближайшие дедлайны (например 5)
        context['near_deadlines'] = Task.objects.filter(
            user=user,
            status__in=['Todo', 'In_progress']
        ).order_by('deadline')[:5]

        # процент выполнения привычек за неделю
        context['habit_progress'] = self.get_habit_progress(user)

        return context


class TasksListView(LoginRequiredMixin, ListView):
    model = Task
    template_name = 'main/tasks.html'
    context_object_name = 'tasks'
    paginate_by = 7
    form_class = TaskFilterForm

    def get_queryset(self):
        queryset = Task.objects.filter(
            user=self.request.user
        )
        form = self.form_class(
            self.request.GET
        )
        if form.is_valid():
            cd = form.cleaned_data
            if cd.get('search'):
                queryset = queryset.filter(title__icontains=cd['search'])

            if cd.get('status'):
                queryset = queryset.filter(status=cd['status'])

            if cd.get('sort'):
                queryset = queryset.order_by(cd['sort'])

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['form'] = self.form_class(self.request.GET)
        context['title'] = 'Задачи'

        return context

