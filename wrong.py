from decimal import Decimal, InvalidOperation
from django.shortcuts import render
from django.http import HttpResponseRedirect
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
from django.db import connection

def truncate_table(Object):
    """
    使用 TRUNCATE 或 DELETE 清空整个表（最快的方法）
    """
    table_name = Object._meta.db_table  # 通常是 "choice_course"
    
    with connection.cursor() as cursor:
        # 方法1: 使用 DELETE（可回滚）
        cursor.execute(f"DELETE FROM {table_name}")
        
        # 方法2: SQLite 使用 DELETE + 重置自增（推荐）
        #cursor.execute(f"DELETE FROM {table_name}")
        #cursor.execute(f"DELETE FROM sqlite_sequence WHERE name='{table_name}'")
        
        print(f"✅ 已清空表 {table_name}")
    
    # 验证
    print(f"剩余记录数: {Course.objects.count()}")

truncate_table(Lesson)
truncate_table(Course)
