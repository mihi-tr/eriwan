from django.core.management.base import NoArgsCommand, make_option
from funda.models import *
from pyquery import PyQuery
import math

class Command(NoArgsCommand):
  help = "Calculate distances between the questions"
  option_list = NoArgsCommand.option_list + (
    make_option('--verbose', action='store_true'),
    )
  def handle_noargs(self, **options):
    questions=Question.objects.all()
    vectors=dict(zip((q.parlid for q in questions),map(self.count_words,questions)))
    startingquestions=Question.objects.raw("""SELECT * from funda_question where id not in
    (select distinct src_id from funda_distance);""")
    for sq in startingquestions:
      print sq
      sv=vectors[sq.parlid]
      for q in questions:
        try:
          Distance.objects.get(src=sq,dst=q)
        except Distance.DoesNotExist:
          """Calculate the distance"""
          dv=vectors[sq.parlid]
          dist=self.distance(sv,dv)
          distance=Distance(src=sq,dst=q)
          distance.distance=dist
          distance.save()
          distance=Distance(src=q,dst=sq)
          distance.distance=dist
          distance.save()

  def count_words(self,question):
    pq=PyQuery(question.text)
    txt=pq.text()
    words=txt.split()

    def count(x,y):
      if y in x.keys():
        x[y]+=1
      else:
        x[y]=1
      return x
    return reduce(count,words,{})

  def distance(self,sv,dv):
    words=set(sv.keys()+dv.keys()) 

    def create_vector(words,v):
      for w in words:
        if w in v.keys():
          yield v[w]
        else:
          yield 0

    sv=[i for i in create_vector(words,sv)]
    dv=[i for i in create_vector(words,dv)]

    dp=reduce(lambda x,y: x+y,map(lambda x: x[0]*x[1],zip(sv,dv))) 
    # dot product
    sl=math.sqrt(reduce(lambda x,y: x+y,map(lambda x: x**2,sv)))
    dl=math.sqrt(reduce(lambda x,y: x+y,map(lambda x: x**2,dv)))
    ln=sl*dl
    return math.acos(dp/ln)
