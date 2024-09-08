from django.db import models

import hashlib

# # Create your models here.

class User(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    email = models.CharField(max_length=254)
    password = models.CharField(max_length=128)
    contact_number = models.CharField(max_length=50)
    city = models.CharField(max_length=50)
    resume = models.FileField(upload_to='resumes/')
    resume_image = models.TextField()
    
    def __str__(self): 
        return self.name
    
    def set_password(self, password):
        password_hash = hashlib.sha256(password.encode("utf-8")).hexdigest()
        self.password = password_hash
    
    def check_password(self, password):
        password_hash = hashlib.sha256(password.encode("utf-8")).hexdigest()
        if self.password == password_hash:
            return self.password
        else:
            return None

class Preferences(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.OneToOneField('User', on_delete=models.CASCADE, related_name='user_preferences')
    industry = models.CharField(max_length=50)
    minimum_base_pay = models.CharField(max_length=50)
    per = models.CharField(max_length=50)
    job_type = models.JSONField()

class Job_Post(models.Model):
    id = models.AutoField(primary_key=True)
    poster = models.ForeignKey('User', on_delete=models.CASCADE, related_name='job_poster')
    industry = models.CharField(max_length=50)
    job_title = models.CharField(max_length=50)
    company = models.CharField(max_length=50)
    job_description = models.TextField()
    city = models.CharField(max_length=50)
    pay = models.CharField(max_length=50)
    per = models.CharField(max_length=50)
    job_type = models.JSONField()
    date_posted = models.CharField(max_length=50)
    users_applied = models.ManyToManyField('User', related_name='users_applied')

class Conversation(models.Model):
    id = models.AutoField(primary_key=True)
    group_name = models.CharField(max_length=50)
    people = models.ManyToManyField('User', related_name='people')
    job = models.ForeignKey('Job_Post', on_delete=models.CASCADE, related_name='job')
    messages = models.ManyToManyField('Message', related_name='messages')

class Message(models.Model):
    id = models.AutoField(primary_key=True)
    sender = models.ForeignKey('User', on_delete=models.CASCADE, related_name='sender')
    receiver = models.ForeignKey('User', on_delete=models.CASCADE, related_name='receiver')
    message = models.TextField()
    is_read = models.BooleanField()
    date = models.CharField(max_length=50)
