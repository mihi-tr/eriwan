from django.db import models

# Create your models here.

class Person(models.Model):
  parlid=models.CharField(max_length=16)
  name=models.CharField(max_length=500)
  link=models.CharField(max_length=200)

  def __unicode__(self):
    return name

class Entity(models.Model):
  type=models.CharField(max_length=50)
  name=models.CharField(max_length=100)

  def __unicode__(self):
    return name

class Alias(models.Model):
  entity=models.ForeignKey(Entity)
  name=models.CharField(max_length=100)
  
  def __unicode__(self):
    return "%s -> %s"%(name,entity.name)

class Keyword(models.Model):
  word=models.CharField(max_length=100)

  def __unicode__(self):
    return word

class Question(models.Model):
  parlid=models.CharField(max_length=16)
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
    return name


class Answer(models.Model):
  parlid=models.CharField(max_length=16)
  question=models.ForeignKey(Question)
  data=models.DateField()
  text=models.TextField()
  url=models.CharField(max_length=200)

  def __unicode__(self):  
    return question.name



