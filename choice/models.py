from django.db import models
from courses.models import Courses
import uuid
# Create your models here.
class Course(models.Model):
    code=models.CharField(max_length=20,verbose_name="code")
    cn=models.CharField(max_length=100,verbose_name="cn")
    credits=models.FloatField(default=0)
    #abc=models.FloatField(default=0)
    crss=models.ForeignKey(Courses, on_delete=models.SET_NULL, null=True,related_name='rlt')
    def __str__(self):
        return self.cn


class Lesson(models.Model):
    code=models.CharField(max_length=20,verbose_name="code")
    teacherAssignmentList=models.JSONField()
    course=models.ForeignKey(Course, on_delete=models.SET_NULL, null=True,related_name='courses')
    select=models.IntegerField(default=0)
    nw=models.JSONField(null=True)
    dateTimePlaceText=models.JSONField(null=True)
    rating=models.IntegerField(default=5)
    def __str__(self):
        return self.code
    class Meta:
        ordering = ['-select','-rating']
    


