from django.core.management.base import NoArgsCommand, make_option
from funda.models import *
from pyquery import PyQuery
import itertools
import datetime,re

base="http://www.parlament.gv.at"
start="http://www.parlament.gv.at/PAKT/JMAB/index.shtml?DEB=&GBEZ=&AUS=ALLE&anwenden=Anwenden&ZUAS=ALLE&LISTE=&NRBR=NR&RGES=&FR=ALLE&STEP=&JMAB-BR=J_JPR_M-BR&listeId=105&ZEIT=&MIN=ALLE&DR=&pageNumber=&FBEZ=FP_005&xdocumentUri=%2FPAKT%2FJMAB%2Findex.shtml&R_MFRAS=MIN&VHG4=ALLE&AS=ALLE&VHG3=ALLE&VHG2=ALLE&requestId=0C4ED47B6E&R_MSFRASZU=MIN&VHG=&NAB=&SID=ALLE&SUCH=&GP=XXIV&ZUFR=ALLE&jsMode=&JMAB=J_JPR_M"

def make_date(str):
  (day,month,year)=[int(i) for i in str.split(".")]
  return datetime.date(day=day,month=month,year=year)

class Command(NoArgsCommand):
  help = "Scrape the Parliament Website and Update the Models"
  option_list = NoArgsCommand.option_list + (
    make_option('--verbose', action='store_true'),
    )
  def handle_noargs(self, **options):
    # self.pages=itertools.ifilter(lambda x: not self.has_answer(x),
    #  self.get_start_list())
    self.process_page("/PAKT/VHG/XXIV/J/J_12779/index.shtml")

  def get_start_list(self):
    pq=PyQuery(start)
    table=pq("table.filter")
    def extract_url(row):
      return pq("td a",r).attr("href")
    return [extract_url(r) for r in pq("tr",table)]  

  def has_answer(self,url):
    try:
      question=Question.objects.get(url=url)
    except Question.DoesNotExist:
      return False
    try:
      answer=Answer.objects.get(question=question)
      return True
    except Answer.DoesNotExist:
      return False
  
  def get_html(self,url):
    pq=PyQuery("%s%s"%(base,url))
    return pq("body").html()

  def process_page(self,url): 
    pq=PyQuery("%s%s"%(base,url))
    parlid=url.split("/")[5]
    print parlid
    try:
      question=Question.objects.get(parlid=parlid)
    except Question.DoesNotExist:
      question=Question(parlid=parlid)
    question.url="%s%s"%(base,url)
    question.name=pq("h1#inhalt").text()
    
    question.text=self.get_html(pq("div.reiterBlock > div.c_2 ul li:last a:last").attr("href"))

    question.date=make_date(pq("table.tabelle tbody tr:first td:first").text())
    question.deadline=make_date(re.search("\(Frist: ([0-9.]+)\)", 
      pq("table.tabelle tbody tr:first td:eq(1)").text()).group(1))

    def get_person(element):
      name=element.text
      id=element.get("href").split("/")[2]
      try:
        return Person.objects.get(parlid=id)
      except Person.DoesNotExist:
        person=Person(name=name,link="%s%s"%(base,element.get("href")),parlid=id)
        person.save()
        return person
    persons=[get_person(x) for x in pq("div.reiterBlock > div.c_2 > p a")]
    question.asker=persons[0]
    question.asked=persons[1]

    question.save() # save before many to many

    keywords=pq("#schlagwortBox li")
    
    def get_keyword(word):
      try:
        return Keyword.objects.get(word=word)
      except Keyword.DoesNotExist:
        keyword=Keyword(word=word)
        keyword.save()
        return keyword
    keywords=[get_keyword(r.text_content()) for r in keywords]
    question.keywords=keywords
    
    answerurl=pq("table.tabelle tbody tr:last td:eq(1) a").attr("href")
    if answerurl and re.search("/AB/",answerurl):
      self.process_answer(answerurl,question)

  def process_answer(self,url,question):
    pq=PyQuery("%s%s"%(base,url))
    parlid=url.split("/")[5]
    print "Answer %s"%parlid

    try:
      answer=Answer.objects.get(parlid=parlid)
    except Answer.DoesNotExist:
      answer=Answer(parlid=parlid)
    
    answer.question=question
    answer.url="%s%s"%(base,url)
    answer.date=make_date(pq("table.tabelle tbody tr:first td:first").text())
    if not pq("div.reiterBlock > div.c_2 ul"):
      """ The answer is not yet in the system """
      return None
    answer.text=self.get_html(pq("div.reiterBlock > div.c_2 ul li:last a:last").attr("href")) 
    answer.save()
    
