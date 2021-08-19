from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from missing_object.models import MissingObject


class MissingObjectListView(ListView):

    model = MissingObject
    paginate_by = 100
    template_name = 'game-list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Daftar Game Pencarian Gambar'
        return context


class MissingObjectDetailView(DetailView):
    model = MissingObject
    template_name = 'game-detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = context['object'].title
        return context
