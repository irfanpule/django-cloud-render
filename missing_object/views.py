from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from missing_object.models import MissingObject
from missing_object.utils import random_picture_missing_obj


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


class QuestionReviewView(DetailView):
    model = MissingObject
    template_name = 'missing_objects/game-missing-object.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Game dimulai"
        ids = context['object'].imageobjects.values_list('id', flat=True)
        pictures, names = random_picture_missing_obj(ids)
        context['pictures'] = pictures
        context['names'] = names
        return context
