from django.http import HttpResponse
from django.template import loader
from django.shortcuts import render
from django.http import Http404
from django.shortcuts import get_object_or_404, render

from django.http import JsonResponse
from .models import Question, Choice, Project, Employee

def get_questions(request):
    data = list(Question.objects.values())
    return JsonResponse(data, safe=False)


def get_choices(request):
    data = list(Choice.objects.values())
    return JsonResponse(data, safe=False)


def get_projects(request):
    data = list(Project.objects.values())
    return JsonResponse(data, safe=False)


def get_employees(request):
    data = list(Employee.objects.values())
    return JsonResponse(data, safe=False)

def index(request):
    latest_question_list = Question.objects.order_by('-pub_date')[:5]
    context = {'latest_question_list': latest_question_list}
    return render(request, 'polls/index.html', context)
# Create your views here.
def detail(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'polls/detail.html', {'question': question})

def results(request, question_id):
    response = "You're looking at the results of question %s."
    return HttpResponse(response % question_id)

def vote(request, question_id):
    return HttpResponse("You're voting on question %s." % question_id)