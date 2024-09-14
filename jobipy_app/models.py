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
    is_online = models.BooleanField(default=False)
    
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

class Job_Application(models.Model):
    id = models.AutoField(primary_key=True)
    job = models.ForeignKey('Job_Post', on_delete=models.CASCADE, related_name='applied_job')
    applicant = models.ForeignKey('User', on_delete=models.CASCADE, related_name='applicant')
    date_applied = models.CharField(max_length=50)
    status = models.CharField(max_length=100, default='NotViewed')
    status_viewed = models.BooleanField(default=False)
    
    def current_status(self):
        curr_status = ''
        if self.status == 'NotViewed':
            curr_status = 'Waiting for employer to view you application.'
        elif self.status == 'Viewed':
            curr_status = 'Your application has been reviewed by the employer. Please wait for further updates from them.'
        elif self.status == 'Interested':
            curr_status = "The employer is interested in your application. If you haven't been contacted yet, please be patient and wait for further updates."
        elif self.status == 'NotInterested':
            curr_status = "The employer is not interested in your application. While this decision is final, we encourage you to apply for future opportunities that match your qualifications"

        return curr_status
    
class Conversation(models.Model):
    id = models.AutoField(primary_key=True)
    group_name = models.CharField(max_length=50)
    people = models.ManyToManyField('User', related_name='people')
    job = models.ForeignKey('Job_Post', on_delete=models.CASCADE, related_name='job')
    updated = models.CharField(max_length=50)

class Message(models.Model):
    id = models.AutoField(primary_key=True)
    sender = models.ForeignKey('User', on_delete=models.CASCADE, related_name='sender')
    receiver = models.ForeignKey('User', on_delete=models.CASCADE, related_name='receiver')
    conversation = models.ForeignKey('Conversation', on_delete=models.CASCADE, related_name='convo')
    message = models.TextField()
    is_read = models.BooleanField()
    date = models.CharField(max_length=50)
