from django.shortcuts import render
from choice.models import Course,Lesson
from django.shortcuts import redirect
from django.http import HttpResponseRedirect
import numpy as np
# Create your views here.
crsall=[]
lst=[]
fa=[]
ret=1
lsst=[7.5,8.4,9.45,10.35,11.25,14,14.5,15.55,16.45,17.35,19.3,20.2,21.10]
lsed=[8.35,9.25,10.3,11.2,12.1,14.45,15.35,16.4,17.3,18.2,20.15,21.05,21.55]
def inv(x):
    return f'{int(np.floor(x))}:{round((x-np.floor(x))*100):02d}'
def solve(nw,request):
    if nw>=len(crsall):
        return 1
    for i in Course.objects.get(code=crsall[nw]).courses.all():
        if request.session.get(i.code)==None:
            continue
        f=1
        for j in i.nw:
            for k in j['wk']:
                for l in j['time']:
                    if (k,j['day'],l) in lst:
                        f=0
        if f==1:
            for j in i.nw:
                for k in j['wk']:
                    for l in j['time']:
                        lst.append((k,j['day'],l))
            fa.append(i)
            if solve(nw+1,request)==1:
                return 1
            fa.remove(i)
            for j in i.nw:
                for k in j['wk']:
                    for l in j['time']:
                        lst.remove((k,j['day'],l))
    return 0
def transfr():
    global fa,ret
    dic={'1':{},'2':{},'3':{},'4':{},'5':{},'6':{},'7':{},'8':{},'9':{},'10':{},'11':{},'12':{},'13':{}}
    global lst
    ret+=1
    for i in fa:
        for j in i.nw:
            k=j
            lst.append(1)
            ret+=1
            k['code']=i.code
            k['cn']=i.course.cn
            k['start']=j['realtime'][0]
            k['end']=j['realtime'][1]
            k['range']=j['time'][1]-j['time'][0]+1
            k['printt']= f'{j['time'][0]},{j['time'][1]}'
            dic[str(k['time'][0])][k['day']]=k
    return dic
def slv(request):
    global lst,fa,crsall
    lst.clear()
    fa.clear()
    crsall=request.session.get('choice')
    solve(0,request)
    tmp=transfr()
    crs=[]
    for tot in '123':
        nwdic={'name':'s'+tot}
        main=[]
        sprd='12345'
        if tot=='2':
            sprd=['6','7','8','9','10']
        if tot=='3':
            sprd=['11','12','13']
        for prd in sprd:
            ll=[]
            for i in '1234567':
                if tmp[prd].get(i)!=None:
                    ll.append(tmp[prd][i])
                else:
                    ll.append(None)
            main.append({'num':prd,'st':inv(lsst[int(prd)-1]),'ed':inv(lsed[int(prd)-1]),'main':ll})
        nwdic['main']=main
        crs.append(nwdic)
    return render(request,'result.html',context={'fa':fa,'num':ret,'cls':crs})
    
