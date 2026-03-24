from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.mixins import (
    LoginRequiredMixin, UserPassesTestMixin, PermissionRequiredMixin
)
from django.urls import reverse_lazy
from django.views.generic import (
    ListView, CreateView, UpdateView, DeleteView, TemplateView
)
from .forms import NotebookForm
from .models import Notebook


class NotebookListView(ListView):
    model = Notebook
    template_name = 'notebook_list.html'
    context_object_name = 'notebooks'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        visitas = self.request.session.get('visitas_inicio', 0)
        self.request.session['visitas_inicio'] = visitas + 1
        context['visitas'] = self.request.session['visitas_inicio']
        return context


class NotebookCreateView(CreateView):
    model = Notebook
    form_class = NotebookForm
    template_name = 'notebook_form.html'
    success_url = reverse_lazy('notebook_list')

    def form_valid(self, form):
        messages.success(self.request, 'Notebook creado correctamente.')
        return super().form_valid(form)


class NotebookUpdateView(UpdateView):
    model = Notebook
    form_class = NotebookForm
    template_name = 'notebook_form.html'
    success_url = reverse_lazy('notebook_list')

    def form_valid(self, form):
        messages.success(self.request, 'Notebook actualizado correctamente.')
        return super().form_valid(form)


class NotebookDeleteView(DeleteView):
    model = Notebook
    template_name = 'notebook_confirm_delete.html'
    success_url = reverse_lazy('notebook_list')

    def form_valid(self, form):
        messages.success(self.request, 'Notebook eliminado correctamente.')
        return super().form_valid(form)

class AccesoDenegadoView(TemplateView):
    template_name = 'acceso_denegado.html'

class SoloEncargadosMixin(LoginRequiredMixin, UserPassesTestMixin):
    login_url = reverse_lazy('login')

    def test_func(self):
        user = self.request.user
        return (
            user.groups.filter(name='Encargados').exists()
            and user.has_perm('inventario.puede_ver_reporte_interno')
        )

    def handle_no_permission(self):
        if not self.request.user.is_authenticated:
            return redirect(self.login_url)
        return redirect('acceso_denegado')


class ReporteInternoView(SoloEncargadosMixin, TemplateView):
    template_name = 'reporte_interno.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['total'] = Notebook.objects.count()
        context['disponibles'] = Notebook.objects.filter(disponible=True).count()
        context['mantencion'] = Notebook.objects.filter(estado='mantencion').count()
        return context