import json
with open('lesson.json','r',encoding='utf-8') as file:
    jsn=json.load(file)
tot=[]
s='dateTimePlaceText'
t="dateTimePlacePersonText"
for i in jsn:
    for j in i['class']:
        if j[s]==None:
            j[s]=[]
        else:
            j[s]=j[s].split(';')
        tmp=[]
        tmp0=[]
        for k in j[s]:
            st=k.split(':',1)[-1].strip()
            if (st in tmp)==0:
                tmp.append(st)
        for k in j[t]:
            #if ('周' in k)==0:
            #    print(j['code'])
            x=k.split('周')[0]
            mp=[]
            for l in tmp:
                if (l.strip() in k.strip()):
                    mp.append(l)
                    tmp0.append({'week':x,'time':l})
            if len(mp)!=1:
                print(j['code'])
            #if (tmp[-1] in tot)==0:
             #   tot.append(tmp[-1])
                #print(j['code'],tmp[-1])
        j['time']=tmp0
        #if i['course']['code']=='MATH1006':
         #   print(j['campus'])

res=json.dumps(jsn,ensure_ascii=False)

with open('newlesson.json','w',encoding='utf-8') as file:
    file.write(res)

