from datetime import datetime

from django.db import models

# Create your models here.

class login(models.Model):
    username = models.CharField(max_length=200)
    password = models.CharField(max_length=20)
    usertype = models.CharField(max_length=20)

class department(models.Model):
    dept = models.CharField(max_length=50)
    
class course(models.Model):
    DEPARTMENT = models.ForeignKey(department, default=1, on_delete=models.CASCADE)
    coursename = models.CharField(max_length=200)

class user(models.Model):
    name = models.CharField(max_length=200)
    COURSE = models.ForeignKey(course, default=1, on_delete=models.CASCADE)
    sem = models.CharField(max_length=20)
    year = models.BigIntegerField()
    photo = models.CharField(max_length=200 ,default=1)
    email = models.CharField(max_length=200 ,default=1)
    LOGIN = models.ForeignKey(login,default=1,on_delete=models.CASCADE)
class post(models.Model):
    post = models.CharField(max_length=50)
    details = models.CharField(max_length=200)
class election(models.Model):
    votingdate = models.CharField(max_length=50)
    campaign = models.CharField(max_length=50)
    publishingdate = models.CharField(max_length=50)
    title = models.CharField(max_length=200)
    lastdatesubmission = models.CharField(max_length=50,default=1)
    status = models.CharField(max_length=50,default='ongoing')
    date = models.CharField(max_length=50,default=datetime.now().date())
class candidates(models.Model):
    USER = models.ForeignKey(user,default=1,on_delete=models.CASCADE)
    POST = models.ForeignKey(post,default=1,on_delete=models.CASCADE)
    details = models.CharField(max_length=200)
    Document = models.CharField(max_length=200,default=1)
    status = models.CharField(max_length=200)
    ELECTION = models.ForeignKey(election,default=1,on_delete=models.CASCADE)
    CCANDIDATE1=models.ForeignKey(user,default=1,on_delete=models.CASCADE,related_name="c1")
    CCANDIDATE2=models.ForeignKey(user,default=1,on_delete=models.CASCADE,related_name="c2")
class rules(models.Model):
    title = models.CharField(max_length=50)
    description = models.CharField(max_length=200)
    date = models.CharField(max_length=200,default=1)

class complaints(models.Model):
    comlaint = models.CharField(max_length=200)
    USER = models.ForeignKey(user,default=1,on_delete=models.CASCADE)
    date = models.CharField(max_length=200)
    time = models.CharField(max_length=200)
    replay = models.CharField(max_length=200)

class result(models.Model):
    result = models.CharField(max_length=200)
    CANDIDATE = models.ForeignKey(candidates,default=1,on_delete=models.CASCADE)

class vote(models.Model):
    time = models.CharField(max_length=20)
    date = models.CharField(max_length=20)
    USER = models.ForeignKey(user, default=1, on_delete=models.CASCADE)
    CANDIDATE = models.ForeignKey(candidates, default=1, on_delete=models.CASCADE)


class otp(models.Model):
    USER = models.ForeignKey(user, default=1, on_delete=models.CASCADE)
    otp = models.BigIntegerField()
    date = models.CharField(max_length=50)


class campaign(models.Model):
    CANDIDATE = models.ForeignKey(candidates, default=1, on_delete=models.CASCADE)
    file = models.CharField(max_length=50)
    type = models.CharField(max_length=50)
    date = models.CharField(max_length=50)
    description = models.CharField(max_length=200)

class review(models.Model):
    USER = models.ForeignKey(user, default=1, on_delete=models.CASCADE)
    review = models.CharField(max_length=200)
    date = models.CharField(max_length=50)

class candidatelogin(models.Model):
    CANDIDATE = models.ForeignKey(candidates, default=1, on_delete=models.CASCADE)
    LOGIN = models.ForeignKey(login, default=1, on_delete=models.CASCADE)

class election_coordinator(models.Model):
    name = models.CharField(max_length=200)
    phno = models.BigIntegerField()
    photo = models.CharField(max_length=200 ,default=1)
    email = models.CharField(max_length=200 ,default=1)
    gender = models.CharField(max_length=200 ,default=1)
    LOGIN = models.ForeignKey(login,default=1,on_delete=models.CASCADE)
