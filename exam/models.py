from django.db import models
import re
import bcrypt

# Create your models here.
class UserManager(models.Manager):
    def basic_validator(self, postData):
        errors = {}
        if len(postData['name']) < 5:
            errors['name'] = "Name should be at least 5 characters long"
        users = User.objects.all()
        for user in users:
            if postData['email'] == user.email:
                errors['unique'] = "This email is already taken"
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if not EMAIL_REGEX.match(postData['email']):
            errors['email'] = "Invalid email address"
        if len(postData['password']) < 8:
            errors['password'] = "Password should be 8 characters long"
        if postData['password'] != postData['pwdconfirm']:
            errors['confirm'] = "Password not the same, try again"
        return errors
    
    def login_validator(self, postData2):
        errors2 = {}
        email2 = postData2['email2']
        password2 = postData2['password2']
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if not EMAIL_REGEX.match(postData2['email2']):
            errors2['email2'] = "Invalid email address"
        users = User.objects.filter(email = email2)
        if users:
            logged_user = users[0]
            if not bcrypt.checkpw(password2.encode(), logged_user.password.encode()):
                errors2['password2'] = "Wrong password, try again"
        return errors2
    

class TeamManager(models.Manager):
    def team_validator(self, PostData3):
        errors3 = {}
        if len(PostData3['name']) < 3:
            errors3['name'] = "Team name should be at least 3 characters long"
        if int(PostData3['skill']) < 1 or int(PostData3['skill']) > 5:
            errors3['skill'] = "skill can't be less that 1 or higher than 5"
        return errors3


class User(models.Model):
    username = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()

    def __str__(self):
        return f"{self.username}"


class Team(models.Model):
    name = models.CharField(max_length = 255)
    skill = models.IntegerField()
    day = models.CharField(max_length = 255)
    created_by = models.ForeignKey(User, related_name='users', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = TeamManager()

    def __str__(self):
        return f"{self.name}"