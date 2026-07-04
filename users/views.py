from django.contrib import messages
from django.contrib.auth import views as auth_views
from django.contrib.auth.models import User
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import redirect
from django.urls import reverse, reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views.generic import CreateView, DeleteView, ListView, UpdateView

from .forms import UserRegistrationForm, UserUpdateForm


class UserListView(ListView):
    model = User
    template_name = 'users/list.html'
    context_object_name = 'users'
    ordering = ['date_joined']


class UserCreateView(SuccessMessageMixin, CreateView):
    model = User
    form_class = UserRegistrationForm
    template_name = 'users/create.html'
    success_url = reverse_lazy('login')
    success_message = _('Пользователь успешно зарегистрирован')


class UserUpdateView(SuccessMessageMixin, UpdateView):
    model = User
    form_class = UserUpdateForm
    template_name = 'users/update.html'
    success_url = reverse_lazy('users_list')
    success_message = _('Пользователь успешно изменен')

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect(f'{reverse("login")}?next={request.path}')
        if request.user != self.get_object():
            messages.error(request, _('У вас нет прав для изменения'))
            return redirect('users_list')
        return super().dispatch(request, *args, **kwargs)


class UserDeleteView(SuccessMessageMixin, DeleteView):
    model = User
    template_name = 'users/delete.html'
    success_url = reverse_lazy('users_list')
    success_message = _('Пользователь успешно удален')

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect(f'{reverse("login")}?next={request.path}')
        if request.user != self.get_object():
            messages.error(request, _('У вас нет прав для изменения'))
            return redirect('users_list')
        return super().dispatch(request, *args, **kwargs)


class UserLoginView(SuccessMessageMixin, auth_views.LoginView):
    template_name = 'registration/login.html'
    success_message = _('Вы залогинены')


class UserLogoutView(auth_views.LogoutView):
    next_page = '/'

    def post(self, request, *args, **kwargs):
        messages.success(request, _('Вы разлогинены'))
        return super().post(request, *args, **kwargs)
