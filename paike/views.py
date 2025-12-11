from django.shortcuts import render
from choice.models import Course,Lesson
from courses.models import Courses
from django.shortcuts import redirect
from django.http import HttpResponseRedirect
# Create your views here.
    
def courseDetail(request,code):
    crs=Course.objects.get(code=code)
    return render(request,'course-detail.html',context={'crs':crs,'lessons':crs.courses.filter(select=1),'num':len(crs.courses.filter(select=1))})
def index(request):
    #request.session.flush()
    cnt=0
    if request.session.get('choice')==None:
        request.session['choice']=[]
    if request.method=='POST':
        lessons=request.POST.getlist('lessons')
        cnt=0
        if lessons !=[]:
            crs=Course.objects.get(code=lessons[0].split('.')[0])
            for i in crs.courses.all():
                i.select=0
                i.save()
            for i in lessons:
                lesson = Lesson.objects.get(code=i)
                lesson.select = 1
                lesson.rating=request.POST[str(i)]
                lesson.save()
            if (crs.code in request.session['choice'])==0:
                if request.session.get('crs')==None:
                    if crs.crss==None:
                        request.session['choice'].append(crs.code)
                        request.session.save()
                else:
                    pk=request.session['crs']
                    crs.crss=Courses.objects.get(id=pk)
                    crs.save()
                    request.session['crs']=None
                    request.session.save()
                    return redirect(f'/courses/{pk}')
        elif request.session.get('crs')!=None:
            pk=request.session['crs']
            return redirect(f'/courses/{pk}')
    else:
        cnt=2
    pst=[]
    for i in request.session['choice']:
        pst.append(Course.objects.get(code=i))
    psts=[]
    for i in Courses.objects.all():
        if len(i.rlt.all())!=0:
            psts.append(i)
    return render(request,'index.html',context={'choice':pst,'cc':cnt,'num':len(pst),'choices':psts,'nums':len(psts)})
def delete(request,code):
    if code in request.session['choice']:
        request.session['choice'].remove(code)
        request.session.save()
    nw=Course.objects.get(code=code)
    if nw.crss != None:
        nw.crss=None
        nw.save()
    return redirect('/')
