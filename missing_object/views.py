from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.shortcuts import render, get_object_or_404
from django.template.loader import render_to_string
from django.http import JsonResponse

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


def playing(request, pk):
    """
    fungsi ini digunakan untuk menginisiasi halaman awal permainan.
    dan set id pertama pada quiz apa yang harus dimunculkan
    """
    mo = get_object_or_404(MissingObject, pk=pk)
    img_ids = list(mo.imageobjects.values_list('id', flat=True))

    context = {
        'title': 'Bermain Pencarian Gambar',
        'missing_object_id': mo.id,
        'object': mo,
        'img_ids': img_ids
    }

    # init beberapa data session
    request.session['mo_img_ids'] = img_ids
    request.session['mo_lives'] = 3
    request.session['mo_correct_select'] = []

    return render(request, 'missing_objects/missing-object-no-content.html', context)


def ajax_get_pictures(request):
    ids = request.session['mo_img_ids']
    pictures, names = random_picture_missing_obj(ids)
    request.session['mo_pictures'] = pictures
    request.session['mo_names'] = names
    context = {
        'pictures': pictures,
        'names': names,
        'lives': range(0, request.session['mo_lives']),
        'lives_reminder': range(0, 3 - request.session['mo_lives'])
    }
    html = render_to_string('missing_objects/game-missing-object.html', context=context, request=request)
    body = {
        'html': html,
        'img_ids': request.session['mo_img_ids']
    }
    return JsonResponse(body, status=200)


def ajax_get_answer(request, id):
    pictures = request.session['mo_pictures']
    names = request.session['mo_names']
    find_picture = list(filter(lambda p: p['id'] == id, pictures))
    find_name = list(filter(lambda n: n['id'] == id, names))

    if find_picture and find_name:
        # TODO: kalau jawabannya bener, kurangi data mo_img_ids
        return JsonResponse({'message': 'berhasil'}, status=200)

    request.session['mo_lives'] -= 1
    # TODO: kalau mo_lives 0 redirect ke halaman kalah
    return JsonResponse({'error_message': 'salah'}, status=400)
