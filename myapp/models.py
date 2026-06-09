from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Customer(models.Model):
    name = models.CharField(max_length=100)
    photo=models.CharField(max_length=100)
    email=models.CharField(max_length=100)
    phone=models.CharField(max_length=100)
    gender=models.CharField(max_length=100)
    dob=models.CharField(max_length=100)
    place=models.CharField(max_length=100)
    bio=models.CharField(max_length=100)
    profilephoto=models.CharField(max_length=500,default='')
    USER=models.OneToOneField(User,on_delete=models.CASCADE)


class Complaints(models.Model):
    complaint= models.CharField(max_length=100)
    date = models.DateField()
    reply = models.CharField(max_length=100)
    status = models.CharField(max_length=100)
    CUSTOMER=models.ForeignKey(Customer,on_delete=models.CASCADE)

class Review(models.Model):
    date = models.CharField(max_length=100)
    review = models.CharField(max_length=100)
    rating = models.CharField(max_length=100)
    CUSTOMER=models.ForeignKey(Customer,on_delete=models.CASCADE)

class Post(models.Model):
    file =models.CharField(max_length=500)
    date=models.CharField(max_length=100)
    description=models.CharField(max_length=100)
    caption=models.CharField(max_length=100)
    place=models.CharField(max_length=100)
    like=models.CharField(max_length=100,default='0')
    CUSTOMER=models.ForeignKey(Customer,on_delete=models.CASCADE)


class Request(models.Model):
    date=models.DateField()
    status=models.CharField(max_length=100)
    Fromr=models.ForeignKey(User,on_delete=models.CASCADE,related_name="fromid")
    Tor=models.ForeignKey(User,on_delete=models.CASCADE,related_name="toid")


class Comments(models.Model):
    comment=models.CharField(max_length=100)
    date=models.DateField()
    POST=models.ForeignKey(Post,on_delete=models.CASCADE)
    status=models.CharField(max_length=100)
    CUSTOMER=models.ForeignKey(Customer,on_delete=models.CASCADE)

class Chat(models.Model):
    FROMID = models.ForeignKey(User, on_delete=models.CASCADE,related_name='fuser')
    TOID = models.ForeignKey(User, on_delete=models.CASCADE,related_name='tfuser')
    message=models.CharField(max_length=200)
    date = models.DateField()


class Notification():
    notification=models.CharField(max_length=100)
    date=models.DateField()
    time=models.TimeField()
    status=models.CharField(max_length=100)
    POST=models.ForeignKey(Post,on_delete=models.CASCADE)



class EducationalContents(models.Model):
    date=models.DateField()
    time=models.TimeField()
    content=models.CharField(max_length=100)
    type=models.CharField(max_length=100)


class PostNotification(models.Model):
    POST =models.ForeignKey(Post, on_delete=models.CASCADE)
    USER = models.ForeignKey(Customer, on_delete=models.CASCADE)
    status = models.CharField(max_length=100)
    date = models.DateField()
    bottom= models.CharField(max_length=100)
    left= models.CharField(max_length=100)
    right=models.CharField(max_length=100)
    top=models.CharField(max_length=100)

class Likes(models.Model):
    POST =models.ForeignKey(Post, on_delete=models.CASCADE)
    USER = models.ForeignKey(Customer, on_delete=models.CASCADE)