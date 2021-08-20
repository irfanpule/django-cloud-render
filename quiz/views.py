from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.template.loader import render_to_string
from django.urls import reverse

from quiz.models import Quiz, Question


def index(request):
    context = {
        'title': 'Beranda'
    }
    return render(request, 'index.html', context)


class QuizListView(ListView):

    model = Quiz
    paginate_by = 100
    template_name = 'game-list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Daftar Quiz'
        return context


class QuizDetailView(DetailView):
    model = Quiz
    template_name = 'game-detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = context['object'].title
        return context


class QuestionReviewView(DetailView):
    model = Question
    template_name = 'quiz/game-quiz.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Game dimulai"
        return context


def playing(request, pk):
    """
    fungsi ini digunakan untuk menginisiasi halaman awal permainan.
    dan set id pertama pada quiz apa yang harus dimunculkan
    """
    quiz: Quiz = get_object_or_404(Quiz, pk=pk)
    question_list = list(quiz.question_set.order_by('-id').values_list('id', flat=True))
    context = {
        'title': 'Bermain quiz',
        'question_id': question_list[-1],
        'object': quiz
    }

    # init beberapa data session
    request.session['question_list'] = question_list
    request.session['score'] = 0
    request.session['total_question'] = len(question_list)
    request.session['current_position'] = 1

    return render(request, 'quiz/quiz-no-content.html', context)


def ajax_question_detail(request, pk):
    """
    fungsi ini digunakan untuk mengambil pertanyaan pda sebuah quiz.
    mengecek dan mengurangi pertanyaan yang sudah muncul.
    """
    question: Question = get_object_or_404(Question, pk=pk)
    question_list = request.session.get('question_list')
    question_list.pop()

    # update question_list and update current position
    request.session['question_list'] = question_list
    request.session['current_position'] = request.session['total_question'] - len(question_list)

    if not question_list:
        question_id = 0
    else:
        question_id = question_list[-1]

    # render html ke string dan masukan dalam response json
    context = {
        'object': question,
        'question_id': question_id,
        'score': request.session['score'],
        'total_question': request.session['total_question'],
        'current_position': request.session['current_position']
    }
    html = render_to_string('quiz/quiz-only-content.html', context)
    body = {
        'html': html,
        'question_id': question_id
    }
    return JsonResponse(body, status=200)


def ajax_get_answer(request, question_id, answer_id):
    question: Question = get_object_or_404(Question, id=question_id)
    answer = question.answer_set.filter(id=answer_id, is_correct=True).first()

    if answer:
        # jika benar tambahkan score
        request.session['score'] += 10
        body = {
            'score': request.session['score']
        }
        return JsonResponse(body, status=200)

    body = {
        'question_id': request.session['score']
    }
    return JsonResponse(body, status=400)
