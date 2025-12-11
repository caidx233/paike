from django.db import models
import uuid
# Create your models here.
class Courses(models.Model):
    id=models.UUIDField(primary_key=True, default=uuid.uuid4,editable=False)
    mincredit=models.FloatField(default=0)
    maxlesson=models.IntegerField(default=100)
