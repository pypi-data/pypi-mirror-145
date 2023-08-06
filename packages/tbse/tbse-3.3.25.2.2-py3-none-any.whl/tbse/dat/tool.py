'''
/**
  * tool.py 
  * For cmd+(0.3~0.6)
  * Copyright: laman29:lmfs (some indevidual exceptions)
  * Run 'setup.py' at first
  */
'''

dbg=0

#import
import tb,os,sys,re,traceback,time,random,socket,subprocess,getpass
from libs import txts
from tb.std import print,input

#setup
dbg=dbg or (len(sys.argv)>1 and sys.argv[1]=='-v')
NAME='tool'+txts.get('version')
PARENT_DIR=os.sep.join(sys.argv[0].split(os.sep)[:-1])
insh=False
inbbx=False
inread=False
insdb=False
sh_erc=0
unix=os.name=='posix'
ps='sh' if unix else 'win'
af=time.strftime('%m%d')=='0401'
sdb=None
fs=[]
cmdcache=[]
var={}
home='/data/data/com.hipipal.qpy3/files/home'
cd='/'
last_cd=cd
pslist={
    'ba':lambda:'\033[91m[\033[93m$%s$\033[91m@\033[34mhey \033[96m%s%shey\033[91m]\033[92mno tbse! \033[0m'%(getpass.getuser(),cd,os.sep),
    'no':lambda:'\033[92m # ',
    'sh':lambda:'\033[34mhey\033[91m:\033[96m%s%shey \033[92mno tbse! \033[0m'%(cd,os.sep),
    'win':lambda:'\033[96m%s%shey\033[92m< \033[0m'%(cd,os.sep),
    'z':lambda:'\033[40;93m$%s$\033[90m@hey \033[0;46m█ %s%shey \033[0;96m→ \033[0m'%(getpass.getuser(),cd,os.sep)
} if af else {
    'ba':lambda:'\033[91m[\033[93m%s\033[91m@\033[34m%s \033[96m%s\033[91m]\033[92m$ \033[0m'%(getpass.getuser(),NAME,cd),
    'no':lambda:'\033[92m $ ',
    'sh':lambda:'\033[34m%s\033[91m:\033[96m%s \033[92m$ \033[0m'%(NAME,cd),
    'win':lambda:'\033[96m%s\033[92m> \033[0m'%cd,
    'z':lambda:'\033[40;93m%s\033[90m@%s \033[0;46m▶ %s \033[0;96m▶ \033[0m'%(getpass.getuser(),NAME,cd)
}
sh_pre_def=lambda:('''
    alias cp='cp -i'
    alias l.='ls -d .* --color=auto'
    alias ll='ls -l --color=auto'
    alias ls='ls --color=auto'
    alias mv='mv -i'
    alias rm='rm -i'
    alias vi='vim'
    alias which='alias | which --tty-only --read-alias --show-dot --show-tilde'
    PS1='%s'
'''%(pslist[ps]())
if unix else '''
    sh
    prompt %s
'''%(pslist[ps]())
)
alias={
    'bash':'sh bash',
    'bbx':'busybox',
    'cls':'sh clear' if unix else 'sh cls',
    'cmd':'sh cmd+',
    'insh':'sh --on',
    '666':'sh echo -e "\\xe"' if unix else '',
    '000':'sh echo -e "\\xfok."' if unix else 'echo ok.'
}

#setup for os
if unix:
    if os.path.isdir('/sdcard'):
        pd='/sdcard'
    else:
        pd='/usr'
else:
    pd='/User'

#define
class Usage(BaseException):
    def __init__(self,content):
        self.content=content
def c(*w):
    return key in w
def aa(count):
    if type(count)==int:
        if len(args)-count:
            raise Usage('%s takes %i argument%s, but %i given.'%(key,count or 'no','s' if count-1 else '',len(args)))
    elif type(count)==tuple:
        if len(args) not in count:
            raise Usage('%s takes %i arguments, but %i given.'%(key,' or '.join(count),len(args)))
    elif type(count)==range:
        if len(args) not in count:
            raise Usage('%s takes %i~%i arguments, but %i given.'%(count.start,count.stop,len(args)))

