# Create your views here.
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404  #There’s also a get_list_or_404() function, which works
                                                        #  just as get_object_or_404() – except using filter() instead of get().
                                                        #     It raises Http404 if the list is empty.
# from django.template import loader
from django.urls import reverse
from .models import Question, Choice
from django.views import generic
from django.utils import timezone


# VIEW CLASSES
class IndexView(generic.ListView):
    template_name = 'polls/index.html'
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        """Return the last five publsihed questions"""
        return Question.objects.filter(
            pub_date__lte=timezone.now() # returns a queryset containing objects only older than .now()
        ).order_by('-pub_date')[:5]


class DeatilView(generic.DetailView):
    model = Question
    template_name = 'polls/detail.html'

    def get_queryset(self):
        return Question.objects.filter(pub_date__lte=timezone.now())



class ResultsView(generic.DetailView):
    model = Question
    template_name = 'polls/results.html'



# ========== USING CLASSES ABOVE INSTEAD OF THE FUNCTIONS BELOW ==========
# def index(request):
#     latest_question_list = Question.objects.order_by('-pub_date')[:5] # pylint: disable
#     context = {'latest_question_list': latest_question_list}
#     print(context)
#     return render(request, 'polls/index.html', context)
#
#
# def detail(request, question_id):
#     # try:
#     #     question = Question.objects.get(pk=question_id)
#     # except Question.DoesNotExist:
#     #     raise Http404("Question does not exist")
#
#     # A better implementation below:
#     question = get_object_or_404(Question, pk=question_id)
#     return render(request, "polls/detail.html", {'question': question})
#
#
# def results(request, question_id):
#     question = get_object_or_404(Question, pk=question_id)
#     return render(request, 'polls/results.html', {'question': question})
# =========================================================================

def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the voting form
        return render(request, 'polls/detail.html', {
            'question': question,
            'error_message': "Please select a valid choice.",
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        # Always return an HttpResponseRedirect to avoid users
        #   from going to the previous page and revoting unintentionally
        return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))
