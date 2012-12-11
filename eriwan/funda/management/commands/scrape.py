from django.core.management.base import NoArgsCommand, make_option
from funda.models import *
from pyquery import PyQuery
import itertools

base="http://www.parlament.gv.at"
start="http://www.parlament.gv.at/PAKT/JMAB/index.shtml?DEB=&GBEZ=&AUS=ALLE&anwenden=Anwenden&ZUAS=ALLE&LISTE=&NRBR=NR&RGES=&FR=ALLE&STEP=&JMAB-BR=J_JPR_M-BR&listeId=105&ZEIT=&MIN=ALLE&DR=&pageNumber=&FBEZ=FP_005&xdocumentUri=%2FPAKT%2FJMAB%2Findex.shtml&R_MFRAS=MIN&VHG4=ALLE&AS=ALLE&VHG3=ALLE&VHG2=ALLE&requestId=0C4ED47B6E&R_MSFRASZU=MIN&VHG=&NAB=&SID=ALLE&SUCH=&GP=XXIV&ZUFR=ALLE&jsMode=&JMAB=J_JPR_M"

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
      
  def process_page(self,url): 
    pq=PyQuery("%s%s"%(base,url))
    keywords=pq("#schlagwortBox li")
    
    def get_keyword(word):
      try:
        return Keyword.objects.get(word=word)
      except Keyword.DoesNotExist:
        return Keyword(word=word)
    keywords=[get_keyword(r.text_content()) for r in keywords]
    print [i for i in keywords]

