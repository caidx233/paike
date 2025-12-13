from django.shortcuts import render
from choice.models import Course,Lesson
# Create your views here.
def findCourse(request):
    cde=request.GET.get('code')
    nme=request.GET.get('name')
    if cde==None:
        return render(request,'find-course.html',context={'courses':[],'code':request.method})
    if cde!="":
        lists=Course.objects.filter(code=cde)
    else:
        lists=Course.objects.filter(cn__contains=nme)
    return render(request,'find-course.html',context={'courses':lists,'num':len(lists)})

    
def choose(request,code):
    
    nw=Course.objects.get(code=code)
    lesson=nw.courses.all()
    for i in lesson:
        if request.session.get(i.code):
            i.rating=request.session[i.code]
            i.select=1
        else:
            i.rating=5
            i.select=0
    return render(request,'lesson-choose.html',context={'courses':nw,"num":len(lesson),"lessons":lesson})
