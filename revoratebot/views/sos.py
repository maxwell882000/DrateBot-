from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from revoratebot.models import SosSignal


class SosSignalsListView(LoginRequiredMixin, ListView):
    template_name = 'admin/sos/list.html'
    model = SosSignal
    context_object_name = 'signals'
