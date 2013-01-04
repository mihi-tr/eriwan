from django.core.management.base import NoArgsCommand, make_option
from funda.models import *
import nltk
import itertools
import math
from django.db import connection, transaction
import gc


class TermCache:
  max_terms=500
  def __init__(self):
    self.terms={}
  
  def get_term(self,term):
    try:
      t=Term.objects.get(term=term)
    except Term.DoesNotExist:
      t=Term(term=term)
      t.save()
    if len(self.terms)<self.max_terms:
      self.terms[term]=t
    return t

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
    
    n=0

    for q in questions: 
      print q.id
      words=nltk.word_tokenize(nltk.clean_html(q.text))
      fd=nltk.FreqDist(words)
      for i in fd.items():  
        term=tcache.get(i[0])
        tc=TermCount(count=i[1])
        tc.term=term
        tc.question=q
        tc.save()
      n+=1
      if not (n%50):
        gc.collect()

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
