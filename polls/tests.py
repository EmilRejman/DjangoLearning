from django.test import TestCase
import datetime
from django.utils import timezone
from django.urls import reverse
from .models import Question, Choice

# Create your tests here.
### internal behaviour of code
class QuestionModelTest(TestCase):

    def test_was_published_recently_with_future_question(self):
        '''
        was_published_recently() returns False for questions whose pub_date is in the future
        it shall return pass True only for day before
        '''

        time=timezone.now() + datetime.timedelta(days=30)
        future_question = Question(pub_date=time)
        self.assertIs(future_question.was_published_recently(), False)

    def test_was_published_recently_with_old_question(self):
        '''
        was_published_recently() returns true when pub_dat is <= 1 day
        '''
        time = timezone.now() - datetime.timedelta(days=1, minutes=1)
        old_question = Question(pub_date = time)
        self.assertIs(old_question.was_published_recently(), False)

    def test_was_published_recently_with_recent_question(self):
        '''
        was_published_recently() returns true when pub_dat is <= 1 day
        '''
        time1 = timezone.now() - datetime.timedelta(days=0, hours=23, minutes=59, seconds= 59)
        recent_question1 = Question(pub_date=time1)
        self.assertIs(recent_question1.was_published_recently(), True)

        time2 = timezone.now()
        recent_question2 = Question(pub_date=time2)
        self.assertIs(recent_question2.was_published_recently(), True)

####

def create_question(question_text, days):
    """
    Create a question with the given `question_text` and published the
    given number of `days` offset to now (negative for questions published
    in the past, positive for questions that have yet to be published).
    """
    time = timezone.now() + datetime.timedelta(days=days)
    return Question.objects.create(question_text=question_text, pub_date=time)


class QuestionIndexViewTests(TestCase):
    def test_no_questions(self):
        """
        If no questions exist, an appropriate message is displayed.
        """
        response = self.client.get(reverse('polls:index'))
        self.assertEqual(response.status_code, 200) #OK status code
        self.assertContains(response, "No polls are available.") # "No polls are available." is in index.html
        self.assertContains(response, "Test of second text.")  # "Test of second text." is in index.html
        self.assertQuerysetEqual(response.context['latest_question_list'], []) #no questions so the table is clear


    def test_past_question(self):
        """
        Questions with a pub_date in the past are displayed on the
        index page.
        """
        q1 = create_question(question_text="Past question.", days=-30) #we craete question so its added to database
        c1 = Choice.objects.create(question=q1, choice_text='answer 1', votes=0)
        response = self.client.get(reverse('polls:index')) #answer as the user would enter the index page
        self.assertQuerysetEqual(
            response.context['latest_question_list'],
            ['<Question: Past question.>']
        ) #check if querryset is: object Question with text "Past question."


    def test_future_question(self):
        """
        Questions with a pub_date in the future aren't displayed on
        the index page.
        """
        create_question(question_text="Future question.", days=30)
        response = self.client.get(reverse('polls:index'))
        self.assertContains(response, "No polls are available.")
        self.assertQuerysetEqual(response.context['latest_question_list'], [])

    def test_future_question_and_past_question(self):
        """
        Even if both past and future questions exist, only past questions
        are displayed.
        """
        qp = create_question(question_text="Past question.", days=-30)
        cp = Choice.objects.create(question=qp, choice_text='answer 1', votes=0)
        qf = create_question(question_text="Future question.", days=30)
        cf = Choice.objects.create(question=qf, choice_text='answer 1', votes=0)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(
            response.context['latest_question_list'],
            ['<Question: Past question.>']
        )

    def test_two_past_questions(self):
        """
        The questions index page may display multiple questions.
        """
        q1 = create_question(question_text="Past question 1.", days=-30)
        c1 = Choice.objects.create(question=q1, choice_text='answer 1', votes=0)
        q2 = create_question(question_text="Past question 2.", days=-5)
        c2 = Choice.objects.create(question=q2, choice_text='answer 1', votes=0)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(
            response.context['latest_question_list'],
            ['<Question: Past question 2.>', '<Question: Past question 1.>']
        )

    def test_question_with_one_choice(self):
        """
        The question idex page is displaying questions with >= 1 choices
        """
        q1 = create_question(question_text="Past question 1.", days=-5)
        c1 = Choice.objects.create(question=q1, choice_text='answer 1', votes=0)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(
            response.context['latest_question_list'],
            ['<Question: Past question 1.>']
        )

    def test_question_without_choice(self):
        """
        The question idex page isnt displaying questions with < 1 choices
        """
        q1 = create_question(question_text="Past question 1.", days=-5)
        response = self.client.get(reverse('polls:index'))
        self.assertContains(response, "<p>No polls are available.</p>")
        self.assertQuerysetEqual(response.context['latest_question_list'], [])




class QuestionDetailViewTests(TestCase):
    def test_future_question(self):
        """
        The detail view of a question with a pub_date in the future
        returns a 404 not found.
        """
        future_question = create_question(question_text='Future question.', days=5)
        url = reverse('polls:detail', args=(future_question.id,)) ##path('<int:pk>/', views.DetailView.as_view(), name='detail'),
        # we put argument so we add it to <int:pk>
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_past_question(self):
        """
        The detail view of a question with a pub_date in the past
        displays the question's text.
        """
        past_question = create_question(question_text='Past Question.', days=-5)
        url = reverse('polls:detail', args=(past_question.id,))
        response = self.client.get(url)
        self.assertContains(response, past_question.question_text)
