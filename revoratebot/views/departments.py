from django.views.generic.edit import CreateView, DeleteView, ModelFormMixin
from django.views.generic.list import ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy, reverse
from django.contrib import messages
from revoratebot.models import Department, User
from django.http import Http404

from core.managers import companies


class CreateDepartmentView(LoginRequiredMixin, CreateView):
    model = Department
    fields = ['name']
    template_name = 'admin/departments/new_department.html'

    def get(self, request, *args, **kwargs):
        company_id = kwargs.get('company_id')
        company = companies.get_company_by_id(company_id)
        if not company:
            return Http404()
        self.company = company
        return super(CreateDepartmentView, self).get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        company_id = kwargs.get('company_id')
        company = companies.get_company_by_id(company_id)
        if not company:
            return Http404()
        self.company = company
        return super().post(request, *args, **kwargs)

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.company = self.company
        messages.success(self.request, "Отдел %s добавлен в компанию %s" % (self.object.name, self.company.name))
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['company'] = self.company
        return context


class EditDepartmentView(LoginRequiredMixin, ModelFormMixin, ListView):
    model = Department
    fields = ['name']
    template_name = 'admin/departments/edit_department.html'

    def get_queryset(self):
        self.queryset = User.objects.filter(department=self.get_object())
        return super(EditDepartmentView, self).get_queryset()

    def get_object(self, queryset=None):
        queryset = Department.objects.all()
        return super().get_object(queryset)

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.company = companies.get_company_by_id(kwargs.get('company_id'))
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = ModelFormMixin.get_context_data(self, **kwargs)
        context = ListView.get_context_data(self, **context)
        context['company'] = self.company
        return context

    def post(self, request, *args, **kwargs):
        self.object  = self.get_object()
        form = self.get_form()
        self.form = form
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def put(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)

    def form_valid(self, form):
        result = super().form_valid(form)
        messages.success(self.request, "Отдел %s отредактирован" % self.object.name)
        return result


class DeleteDepartmentView(LoginRequiredMixin, DeleteView):
    model = Department

    def delete(self, request, *args, **kwargs):
        department = self.get_object()
        company = department.company
        department_name = department.name
        self.company_id = company.id
        result = super().delete(request, *args, **kwargs)
        messages.success(request, "Отдел %s удалён из компании %s" % (department_name, company.name))
        return result

    def get_success_url(self):
        return reverse('admin_company', kwargs={'pk': self.company_id})
