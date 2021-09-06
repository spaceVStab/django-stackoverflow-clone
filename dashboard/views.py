from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout
from .models import Answers, Questions
from . import forms
from rest_framework.decorators import parser_classes
from rest_framework.parsers import JSONParser

from django.contrib.auth.decorators import login_required
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from .serializers import QuestionsSerializer, AnswersSerializer
from .models import Answers, Questions
from rest_framework import status

from dashboard import serializers

def question_list(request):
    questions = Questions.objects.all().order_by('posted_at');
    return render(request, 'question_list.html', { 'questions': questions })

def question_detail(request, id):
    question = Questions.objects.get(id=id)
    answers = Answers.objects.filter(question_id=id)
    print(answers)
    return render(request, 'question_detail.html', { 'question': question, 'answers':answers })

@login_required(login_url="/dashboard/login/")
def post_answer(request, id):
    question = Questions.objects.get(id=id)
    if request.method == 'POST':
        form = forms.CreateAnswer(request.POST, request.FILES)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.answered_by = request.user
            instance.question = question
            instance.save()
            return redirect('dashboard:detail', id=id) 
            # render(request, 'question_detail.html', { 'question': question})
    else:
        form = forms.CreateAnswer()
    return render(request, 'question_detail.html', { 'question': question, 'form': form})

@login_required(login_url="/dashboard/login/")
def post_question(request):
    if request.method == 'POST':
        form = forms.CreateQuestion(request.POST, request.FILES)
        if form.is_valid():
            # save question to db
            instance = form.save(commit=False)
            instance.posted_by = request.user
            instance.save()
            return redirect('dashboard:question_list')
    else:
        form = forms.CreateQuestion()
    return render(request, 'post_question.html', { 'form': form })


def signup_view(request):
    if request.method == 'POST':
         form = UserCreationForm(request.POST)
         if form.is_valid():
             user = form.save()
             #  log the user in
             login(request, user)
             return redirect('dashboard:question_list')
    else:
        form = UserCreationForm()
    return render(request, 'signup.html', { 'form': form })

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            # log the user in
            user = form.get_user()
            login(request, user)
            if 'next' in request.POST:
                return redirect(request.POST.get('next'))
            else:
               return redirect('dashboard:question_list')
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', { 'form': form })

def logout_view(request):
    if request.method == 'POST':
            logout(request)
            return redirect('dashboard:question_list')

# get all questions
@api_view(["GET"])
def get_questions(request):
    questions = Questions.objects.all()
    serializer = QuestionsSerializer(questions, many=True)
    return JsonResponse({'questions':serializer.data}, safe=False, status=status.HTTP_200_OK)

# get ques by id

# update ques

# post ques
@api_view(["POST"])
@csrf_exempt
@parser_classes((JSONParser,))
@permission_classes([IsAuthenticated])
def post_question_api(request):
    print(request.data)
    payload = request.data
    user = request.user
    try:
        ques = Questions.objects.create(
            ques_title = payload["ques_title"],
            ques_text = payload["ques_text"],
            posted_by = user
        )
        serializer = QuestionsSerializer(ques)
        return JsonResponse({'question': serializer.data}, safe=False, status=status.HTTP_201_CREATED)
    except Exception:
        return JsonResponse({'error': 'Something went wrong'}, safe=False, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

# delete ques

# show ans to ques by ques id