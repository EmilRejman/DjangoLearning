from django import forms
from django.core.exceptions import ValidationError
from django.forms import formset_factory, BaseFormSet
import datetime
from django.utils import timezone
from django.utils.translation import ugettext_lazy
import re
from .models import Choice


class AddQuestionForm(forms.Form):
    question_text = forms.CharField(help_text="Enter a question text, not longer then 200 signs", \
                                    label="question text")

    myDate = timezone.now()
    pub_date = forms.DateTimeField(help_text="Enter a publication date, not in past, \
        if in future the question will be shown after the date", \
                                   label="publication date and time", initial=myDate )


    def clean_question_text(self):
        data = self.cleaned_data['question_text']

        # check if data is empty
        if data == '':
            raise ValidationError(ugettext_lazy('Invalid question text - it is empty!'))

        # check if data has only allowed signs
        pattern = re.compile("^[a-zA-Z0-9,.!? ]+$")
        if not pattern.match(data):
            raise ValidationError(ugettext_lazy('Invalid question text - not allowed signs'))

        # check if data is more then 200
        if len(data) > 200:
            raise ValidationError(ugettext_lazy('Invalid question text - text too long'))

        return data

    def clean_pub_date(self):
        """ #This step gets us the data "cleaned" and sanitized of
        potentially unsafe input using the default validators"""
        data = self.cleaned_data['pub_date']

        # check if data is not in the past
        now = timezone.now()
        if data < now - datetime.timedelta(minutes=60):
            raise ValidationError(ugettext_lazy('Invalid date - question in the past'))

        """ we wraps this text in one of Django's translation functions ugettext_lazy(),
        which is good practice if you want to translate your site later. """

        # check if data is not more then 1 year in future
        if data > now + datetime.timedelta(days=365):
            raise ValidationError(ugettext_lazy('Invalid date - question too far in future'))

        return data


class ChoiceForm(forms.ModelForm):

    class Meta:
        model = Choice
        fields = ['choice_text']
        labels = {'choice_text': ugettext_lazy('Your answer')}
        initial = {'choice_text': ugettext_lazy('answer...')}
        help_text = {'choice_text': ugettext_lazy('100 chars max')}

    def clean_choice_text(self):
        data = self.cleaned_data['choice_text']
        print('entered clean choice text')
        # check if data is empty
        if data == '' or data is None:
            print('ChoiceForm - Invalid answer text - it is empty')
            raise ValidationError(ugettext_lazy('Invalid answer text - it is empty!'))

        # check if data has only allowed signs
        pattern = re.compile("^[a-zA-Z0-9,.!? ]+$")
        if not pattern.match(data):
            print('ChoiceForm - Invalid answer text - not allowed signs')
            raise ValidationError(ugettext_lazy('Invalid answer text - not allowed signs'))

        # check if data is more then max length defined in choice
        if len(data) > 100: #Choice.choice_text.max_length:
            print('ChoiceForm - Invalid question text - text too long')
            raise ValidationError(ugettext_lazy('Invalid question text - text too long'))

        return data




'''# defing clean method for whole formset
The formset clean method is called after all the Form.clean methods have been called.
The errors will be found using the non_form_errors() method on the formset.
'''
class BaseChoiceFormSet(BaseFormSet):
    def clean(self):
        """Checks that no two articles have the same title."""
        if any(self.errors):
            print('self errors of each choice')
            # Don't bother validating the formset unless each form is valid on its own
            return
        answers = []
        for form in self.forms:
            if self.can_delete and self._should_delete_form(form): # if we click delete box on html
                print('BaseChoiceFormSet - Delete')
                continue
            answer = form.cleaned_data.get('choice_text')
            if answer in answers:
                print('BaseChoiceFormSet - Choices must have distinct texts')
                raise forms.ValidationError("Choices must have distinct texts.")
            answers.append(answer)


ChoiceFormSet = formset_factory(ChoiceForm, formset=BaseChoiceFormSet, max_num=10, validate_max=True,
                                min_num=2, validate_min=True, extra=0, can_delete=False)
#

"""
maximum number of 10 answers, minimum number of 2 answers
formset.errors() will not rise an error if min or max exceeded, but
formset.non_form_errors() will rise one
"""

"""
The formset_factory() provides two optional parameters can_order and can_delete to help with ordering of forms in formsets and deletion of forms from a formset.
can_order=True:
This adds an additional field to each form. This new field is named ORDER and is an forms.IntegerField. For the forms that came from the initial data 
it automatically assigned them a numeric value.

can_delete=True:
Similar to can_order this adds a new field to each form named DELETE and is a forms.BooleanField.
When data comes through marking any of the delete fields you can access them with deleted_forms
f you are using a ModelFormSet, model instances for deleted forms will be deleted when you call formset.save().
"""

# Custom formset validation - is valid function will check each choice one by one

''' #check if data for each form in formset is valid
formset = ArticleFormSet(data)
>>> formset.is_valid()

in data the below fields are needed to work:
'form-TOTAL_FORMS': '1',
'form-INITIAL_FORMS': '0',
'form-MAX_NUM_FORMS': '',

'''
