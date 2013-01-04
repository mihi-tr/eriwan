from django.db import models

# Create your models here.

class Person(models.Model):
  parlid=models.CharField(max_length=16,unique=True)
  name=models.CharField(max_length=500)
  link=models.CharField(max_length=200)

  def __unicode__(self):
    return self.name

class Entity(models.Model):
  type=models.CharField(max_length=50)
  name=models.CharField(max_length=100)

  def __unicode__(self):
    return self.name

class Alias(models.Model):
  entity=models.ForeignKey(Entity)
  name=models.CharField(max_length=100)
  
  def __unicode__(self):
    return "%s -> %s"%(self.name,self.entity.name)

class Keyword(models.Model):
  word=models.CharField(max_length=100,unique=True)

  def __unicode__(self):
    return self.word

class Question(models.Model):
  parlid=models.CharField(max_length=16,unique=True)
  name=models.CharField(max_length=1024)
  asker=models.ForeignKey(Person,related_name="asking")
  asked=models.ForeignKey(Person,related_name="asked")
  text=models.TextField()
  date=models.DateField()
  deadline=models.DateField()
  keywords=models.ManyToManyField(Keyword)
  entities=models.ManyToManyField(Entity,null=True,blank=True)
  url=models.CharField(max_length=200)

  def __unicode__(self):
    return self.name

class Distance(models.Model):
  src=models.ForeignKey(Question,related_name="src")
  dst=models.ForeignKey(Question,related_name="dst")
  distance=models.FloatField()

class Answer(models.Model):
  parlid=models.CharField(max_length=16,unique=True)
  question=models.ForeignKey(Question)
  date=models.DateField()
  text=models.TextField()
  url=models.CharField(max_length=200)

  def __unicode__(self):  
    return self.question.name



class TermCount(models.Model):
  count=models.IntegerField()
  term=models.CharField(max_length=500)
  question=models.ForeignKey(Question)

class NotableTerms(models.Model):
  term=models.CharField(max_length=500)
  question=models.ForeignKey(Question)

