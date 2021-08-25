from django.template import Library

register = Library()


@register.filter(name='correct_answer')
def correct_answer(question):
    answer = question.answer_set.filter(is_correct=True).first()
    return answer.content
