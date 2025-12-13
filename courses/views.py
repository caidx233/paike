from django.shortcuts import render
from choice.models import Course,Lesson
from django.shortcuts import redirect
from django.http import HttpResponseRedirect

# Create your views here.
def Detail(request,pk):
    if request.session.get(pk)==None:
        request.session[pk]={'mincredit':0,'maxlesson':0}
    if request.method=='POST':
        request.session[pk]['mincredit']=request.POST['credit']
        request.session[pk]['maxlesson']=request.POST['numb']
        request.session.save()
    keys = list(filter(lambda item: item[1] == pk, request.session.items()))
    keys = [key for key, value in keys]
    key=[]
    for i in keys:
        key.append(Course.objects.get(code=i))
    return render(request,'crs.html',context={'id':request.session[pk],'num':len(keys),'lst':key})
def Add(request,pk):
    request.session['crs']=pk
    request.session.save()
    return redirect('/choice')
def Delete(request,pk):
    keys = list(filter(lambda item: item[1] == pk, request.session.items()))
    keys = [key for key, value in keys]
    for i in keys:
        request.session.pop(i)
    request.session.save()
    return redirect('/')
def New(request):
    if request.session.get('crscnt')==None:
        request.session['crscnt']=0
    request.session['crscnt']+=1
    wh=request.session['crscnt']
    return redirect(f"/courses/{'crs'+str(wh)}")
