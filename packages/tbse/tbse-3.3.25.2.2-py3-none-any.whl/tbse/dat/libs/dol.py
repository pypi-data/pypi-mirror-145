import os,sys,tb
tb.std.cls()
c=[]#语句标识
a=[]#参数存储

#running
r=[0]*65536
t=0
s=1

class Usage(Exception):
    def __init__(self,content):
        self.content=content
def aa(count):
    if len(args)-count:
        raise Usage('%s takes %s argument%s, but %i given.'%(key,count or 'no','s' if count-1 else '',len(args)))

print('Do v1.0')
print()
while s:
    s=input('%s>'%(len(c)+1))
    if s:
        c.append(s.split()[0])
        a.append(s.split()[1:])
while -1<t<len(c):
    ct=c[t]
    at=[int(x) for x in a[t]]
    if ct=='set':
        aa(2)
        r[at[0]]=at[1]
    elif ct=='add':
        aa(3)
        r[at[2]]=r[at[0]]+r[at[1]]
    elif ct=='gto':
        aa(3)
        print(r[:5])
        if r[at[0]]==r[at[1]]:
            t+=r[2]
            continue
    elif ct=='shw':
        aa(1)
        print('<',r[at[0]])
    elif ct=='get':
        aa(1)
        r[at[0]]=int(input('\033[32m> \033[0m'))
    else:
        raise Usage('not found')
    t+=1

'''
add 索引 索引 和
set 索引 值
gto 条件 条件 偏移量
shw 位置
get 位置

get 0
get 1
set 2 0
set 3 -1
set 4 0
add 4 0 4
add 1 3 1
gto 1 2 2
gto 0 0 -3
shw 4
'''