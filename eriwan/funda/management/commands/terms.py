from django.core.management.base import NoArgsCommand, make_option
from funda.models import *
from pyquery import PyQuery
import nltk
import itertools
import math
from django.db import connection, transaction


class TermCache:
  def __init__(self):
    self.terms={}
  
  def get_term(self,term):
    try:
      self.terms[term]=Term.objects.get(term=term)
      return self.terms[term]
    except Term.DoesNotExist:
      self.terms[term]=Term(term=term)
      self.terms[term].save()
      return self.terms[term]

  def get(self,term):
    return self.terms.get(term,self.get_term(term))
    
    
class Command(NoArgsCommand):
  help = "Counts the terms in each question and identifies important terms"
  option_list = NoArgsCommand.option_list + (
    make_option('--verbose', action='store_true'),
    )
  def handle_noargs(self, **options):
    self.get_term_counts()
    self.tfidf()

  def get_term_counts(self):
    questions=Question.objects.raw("""Select * from funda_question where id
    not in (select question_id from funda_termcount)""");
    tcache=TermCache()

    for q in questions: 
      print q.id
      pq=PyQuery(q.text)
      words=nltk.word_tokenize(pq.text())
      fd=nltk.FreqDist(words)
      for i in fd.items():  
       term=tcache.get(i[0])
       tc=TermCount(count=i[1])
       tc.term=term
       tc.question=q
       tc.save()

  def tfidf(self):
    questions=Question.objects.raw("""Select * from funda_question where id
    not in (select question_id from funda_notableterms)""")
    cursor=connection.cursor()
    
    cursor.execute("""Select count(distinct(question_id)) from
    funda_termcount;""")
    total_docs=cursor.fetchone()[0]

    def calculate(tc):
      tf=1+math.log(tc.count)
      cursor.execute("""Select count(distinct(question_id)) from funda_termcount where
      term_id=%s"""%tc.term.id)
      tdc=cursor.fetchone()[0]
      idf=math.log(total_docs/tdc)
      return (tc.term,tf*idf)
      
    for q in questions:
      tcs=TermCount.objects.filter(question=q)
      tcs=sorted([calculate(t) for t in tcs],key=lambda x: x[1])[-5:]
      for t in tcs:
        nt=NotableTerms(term=t[0],question=q)
        nt.save()
