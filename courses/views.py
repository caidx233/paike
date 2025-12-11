from django.shortcuts import render
from choice.models import Course,Lesson
from courses.models import Courses
from django.shortcuts import redirect
from django.http import HttpResponseRedirect

# Create your views here.
def Detail(request,pk):
    if request.method=='POST':
        wh=Courses.objects.get(id=pk)
        wh.mincredit=request.POST['credit']
        wh.maxlesson=request.POST['numb']
        wh.save()
    ret=Courses.objects.get(id=pk)
    return render(request,'crs.html',context={'id':ret,'num':len(ret.rlt.all())})
def Add(request,pk):
    request.session['crs']=str(pk)
    request.session.save()
    return redirect('/choice')
def Delete(request,pk):
    wh=Courses.objects.get(id=pk)
    wh.delete()
    return redirect('/')
def New(request):
    nwcrs=Courses()
    nwcrs.save()
    return redirect(f"/courses/{nwcrs.id}")
