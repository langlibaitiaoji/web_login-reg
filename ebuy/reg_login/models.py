from django.db import models
# Create your models here.


class User(models.Model):
    user_phone = models.CharField(primary_key=True, max_length=11)
    user_password = models.CharField(max_length=35)
    user_nickname = models.CharField(max_length=30)
    user_pic = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        db_table = 'user'


class Secure(models.Model):
    user_verify_question = models.CharField(max_length=40)
    user_verify_answer = models.CharField(max_length=40)
    user_to = models.ForeignKey(to=User, related_name='user_verify', on_delete=models.CASCADE)

    class Meta:
        db_table = 'user_verify'
