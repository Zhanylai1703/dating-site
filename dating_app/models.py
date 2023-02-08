from django.db import models
import re
# Create your models here.
class UserManager(models.Manager):
    def basic_validator(self, post_data):
        errors={}
        email_regex = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if not email_regex.match(post_data['email']):
            errors['email']='Пожалуйста, введите действующий адрес электронной почты'

        if len(post_data['first_name'])<2:
            errors['first_name']='Имя должно быть не менее 2 символов'
        if len(post_data['first_name'])>50:
            errors['first_name']='Имя должно содержать менее 50 символов.'

        if len(post_data['last_name'])<2:
            errors['last_name']='Фамилия должна быть не менее 2 символов.'
        if len(post_data['last_name'])>50:
            errors['last_name']='Фамилия должна содержать менее 50 символов.'
        
        try: 
            User.objects.get(email=post_data['email'])
            errors ['email']="Такой адрес электронной почты уже используется"
        except:
            pass
        
        if len(post_data['password'])<3:
            errors['password']='Пароль должен быть не менее 3 символов'
        if post_data['password'] != post_data ['confirm_password']:
            errors['confirm_password']='Пароли не совпадают'
        if len(post_data['description'])>255:
            errors['description']='Описание должно быть меньше 255 символов'
        return errors

    def info_validator(self, post_data, user):
        errors={}
        email_regex = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if not email_regex.match(post_data['email']):
            errors['email']='Пожалуйста, представьте действующий адрес электронной почты'

        if len(post_data['first_name'])<2:
            errors['first_name']='Имя должно быть не менее 2 символов'
        if len(post_data['first_name'])>50:
            errors['first_name']='Имя должно содержать менее 50 символов.'

        if len(post_data['last_name'])<2:
            errors['last_name']='Фамилия должна быть не менее 2 символов'
        if len(post_data['last_name'])>50:
            errors['last_name']='Фамилия должна содержать менее 50 символов.'
        
        if  user.email != post_data['email'] and User.objects.get(email = post_data['email']):
            errors ['email']="Такой адрес электронной почты уже используется"
        if user.age <18: 
            errors ['age']='Ты еще маленький'
        if len(post_data['nickname'])<2:
            errors['nickname']='Никнейм должен быть не менее 2 символов'
        if len(post_data['nickname'])>50:
            errors['nickname']='Никнейм должен быть меньше 50 символов'

        return errors

    def description_validator(self, post_data):
        errors={}
        if len(post_data['description'])>255:
            errors['description']='Описание должно быть меньше 255 символов'
        return errors


    def password_validator(self, post_data):
        errors={}
        if len(post_data['password'])<3:
            errors['password']='Пароль должен быть не менее 3 символов'
        if post_data['password'] != post_data['confirm_password']:
            errors['confirm_password']='Неверный пароль'
        return errors



class MessageManager(models.Manager):
    def messageValidator(self, post_data):
        errors={}
        if len(post_data['message'])<2:
            errors['message'] = 'Сообщение должно быть не менее 2 символов.'
        return errors



class User(models.Model):
    first_name=models.CharField(max_length=60)
    last_name=models.CharField(max_length=60)
    description = models.TextField(max_length=255)
    admin=models.BooleanField()
    email=models.CharField(max_length=254)
    age=models.IntegerField()
    nickname=models.CharField(max_length=60)
    photo=models.ImageField(upload_to='profile_images', blank=True, null=True)
    gender=models.BooleanField()
    password=models.CharField(max_length=255)
    likes = models.ManyToManyField('User', related_name="matches")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects=UserManager()

class Message(models.Model):
    message=models.TextField()
    user=models.ForeignKey(User, related_name='messages', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects=MessageManager()


