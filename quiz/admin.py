from django.contrib import admin
from .models import Answer, Quiz, Question


class AnswerInline(admin.TabularInline):
    model = Answer
    extra = 4


@admin.register(Quiz)
class QuizAdmin(admin.ModelAdmin):
    search_fields = ('title',)


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    inlines = [AnswerInline]
    list_filter = ['quiz']
