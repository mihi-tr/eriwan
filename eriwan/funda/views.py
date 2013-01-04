# Create your views here.
from django.http import HttpResponse
from django.shortcuts import render_to_response, get_object_or_404
from funda.models import *
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

def home(request):
  questions=Question.objects.order_by('date').reverse()[0:5]
  answers=Answer.objects.order_by('date').reverse()[0:5]
  keywords=Keyword.objects.order_by('word')
  return render_to_response("home.html",locals()) 

def create_pagination(request,list):
  paginator = Paginator(list.order_by('date').reverse(), 25)
  page = request.GET.get('page')
  try:
    questions=paginator.page(page)
  except PageNotAnInteger:
    questions=paginator.page(1)
  except EmptyPage:
    questions=paginator.page(paginator.num_pages)
  return questions

def questions(request):
  questions=create_pagination(request,Question.objects.all())
  return render_to_response("questions.html",locals())

def keyword(request,id):
  keyword=get_object_or_404(Keyword,id=id)
  questions=create_pagination(request,Question.objects.filter(keywords=keyword))
  return render_to_response("keywords.html",locals())

def person(request,parlid):
  person=get_object_or_404(Person,parlid=parlid)
  questions=create_pagination(request,Question.objects.filter(asker=person))
  return render_to_response("person.html",locals())

def asked(request,parlid):
  person=get_object_or_404(Person,parlid=parlid)
  questions=create_pagination(request,Question.objects.filter(asked=person))
  return render_to_response("asked.html",locals())

def get_similar(question):
  distances=Distance.objects.raw("""select * from funda_distance where
  src_id=%s or dst_id=%s order by distance limit 10;"""%(question.id,question.id))
  for d in distances:
    if question==d.src:
      yield d.dst
    else:
      yield d.src

def question(request,parlid):
  question=get_object_or_404(Question,parlid=parlid)
  #similar=get_similar(question)
  try:
    answer=Answer.objects.get(question=question)
  except Answer.DoesNotExist:
    answer=None
  terms=NotableTerms.objects.filter(question=question)  
  return render_to_response("question.html",locals())

def persons(request):
  persons=Person.objects.raw("""SELECT * from funda_person where id in
    (select distinct asker_id from funda_question) order by name;""")
  return render_to_response("persons.html",locals()) 
