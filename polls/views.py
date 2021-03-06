import hashlib
from builtins import super
import datetime
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from .models import Question, Choice
from django.http import Http404
from django.urls import reverse
from django.views import generic
from django.utils import timezone
from django.db.models import Count
from .forms import AddQuestionForm, ChoiceFormSet
from django.forms import formset_factory
from django.utils.http import is_safe_url
from django.views.decorators.cache import cache_page





# Create your views here.
'''
def index(request):
    latest_question_list = Question.objects.order_by('-pub_date')[:5]
    #print(latest_question_list) #printuje na serwerze co się dzieje
    template = loader.get_template('polls/index.html')
    context = {
        'latest_question_list': latest_question_list,
    }
    #return HttpResponse(template.render(context,request))
    return render(request, 'polls/index.html', context)


def detail(request, question_id):
    # try:
    #     question = Question.objects.get(id=question_id)
    # except Question.DoesNotExist:
    #     raise Http404("Question does not exist")
    ### get_object_or_404 to to samo co u góry tylko lepsze
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'polls/detail.html', {'question': question})
    #return HttpResponse("You're looking at question %s." % question_id)


def results(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'polls/results.html', {'question': question})
'''

#new way with views

class IndexView(generic.ListView):
    paginate_by = 5
    template_name = 'polls/index.html' #Similarly, the ListView generic view uses a default template called <app name>/<model name>_list.html;
    # we use template_name to tell ListView to use our existing "polls/index.html" template.
    #context_object_name = 'latest_question_list' #context_object_name attribute, specifying that we want to use latest_question_list instead.
    #thats why we know what name to use in .html file
    #otherwise it would be named "object_list"


    def get_queryset(self): # defines how the querryset will be created, we override it to write 5 questions, not all form DB
        """Return the last five published questions.

        if we wanna chenge the context #context = super().get_context_data(**kwargs)  ### in this case super() referse to parent classes in a
        we need to remember (if needed) to get context from parents class
        """
        # we return 5 latests questions which date is allready released
        if self.request.user.is_authenticated:
            return Question.objects.filter(pub_date__lte=timezone.now()).annotate(choice_count=Count('choice')).filter(choice_count__gte=1).order_by('-pub_date')
        else:
            return []

        #pub_date__lte <- "less then or equal to" && number of choices greater than or equal to 1


    # to use different context we overload the get_context_data method
    def get_context_data(self, **kwargs):
        # Call the base implementation first to get the context
        context = super().get_context_data(**kwargs)

        # Number of visits to this view, as counted in the session variable.
        num_visits = self.request.session.get('num_visits', 0)
        self.request.session['num_visits'] = num_visits + 1
        # Create any data and add it to the context
        context['num_visits'] = num_visits
        return context




class DetailView(LoginRequiredMixin,generic.DetailView): #used to let to this URL only logged in users
    # redirect_field_name = 'redirect_to'  #uf we want to redirect it to different URL
    model = Question
    template_name = 'polls/detail.html' # DetailView generic view uses a template called <app name>/<model name>_detail.html.
    # In our case, it would use the template "polls/question_detail.html". The template_name attribute is used to tell
    # Django to use a specific template name instead of the autogenerated default template name.

    #@property  #turns the function into "getter" - read-only atrubite
    def get_queryset(self):
        """
        Excludes any questions that aren't published yet.
        """
        return Question.objects.filter(pub_date__lte=timezone.now())  # it is DetailView thats why we dont use
        # choice_set because we allready have object


class ResultsView(generic.DetailView):
    model = Question
    template_name = 'polls/results.html'

# used for function based views
@login_required  #with this decorator (func which gets func as argument) lets logged users to use this function, if not they will be transsfered to login page
def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice']) #request.POST dostaję request typu post bo ktoś kliknął w guzik
        #<input type="radio" name="choice" id="choice{{ forloop.counter }}" value="{{ choice.id }}"> <- this in html
        # dictionary-like object that lets you access submitted data by key name
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the question voting form.
        return render(request, 'polls/detail.html', {
            'question': question,
            'error_message': "You didn't select a choice.",
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))
        # HttpResponseRedirect takes a single argument: the URL to which the user will be redirected
        # you should always return an HttpResponseRedirect after successfully dealing with POST data.
        # This tip isn’t specific to Django; it’s good Web development practice in general.

        #redirect helps to avoid hardcoding URL , given name where we want to pass controll and arguments

#The add question process will be writing to our database, so, by convention, we use the POST request approach.
# for class based view we need PermisionRequiredMixin and variable permission_required = 'catalog.can_mark_returned'
@permission_required('question.can_add_question')
def AddQuestion(request):
    # If this is a POST request then process the Form data

    """ChoiceFormSet = formset_factory(ChoiceForm, formset=BaseChoiceFormSet, max_num=10, validate_max=True,
                                    min_num=2, validate_min=True, can_delete=True)"""

    if request.method == 'POST':
        print('\n\n',request.POST,'\n\n',request.POST.get('csrfmiddlewaretoken').encode('utf-8'),'\n\n',request.session,'\n\n')

        # Create a form instance and populate it with data from the request (binding):
        form = AddQuestionForm(request.POST)

        ChoicesFormset = ChoiceFormSet(request.POST) #request.FILES for files upload handling

        # hashstring = hashlib.sha1(request.POST.get('csrfmiddlewaretoken').encode('utf-8'))  ## This is going to be unique
        # if request.session.get('sesionform') != hashstring:
        # Check if the form is valid:
        if form.is_valid() and ChoicesFormset.is_valid():
            question_instance = Question(question_text = form.cleaned_data['question_text'],\
                                pub_date = form.cleaned_data['pub_date'])
            question_instance.save()

            print('print all ChoicesFormset')
            print(ChoicesFormset)
            for answer in ChoicesFormset:
                print('rpint jeden test')
                print(answer)
                choice_instance = Choice(question = question_instance, choice_text = answer.cleaned_data['choice_text'])
                choice_instance.save()

            #check if redirect URL is safe
            print(is_safe_url(reverse('polls:index'),allowed_hosts=None))
            # redirect to a new URL:
            return HttpResponseRedirect(reverse('polls:index'))

    # If this is a GET (or any other method) create the default form.
    else:
        form = AddQuestionForm()
        ChoicesFormset = ChoiceFormSet()


    context = {
        'form': form,
        'choices': ChoicesFormset,
        #'question_instance': question_instance,
    }

    return render(request, 'polls/AddQuestion.html', context)