from decimal import Decimal, InvalidOperation
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
from choice.models import Course
from django.db import connection
def fix_credits_data():
    """
    修复credits字段的无效数据
    """
    with connection.cursor() as cursor:
        # 1. 查看有问题的数据
        cursor.execute("""
            SELECT id, credits 
            FROM choice_course 
            WHERE typeof(credits) != 'real' AND typeof(credits) != 'integer'
        """)
        
        problem_rows = cursor.fetchall()
        print(f"找到 {len(problem_rows)} 条有问题的记录")
        
        
    
    print("✅ 数据修复完成")

# 先修复数据
fix_credits_data()

