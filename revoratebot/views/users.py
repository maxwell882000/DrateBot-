from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.list import ListView
from django.views.generic.edit import DeleteView
from django.views.generic import FormView, DetailView
from revoratebot.models import User, Department, Company
from revoratebot.forms import CreateUserForm
from django.urls import reverse, reverse_lazy
from django.contrib import messages
from core.managers import companies, users, ratings
from django.http import Http404
from bot import telegram_bot


class UsersListView(LoginRequiredMixin, ListView):
    ordering = 'created_at'
    model = User
    template_name = 'admin/users/users_list.html'
    context_object_name = 'users'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['companies'] = companies.get_all_companies()
        context['departments'] = companies.get_all_departments()
        return context


class CreateUserView(LoginRequiredMixin, FormView):
    form_class = CreateUserForm
    template_name = 'admin/users/new_user.html'

    def form_valid(self, form):
        name = form.cleaned_data['name']
        phone_number = form.cleaned_data['phone_number']
        is_manager = form.cleaned_data['is_manager']
        department = form.cleaned_data['department']
        company = form.cleaned_data['company']
        if not is_manager:
            if company == '' or company.isspace():
                form.add_error('company', 'Вы не указали компанию')
                return super().form_invalid(form)
            if department == '' or department.isspace():
                form.add_error('department', 'Вы не указали отделение')
                return super().form_invalid(form)
        try:
            user = users.create_user(name, phone_number, company, department, is_manager)
        except Company.DoesNotExist:
            messages.error(self.request, "Указанная компания не существует, проверьте свой выбор")
            return super().form_invalid(form)
        except Department.DoesNotExist:
            messages.error(self.request, "Указан не существующий отдел в выбранной компании, проверьте свой выбор")
            return super().form_invalid(form)
        except Exception as e:
            messages.error(self.request, 'Произошла ошибка: ' + str(e))
            return super().form_invalid(form)
        self.object = user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('admin_user_created', kwargs={'pk': self.object.id})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['companies'] = companies.get_all_companies()
        context['departments'] = companies.get_all_departments()
        return context


class UserCreatedView(LoginRequiredMixin, DetailView):
    model = User
    template_name = 'admin/users/user_created.html'
    context_object_name = 'user'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['bot_username'] = telegram_bot.get_me().username
        return context


class EditUserView(LoginRequiredMixin, FormView):
    form_class = CreateUserForm
    success_url = reverse_lazy('admin_users')
    template_name = 'admin/users/edit_user.html'

    def get(self, request, *args, **kwargs):
        user_id = kwargs.get('pk')
        user = users.get_by_id(user_id)
        if not user:
            raise Http404()
        self.object = user
        if not user.is_manager:
            self.company = user.department.company
        else:
            self.company = None
        return super().get(request, *args, **kwargs)

    def get_initial(self):
        user = self.object
        initial = super().get_initial()
        initial['name'] = user.name
        initial['phone_number'] = user.phone_number
        if not user.is_manager:
            initial['company'] = user.department.company_id or ''
            initial['department'] = user.department_id or ''
        else:
            initial['company'] = ''
            initial['department'] = ''
        initial['is_manager'] = user.is_manager
        return initial

    def post(self, request, *args, **kwargs):
        user = users.get_by_id(kwargs.get('pk'))
        if not user:
            raise Http404()
        self.object = user
        if not user.is_manager:
            self.company = user.department.company
        else:
            self.company = None
        return super().post(request, args, kwargs)

    def form_valid(self, form):
        name = form.cleaned_data['name']
        phone_number = form.cleaned_data['phone_number']
        is_manager = form.cleaned_data['is_manager']
        department = form.cleaned_data['department']
        company = form.cleaned_data['company']
        if not is_manager:
            if company == '' or company.isspace():
                form.add_error('company', 'Вы не указали компанию')
                return super().form_invalid(form)
            if department == '' or department.isspace():
                form.add_error('department', 'Вы не указали отделение')
                return super().form_invalid(form)

        try:
            user = users.edit_user(self.object.id, name, phone_number, company, department, is_manager)
        except Company.DoesNotExist:
            messages.error(self.request, "Указанная компания не существует, проверьте свой выбор")
            return super().form_invalid(form)
        except Department.DoesNotExist:
            messages.error(self.request, "Указан не существующий отдел в выбранной компании, проверьте свой выбор")
            return super().form_invalid(form)
        except Exception as e:
            messages.error(self.request, 'Произошла ошибка: ' + str(e))
            return super().form_invalid(form)
        if user.is_manager:
            success_message = "Менеджер %s изменён" % user.name
        else:
            success_message = "Пользователь %s из отдела %s компании %s изменён" % (user.name, user.department.name, user.department.company.name)
        messages.success(self.request, success_message)
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['companies'] = companies.get_all_companies()
        context['departments'] = companies.get_all_departments()
        context['user_id'] = self.object.id
        if self.company:
            context['current_departments'] = self.company.department_set.all()
        return context


class DeleteUserView(LoginRequiredMixin, DeleteView):
    model = User
    success_url = reverse_lazy('admin_users')

    def delete(self, request, *args, **kwargs):
        user = self.get_object()
        user_id = user.id
        user_name = user.name
        result = super().delete(request, *args, **kwargs)
        ratings.delete_users_ratings(user_id)
        messages.success(request, 'Пользователь %s и всего его рейтинги удалены!' % user_name)
        return result
