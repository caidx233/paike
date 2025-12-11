import os
import sys
import django

# ==================== 第一步：设置路径 ====================
# 获取当前文件的绝对路径
current_file_path = os.path.abspath(__file__)
# 获取项目根目录（paike文件夹）
project_root = os.path.dirname(current_file_path)
# 将项目根目录添加到 Python 路径
sys.path.insert(0, project_root)

# 修改这里的项目名：根据你的实际项目名（settings.py 所在的目录名）
PROJECT_NAME = "paike"  # 或 "your_project_name"，查看你的项目目录名

# 设置环境变量
os.environ.setdefault('DJANGO_SETTINGS_MODULE', f'{PROJECT_NAME}.settings')
django.setup()
from django.apps import apps
import json
from choice.models import Course,Lesson
with open('lesson.json','r',encoding='utf-8') as file:
    jsn=json.load(file)
lists=[]
lessons=[]
for i in jsn:
    nw=i['course']
    tmp=Course()
    for key in nw :
        setattr(tmp,key,nw[key])
    lists.append(tmp)
    nw=i['class']
    for j in nw:
        t=Lesson()
        for key in j:
            setattr(t,key,j[key])
        t.course=tmp
        lessons.append(t)
Course.objects.bulk_create(lists)
Lesson.objects.bulk_create(lessons)


