from django.shortcuts import render
from choice.models import Course,Lesson
from django.shortcuts import redirect
from django.http import HttpResponseRedirect
import numpy as np
# Create your views here.
crsall=[]
lst=[]
fa=[]
cfa=[]
lsn=[]
mxrt=int(-1e10)
greq=None
ret=1
lsst=[7.5,8.4,9.45,10.35,11.25,14,14.5,15.55,16.45,17.35,19.3,20.2,21.10]
lsed=[8.35,9.25,10.3,11.2,12.1,14.45,15.35,16.4,17.3,18.2,20.15,21.05,21.55]
def inv(x):
    return f'{int(np.floor(x))}:{round((x-np.floor(x))*100):02d}'
def getpr(x):
    return int(greq.session[str(x)])
def pre():
    global lsn,mxrt
    lsn.clear()
    for i in crsall:
        temp=[]
        for j in Course.objects.get(code=i).courses.all():
            if greq.session.get(j.code)!=None:
                temp.append(j)
        temp.sort(key=getpr,reverse=True)
        lsn.append(temp)
def solve(nw,ss):
    global mxrt,fa,cfa
    if nw>=len(lsn):
        mxrt=ss
        fa=cfa.copy()
        return 1
    srem=0
    for i in range(nw+1,len(lsn)):
        srem+=getpr(lsn[i][0])
    for i in lsn[nw]:
        f=1
        if ss+srem+getpr(i)<=mxrt:
            break
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
            cfa.append(i)
            solve(nw+1,ss+getpr(i))
            cfa.remove(i)
            for j in i.nw:
                for k in j['wk']:
                    for l in j['time']:
                        lst.remove((k,j['day'],l))
    return 0
tstret=[]
def solve2(nw):
    global crsall,tstret
    if nw>=greq.session['crscnt']:
        pre()
        solve(0,0)
        return
    pk='crs'+str(nw+1)
    keys = list(filter(lambda item: item[1] == pk, greq.session.items()))
    keys = [key for key, value in keys]
    if len(keys)!=0:
        crd=float(greq.session[pk]['mincredit'])
        lssn=int(greq.session[pk]['maxlesson'])
        for msk in range(2**len(keys)):
            if bin(msk).count('1')<=lssn:
                ccnt=0
                for i in range(len(keys)):
                    if (1<<i) & msk:
                        crsall.append(keys[i])
                        ccnt+=Course.objects.get(code=keys[i]).credits
                if ccnt>=crd:
                    tstret.append(crsall.copy())
                    solve2(nw+1)
                for i in range(len(keys)):
                    if (1<<i) & msk:
                        crsall.remove(keys[i])
    else:
        solve2(nw+1)

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
    global lst,fa,crsall,greq,cfa,mxrt
    mxrt=-1e10
    greq=request
    lst.clear()
    fa.clear()
    cfa.clear()
    crsall=request.session.get('choice')
    #pre()
    #solve(0,0)
#sort lessons
    solve2(0)
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
    return render(request,'result.html',context={'fa':fa,'num':ret,'cls':crs,'tst':tstret})