#main
if af:
    cmdcache.extend(('666','insh'))
    tb.std._norm='100;35'
    tb.std.cls()
    dbg=1
if sys.argv[0]:
    if len(sys.argv)>1:
        endexit=True
        af=False
        sa1=lambda *x:sys.argv[1] in x
        if sa1('-V'):
            print(NAME)
        elif sa1('-c'):
            _=''
            for _c,a in (((x,_) if x.find(':')==-1 else (x[:x.find(':')],x[x.find(':')+1:])) for x in sys.argv[2:]):
                if _c=='cmd':
                    cmdcache.append(a)
                elif _c=='psml':
                    pass#
        elif sa1('-v'):
            dbg=1
            endexit=False
        else:
            for x in sys.argv[1:]:
                cmdcache.append('run '+x)
    else:
        endexit=False
if not endexit:
    tb.std.cls()
    print('\033[1;96mWelcome to use Too%sox%s!'%('bl' if af else 'lb',txts.get('version')))
    print('\033[0;33mlaman29:lmfs(c)2022')
    print('\033[94mType "help" to get some information!\033[0m')
    if dbg:
        print('[dbg on]')
    print()
while 1:
    try:
        try:
            os.chdir(cd)
            if cmdcache:
                s=cmdcache.pop(0)
            else:
                if insdb:
                    s=sdb.recv()[1]
                elif inread:
                    s=fs[-1].readline()
                    if not s:
                        fs[-1].close()
                        fs.pop()
                        if not fs:
                            inread=False
                        continue
                else:
                    print(end='\033[0m')
                    if insh:
                        if sh_erc:
                            print(sh_erc,end='|')
                        s=input(pslist[ps]())
                    elif inbbx:
                        if af:
                            s=input('busbyox %s→ '%cd)
                        else:
                            s=input('busybox %s> '%cd)
                    elif endexit:
                        exit(256)
                    elif af:
                        s=input('==》 ')
                    else:
                        s=input('--> ')
                if not insh and not inbbx:
                    if ';' in s:
                        s=s[:s.index(';')]
                    cmdcache=s.split('&')
                    s=cmdcache.pop(0)
            s=re.sub('\s+',' ',s)
            if insh:
                s='sh '+s
            elif inbbx:
                s='sh busybox '+s
            try:
                key=s.split()[0]
            except IndexError:
                continue
            if key in alias.keys():
                if dbg:
                    print('(alias in)')
                s=' '.join((alias[key],*(s.split()[1:])))
                key=s.split()[0]
            allstr=' '.join(s.split()[1:])
            swch,bgsw,args='',[],[]
            if not insh and not inbbx:
                splall=[]
                tmp=''
                _pc=0
                instr=0
                while _pc<len(allstr):
                    x=allstr[_pc]
                    if instr:
                        if x=='#':
                            _pc+=1
                            x=allstr[_pc]
                            if x=='q':
                                tmp+="'"
                            elif x=='a':
                                tmp+='&'
                            elif x=='#':
                                tmp+=x
                            elif x=='.':
                                tmp+=' '
                            elif x=='x':
                                tmp+=chr(int(allstr[_pc+1:_pc+3],16))
                                _pc+=2
                            elif x=='u':
                                tmp+=chr(int(allstr[_pc+1:_pc+5],16))
                                _pc+=4
                            else:
                                raise Usage('unexpected escape character: %s'%x)
                        elif x=="'":
                            instr=0
                        else:
                            tmp+=x
                    elif x==' ':
                        splall.append(tmp)
                        tmp=''
                    elif x=="'":
                        instr=1
                    elif x=='~':
                        tmp+=home
                    else:
                        tmp+=x
                    _pc+=1
                if tmp:
                    splall.append(tmp)
                    tmp=''                    
            else:
                splall=allstr.split()
            allstr=' '.join(splall)
            for x in splall:
                if x.startswith('--') and x!='--':
                    bgsw.append(x[2:])
                elif x.startswith('-') and x!='-':
                    swch+=x[1:]
                else:
                    args.append(x)
            argstr=' '.join(args)
            if dbg:
                print('s:',s,'\nkey:',key,'\nswch:',swch,'\nbgsw:',bgsw,'\nargs:',args)
            if c('rainbow') or not (inread or insdb or endexit or random.randint(0,255)):
                while 1:
                    print('\033[?25l\033[%sm%s'%(random.randint(101,106),' '*os.get_terminal_size().columns*os.get_terminal_size().lines))
                    time.sleep(.2)
            elif c('alias'):
                if not allstr:
                    for k,v in alias.items():
                        print(k+'='+v)
                elif '=' in allstr:
                    alias[allstr.split('=')[0]]=allstr[allstr.index('=')+1:]
                else:
                    if allstr in alias:
                        print(alias[allstr])
                    else:
                        raise Usage("alias:not found '%s'"%allstr)
            elif c('busybox'):
                if 'on' in bgsw:
                    inbbx=True
                else:
                    os.system('busybox '+allstr)
            elif c('clearqq'):
                aa(0)
                tb.exe.exe(txts.get('path')+os.sep.join(' Run libs clearqq.py'.split(' ')))
            elif c('do'):
                aa(0)
                try:
                    tb.exe.exe(txts.get('path')+os.sep.join(' Run libs dol.py'.split(' ')))
                except:
                    print('Can not open do launcher.')
            elif c('echo'):
                print(allstr)
            elif c('exit'):
                if insdb:
                    sdb.send(0)
                    sdb.close('s')
                    insdb=False
                if inread:
                    fs[-1].close()
                    fs.pop()
                    if not fs:
                        inread=False
                elif allstr:
                    sys.exit(int(allstr))
                else:
                    sys.exit(256)
            elif c('help'):
                aa(0)
                print()
                print(txts.get('hlp'))
                print('Alias:')
                cmdcache.insert(0,'alias')
            elif c('home'):
                home=allstr
            elif c('input'):
                aa(0)
                input()
            elif c('int','str','bln'):
                _k=allstr.split('=')[0]
                _v=allstr[allstr.index('=')+1:]
                if _k in varnames:
                    raise Usage('variable name repeat')
                else:
                    if c('int'):
                        pass
            elif c('popen'):
                _p=os.popen(allstr)
                try:
                    while 1:
                        _s=_p.read(1)
                        if _s:
                            sys.stdout.write(_s)
                        else:
                            raise Usage(Usage('_exit'))
                except KeyboardInterrupt:
                    pass
                except Usage as x:
                    if x.content.content=='_exit':
                        pass
                    else:
                        raise x
            elif c('ps'):
                if not allstr:
                    print(' '.join([tb.str033.color(96,x) if x==ps else x for x in pslist.keys()]))
                elif allstr in pslist:
                    ps=allstr
                else:
                    raise Usage('not in list')
            elif c('raise'):
                raise Exception(allstr)
            elif c('run'):
                aa(1)
                try:
                    _fn=tb.checkfile.check(argstr or pd,file=0,dir=0,_tb=1) if 'p' in swch else allstr
                    _ft=os.path.splitext(_fn)[-1]
                    if _ft=='.tb' or (_ft=='.py' and open(_fn).readline().startswith(';qpy:tbse')):
                        fs.append(open(_fn))
                        inread=True
                    elif _ft=='.py':
                        subprocess.call((sys.executable,_fn))
                    else:
                        os.system(_fn)
                except FileNotFoundError:
                    print('tool:no such file or directory')
            elif c('sdb'):#
                aa(2)
                if args[0]=='conn':
                    sdb=tb.tbsocket.client()
                    #sdb.conn(input('host: '),input('port: '))
                    sdb.conn(*(args[1].split(':')))
                    while 1:
                        _s=input('sdb -->')
                        sdb.send(_s)
                        _recv=sdb.recv()[1]
                        if _recv==0:
                            sdb.close()
                            break
                        if _recv==1:
                            pass
                        else:
                            print(_recv)
                    sdb.close()
                elif args[0]=='on':
                    if args[1]=='rand':
                        _port=random.randint(1025,65535)
                        sdb=tb.tbsocket.server(socket.gethostname(),_port,num=1)
                        print('port=%i'%_port)
                    else:
                        sdb=tb.tbsocket.server(*(args[1].split(':')),num=1)
                    sdb.acpt()
                    insdb=True
                elif args[0]=='off':
                    if args[1]=='conn':
                        sdb.close('s')
                        insdb=False
                    else:
                        raise Usage('what to close?')
                else:
                    raise Usage('the first argument must be connect|on|off')
            elif c('set'):
                if 'p' in swch:
                    _v=input()
                else:
                    _v=0
            elif c('sh'):
                if s=='sh busybox exit':
                    inbbx=False
                elif s=='sh exit':
                    insh=False
                elif 'on' in bgsw:
                    insh=True
                elif args and args[0]=='cd':
                    if len(args)==1:
                        _cd=home
                    elif len(args)==2:
                        _cd=args[1]
                        if _cd=='-':
                            _cd=last_cd
                    else:
                        _cd=cd.replace(args[1],args[2])
                    _cd=os.path.realpath(_cd)
                    try:
                        os.chdir(_cd)
                        last_cd=cd
                        cd=_cd
                        sh_erc=0
                        if dbg:
                            print('cd:',cd,'\nlast_cd:',last_cd)
                    except FileNotFoundError:
                        raise Usage('cd: %s: no such file or directory'%_cd)
                        sh_erc=2
                    except NotADirectoryError:
                        raise Usage('cd: %s: not a directory'%_cd)
                        sh_erc=2
                else:
                    sh_erc=os.system(sh_pre_def()+allstr)>>8
            elif c('uninstall'):
                aa(0)
                if input('Uninstall all?(y/n)').lower()=='y':
                    print('ok.')
                    os.chdir(txts.get('path'))
                    print('Change directory to ',txts.get('path'))
                    try:
                        os.chdir('Run')
                    except FileNotFoundError:
                        raise Usage('you cannot uninstall this package!')
                    for x in txts.get('install files').split():
                        print('remove '+x)
                        if os.path.isfile(x):
                            os.remove(x)
                        elif os.path.isdir:
                            os.system('rm %sf %s'%('/' if os.name=='nt' else '-r',x))
            elif c('update'):
                aa(0)
                print(txts.get('upd'))
            elif c('ver'):
                aa(0)
                print(txts.get('version'))
            elif c('wait'):
                aa(1)
                time.sleep(float(allstr)/1000)
            elif not re.sub(' ','',s):
                pass
            else:
                print('tool:%s:Not found'%key)
            if insdb:
                sdb.send(b'1')
        except Usage as x:
            print('tool:%s'%x.content)
        except SystemExit as x:
            raise x
        except KeyboardInterrupt:
            print('\nAbort')
            continue
        except EOFError:
            if insh or inbbx:
                insh=inbbx=False
                print()
                continue
            print(end='\n\033[32mYes or no? (y/[n]) \033[0m')
            if tb.getch.getch().lower()=='y':
                print()
                sys.exit(256)
            print()
            continue
        except:
            traceback.print_exc()
            time.sleep(1)
    except (KeyboardInterrupt,EOFError):
        if insh or inbbx:
            insh=inbbx=False
            print()
            continue
        print(end='\n\033[32mYes or no? (y/[n]) \033[0m')
        if tb.getch.getch().lower()=='y':
            print()
            sys.exit(256)
        print()
        continue
