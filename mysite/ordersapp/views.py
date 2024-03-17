from django.views.generic import TemplateView
from django.http import HttpRequest, HttpResponse
from django.db import transaction

from . import services


class DashboardView(TemplateView):
    template_name = "ordersapp/index.html"

    @transaction.atomic
    def post(self, request: HttpRequest, *args, **kwargs):
        if request.POST.get("change_status"):
            services.change_suborder_status(request)
        return self.get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(services.get_dashboard_context_data())
        return context
