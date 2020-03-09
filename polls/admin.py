from django.contrib import admin
from .models import Question, Choice

# Register your models here.
#class ChoiceInline(admin.StackedInline): #fields of choice one under anyother
class ChoiceInline(admin.TabularInline): #fields of choice in form of table
    model = Choice
    extra = 3


class QuestionAdmin(admin.ModelAdmin):
    fieldsets = [
        ('Question information',               {'fields': ['question_text']}),
        ('Date information', {'fields': ['pub_date']})
    ]
    inlines = [ChoiceInline]
    list_display = ('question_text', 'pub_date', 'was_published_recently') #this part of code is displayed not in description of Question
    # but in the list of all questions

    list_filter = ['pub_date'] #with this we can filter the Questions by its pub_date

    search_fields = ['question_text']

admin.site.register(Question, QuestionAdmin)
