from django.shortcuts import render
from choice.models import Course,Lesson
from django.shortcuts import redirect
from django.http import HttpResponseRedirect
# Create your views here.
    
def courseDetail(request,code):
    crs=Course.objects.get(code=code)
    selected=[]
    rating=[]
    for i in crs.courses.all():
        if request.session.get(i.code)!=None:
            i.rating=request.session[i.code]
            selected.append(i)
    return render(request,'course-detail.html',context={'crs':crs,'lessons':selected,'num':len(selected),"rating":rating})
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
                request.session.pop(i.code, None)
            for i in lessons:
                request.session[str(i)]=request.POST[str(i)]
            request.session.save()
            if (crs.code in request.session['choice'])==0:
                if request.session.get('crs')==None:
                    if request.session.get(crs.code)==None:
                        request.session['choice'].append(crs.code)
                        request.session.save()
                else:
                    pk=request.session['crs']
                    request.session[crs.code]=pk
                    request.session.pop('crs')
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
    if request.session.get('crscnt')==None:
        request.session['crscnt']=0
    request.session.pop('crs',None)
    for i in range(request.session['crscnt']):
        keys = list(filter(lambda item: item[1] == ('crs'+str(i+1)), request.session.items()))
        keys = [key for key, value in keys]
        if len(keys)!=0:
            tmp=[]
            for j in keys:
                tmp.append(Course.objects.get(code=j))
            psts.append({'rlt':tmp,'id':('crs'+str(i+1))})
    return render(request,'index.html',context={'choice':pst,'cc':cnt,'num':len(pst),'choices':psts,'nums':len(psts)})
def delete(request,code):
    if code in request.session['choice']:
        request.session['choice'].remove(code)
        request.session.save()
    nw=Course.objects.get(code=code)
    request.session.pop(code,None)
    request.session.save()
    return redirect('/')
