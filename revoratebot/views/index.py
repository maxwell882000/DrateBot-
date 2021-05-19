from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin


class IndexView(LoginRequiredMixin, TemplateView):
    template_name = 'admin/index.html'

    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)
