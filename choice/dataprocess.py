import os
import django
from django.apps import apps
import json
from paike.models import Course
with open('lesson.json','r',encoding='utf-8') as file:
    jsn=json.load(file)

for i in jsn:
    nw=i['course']
    for key in nw :
        tmp=Course()
        setattr(tmp,key,nw[key])


