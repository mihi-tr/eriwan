from django.core.management.base import NoArgsCommand, make_option
from django.db import connection, transaction
from funda.models import *
from pyquery import PyQuery
import math

class Command(NoArgsCommand):
  help = "Calculate distances between the questions"
  option_list = NoArgsCommand.option_list + (
    make_option('--verbose', action='store_true'),
    )
  def handle_noargs(self, **options):
    questions=Question.objects.all().order_by('id')
    questions=map(self.count_words,questions)
    cursor = connection.cursor()
    cursor.execute("select src_id,dst_id from funda_distance")
    done=set(cursor.fetchall())
    
    lq=len(questions)+1

    def calculate_distances(sq):
      sv=questions[sq-1]
      for dq in range(sq+1,lq):
        dv=questions[dq-1]
        if (sq,dq) not in done:
          yield(None,sq,dq,self.distance(sv,dv))

    for sq in range(1,lq):
      print sq
      cursor.executemany("INSERT into funda_distance values (?,?,?,?)",
        calculate_distances(sq))
      transaction.commit_unless_managed()

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
