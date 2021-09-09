from django.contrib import admin
from django.utils.html import mark_safe
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
    list_display = ('get_question', 'preview_question')

    @admin.display(description='Preview')
    def preview_question(self, obj):
        return mark_safe(f"<a href='{obj.get_preview_url}' target='_blank'>Preview</a>")

    @admin.display(description='Pertanyaan')
    def get_question(self, obj):
        return obj.plain_content
