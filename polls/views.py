from django.http import HttpResponse, JsonResponse, Http404
from django.shortcuts import render, get_object_or_404

from .models import Question, Choice, Project, Employee, IdempotencyKey, Comment

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, BasePermission
from rest_framework.response import Response
from django_ratelimit.decorators import ratelimit
from datetime import date
import re


class IsAdminRole(BasePermission):
    def has_permission(self, request, view):
        return request.user.groups.filter(name='Admin').exists()
    

@api_view(['GET'])
@ratelimit(key='ip', rate='10/m', method='GET', block=True)
def search_employee(request):
    name = request.GET.get('name')

    if not name:
        return Response({'error': 'Name required'}, status=400)

    if len(name) > 100:
        return Response({'error': 'Too long'}, status=400)

    if not re.match(r'^[a-zA-Z ]+$', name):
        return Response({'error': 'Invalid name'}, status=400)

    employees = Employee.objects.filter(name=name)
    data = list(employees.values())

    return Response(data)


@api_view(['POST'])
def create_comment(request):
    username = request.data.get('username')
    message = request.data.get('message')

    if not username or not message:
        return Response({'error': 'Invalid data'}, status=400)

    comment = Comment.objects.create(
        username=username,
        message=message
    )

    return Response({'message': 'Comment added'})


@api_view(['GET'])
@ratelimit(key='ip', rate='5/m', method='GET', block=True)
def get_questions(request):
    data = list(Question.objects.values())
    return Response(data)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
@ratelimit(key='ip', rate='10/m', method='POST', block=True)
def create_employee(request):
    name = request.data.get('name')
    email = request.data.get('email')
    salary = request.data.get('salary')
    project_id = request.data.get('project_id')

    if not name:
        return Response({'error': 'Name required'}, status=400)

    if not email:
        return Response({'error': 'Email required'}, status=400)

    if salary is None or float(salary) < 0:
        return Response({'error': 'Invalid salary'}, status=400)

    if not project_id:
        return Response({'error': 'Project ID required'}, status=400)

    employee = Employee.objects.create(
        name=name,
        email=email,
        salary=salary,
        designation="Developer",
        date_joined="2024-01-01",
        project_id=project_id
    )

    return Response({'message': 'Employee created', 'id': employee.id})

@api_view(['POST'])
@ratelimit(key='ip', rate='10/m', method='POST', block=True)
def create_project(request):
    key = request.headers.get('Idempotency-Key')

    if not key:
        return Response({'error': 'Idempotency-Key required'}, status=400)

    if IdempotencyKey.objects.filter(key=key).exists():
        return Response({'message': 'Duplicate request (ignored)'})

    name = request.data.get('name')

    if not name:
        return Response({'error': 'Project name required'}, status=400)

    project = Project.objects.create(
        name=name,
        start_date=date.today()
    )

    IdempotencyKey.objects.create(key=key)

    return Response({'message': 'Created', 'id': project.id})

@api_view(['GET'])
@permission_classes([IsAuthenticated, IsAdminRole])
def get_projects(request):
    data = list(Project.objects.values())
    return Response(data)





@api_view(['GET'])
def get_choices(request):
    data = list(Choice.objects.values())
    return Response(data)


@api_view(['GET'])
def get_employees(request):
    data = list(Employee.objects.values())
    return Response(data)




def index(request):
    latest_question_list = Question.objects.order_by('-pub_date')[:5]
    context = {'latest_question_list': latest_question_list}
    return render(request, 'polls/index.html', context)


def detail(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'polls/detail.html', {'question': question})


def results(request, question_id):
    return HttpResponse(f"You're looking at the results of question {question_id}.")


def vote(request, question_id):
    return HttpResponse(f"You're voting on question {question_id}.")

def comments_page(request):
    comments = Comment.objects.all()
    return render(request, 'polls/comments.html', {'comments': comments})