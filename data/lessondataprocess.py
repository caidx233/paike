import json
import re
import numpy as np
lsst=[7.5,8.4,9.45,10.35,11.25,14,14.5,15.55,16.45,17.35,19.3,20.2,21.10]
lsed=[8.35,9.25,10.3,11.2,12.1,14.45,15.35,16.4,17.3,18.2,20.15,21.05,21.55]
def prc(s):
    st=s.split('~')[0]
    ed=s.split('~')[1]
    stt=int(st.split(':')[0])+int(st.split(':')[1])/100
    edt=int(ed.split(':')[0])+int(ed.split(':')[1])/100
    x=1
    y=len(lsed)
    for i in range(0,len(lsst)):
        if y==len(lsed) and edt<=lsst[i]:
            y=i
        if (x==1)and  stt>=lsed[len(lsst)-1-i]:
            x=len(lsst)-i+1
        #print(lsed[len(lsst)-1-i])
    return x,y
            
def slv(input_str):
    pattern = r'^(.+):(\d)\((.+)\)$'  # 匹配 x:(y) 格式
    match = re.match(pattern, input_str)
    
    if match:
        x = match.group(1) 
        y = match.group(2) 
        z=match.group(3)
        return x, y,z
    else:
        return None
def inv(x):
    return f'{int(np.floor(x))}:{round((x-np.floor(x))*100):02d}'
#print(prc('14:30~16:40'))
'''
if slv('2404:4(8,9,10)'):
    pass
else:
    print(114514)
'''

with open('lesson.json','r',encoding='utf-8') as file:
    jsn=json.load(file)
nwjsn=[]
lst=["code","dateTimePlaceText","dateTimePlacePersonText","teacherAssignmentList","campus",]
lst.append('nw')
for i in jsn:
    f=1
    tmp_dict={}
    i['course']["credits"]=i["credits"]

    #teacherAssignmentList
    tchr=[]
    for j in i[lst[3]]:
        tchr.append(j['cn'])
    i[lst[3]]=tchr

    #date Time Place Person
    i[lst[2]]=i[lst[2]]['cn']
    i['nw']=[]
    if i[lst[1]]!=None:
        i[lst[2]]=i[lst[2]].replace(' ','')
        i[lst[1]]=i[lst[1]].replace('; \n#1','')
        i[lst[2]]=i[lst[2]].replace(';\n#1','')
        i[lst[1]]=i[lst[1]].split(';')
        nwlst=[]
        for j in i[lst[1]]:
            #dic={'place':j.rsplit(':',1)[0],'time':j.rsplit(':',1)[1]}
            #i['nw'].append(dic)
            j=j.replace(' ','')
            nw=j.replace('\n','')
            nw=nw.replace('\t','')
            i[lst[2]]=i[lst[2]].replace(j,nw)
            nwlst.append(nw)
        i[lst[1]]=nwlst
        i[lst[2]]=i[lst[2]].split('\n')
    else:
        i[lst[1]]=[]
        i[lst[2]]=[]
    for j in i[lst[2]]:
        #j:'week周classroom:day(time)teacher'
        ff=0
        tmpdic={'wk':[]}
        ss=j.split('周')[0]
        tmpdic['week']=ss
        ss=ss.split(',')
        for k in ss:
            if k.find('~')==-1:
                tmpdic['wk'].append(int(k))
            else:
                ds=-1
                if k.find('(单)')!=-1:
                    k=k.replace('(单)','')
                    ds=1
                if k.find('(双)')!=-1:
                    k=k.replace('(双)','')
                    ds=0
                st=int(k.split('~')[0])
                ed=int(k.split('~')[1])
                for num in range(st,ed+1):
                    if (ds==-1) or((num+ds)%2==0):
                        tmpdic['wk'].append(num)
        for k in i[lst[1]]:
            #k:'classroom:day(time)'
            if k in j:
                ff=1
                ret=slv(k)
                tmpdic['classroom']=ret[0]
                tmpdic['day']=ret[1]
                j.replace(k,'$')
                tmpdic['teacher']=j.replace(k,'$').split('$')[-1]
                if ret[2].find('~')!=-1:
                    tmpdic['realtime']=ret[2].split('~')
                    tmpdic['time']=prc(ret[2])
                    if tmpdic['time'][0]==-1 or tmpdic['time'][1]==-1:
                        print('!',i['code'],tmpdic['time'][0],tmpdic['time'][1])
                else:
                    tmpdic['time']=int(ret[2].split(',')[0]),int(ret[2].split(',')[-1])
                    stt=lsst[tmpdic['time'][0]-1]
                    edt=lsed[tmpdic['time'][1]-1]
                    tmpdic['realtime']=[inv(stt),inv(edt)]
                break
        if ff==0:
            ret=slv(i[lst[1]][0])
            tmpdic['day']=ret[1]
            print(i['code'])
        flg=1
        for k in i['nw']:
            if k['week']==tmpdic['week'] and k['time']==tmpdic['time'] and k['day']==tmpdic['day']:
                if (tmpdic['teacher'] in k['teacher'])==0:
                    k['teacher'].append(tmpdic['teacher'])
                flg=0
                break
        if flg==1:
            tmpdic['teacher']=[tmpdic['teacher']]
            i['nw'].append(tmpdic)
            #print(i['code'])
    i[lst[4]]=i[lst[4]]['cn']
    
    for j in lst:
        tmp_dict[j]=i[j]
    for j in nwjsn:
        if j['course']==i['course']:
            j['class'].append(tmp_dict)
            #print(j.course['code'],len(j.classes))
            f=0
            break
    if f==1:
        tmp_course={"course":i['course'],'class':[tmp_dict]}
        nwjsn.append(tmp_course)
res=json.dumps(nwjsn,ensure_ascii=False)

with open('newlesson.json','w',encoding='utf-8') as file:
    file.write(res)



