'''
/**
  * tbse install guide
  */
'''

import builtins,json,os,re,shutil,socket,sys,time
if os.name not in ('nt','posix'):
    print('Hey, sorry, no support for jvav platform!')
    exit(18)
def print(*objects,sep=' ',end='\n',file=sys.stdout,flush=False):
    if os.name=='posix' and file==sys.stdout:
        file.write('\033[?25l')
    s=sep.join([str(x) for x in objects])+end
    if os.name!='posix' and file==sys.stdout:
        s=re.sub('\\033\[[0-9;]*[a-zA-Z]','',s)
    elif os.name=='posix' and file==sys.stdout:
        s=s.replace('\033[0','\033[%s'%_norm)
    file.write(s)
    if flush or (os.name=='posix' and file==sys.stdout):
        file.flush()
    if os.name=='posix' and file==sys.stdout:
        file.write('\033[?25h')
        file.flush()
def input(s=''):
    print(end=s)
    return builtins.input()
def getch():
    try:
        return __import__('msvcrt').getch()
    except ImportError:
        import tty,termios
        fd=sys.stdin.fileno()
        old_settings=termios.tcgetattr(fd)
        try:
            tty.setraw(sys.stdin.fileno(),termios.TCSANOW)
            ch=sys.stdin.read(1)
            sys.stdout.write(ch)
            sys.stdout.flush()
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
            return ch
_norm='0'
from dat.libs import txts
sep=os.sep
_dir=''
os.system('cls' if os.name=='nt' else 'clear')
def line(c):
    print('\033['+str(c)+'m'+'-'*os.get_terminal_size().columns)
print('\033[1mToolBox%s\033[90m (Simple Edition)\033[0;1m Install Guide\033[0m'%txts.get('version'))
line(94)
print(end='\033[91m'+txts.get('upd')+'\033[0m')
line(94)
def m():
    global _dir
    while 1:
        _dir=input('\n\033[34;43mInstallation direction: \033[32;40m')
        if _dir[-8:]=='%sCommand'%sep:
            break
        if _dir[-9:]=='%sCommand%s'%(sep,sep):
            _dir=_dir[:-1]
            break
        print('\033[31mPlease refer to "Command%s" direction!'%sep)
        time.sleep(.5)
    print(end='\033[0m')
if 'manually'!=input('\033[33mHow to install ([auto],manually):\033[0m'):
    print('Starting to auto install...')
    if os.name=='nt':
        print(end='Type your disk: ',flush=1)
        _disk=getch().upper()
        _path=input('\nType path: %s:\\'%_disk)
        g_w=os.walk(_disk+':\\'+_path)
    else:
        g_w=os.walk((lambda x:x if x!='/' else '/sdcard')('/'+input('\033[B\033[90m(Normal /sdcard)\033[A\r\033[35;42mSearch cmdplus from:\033[0m /')))
    print('Find installation diractory...',end='',flush=1)
    found=[path for path,dirs,files in g_w if path[-8:]=='%sCommand'%sep and 'Run' in dirs and not os.path.realpath(path).startswith('/storage/emulated/0/.File_Recycle/')]
    print('%s found'%len(found))
    if len(found):
        if len(found)>1:
            for i in range(len(found)):
                print('\033[96m%3i:\033[94m%s\033[0m'%(i+1,found[i]))
            while 1:
                check=input('\033[32mSelect: \033[0m')
                if check in (str(i+1) for i in range(len(found))):
                    break
        else:
            check=1
        print('Press enter to run!')
        if 'n'==input('\033[36mInstall to \033[31m%s\n\033[32mAll right?\033[33m([y]/n)\033[0m'%found[int(check)-1]):
            print('Exitting...')
            exit(0)
        else:
            _dir=found[int(check)-1]
    else:
        print('\033[33mNot found!')
        print('Please try to manually install\033[0m')
        time.sleep(1)
        m()
else:
    m()
print('\n\033[90mVerifing package...')
try:
    with open(_dir+'/Run/libs/.las.prolb','w') as f:
        f.write(''.join([''.join([chr(int(j)) for j in str(ord(i))])+'>' for i in (chr((int(i)+1)*2+5) for i in ''.join(bin(eval('0x'+f'$key={"PX@ZTXXVZPX@ZTXXVZPX@ZPBXXBPX@ZPBXXBPX@XTXP@XPX@XTXP@XPX@XXBTZVPX@XXBTZVPX@XXBTZVPX@XXBTZVP@@XVXB@@P@@XVXB@@P@@XP@VPXP@@XP@VPXP@@XVXB@@P@@XVXB@@P@ZXXBPZ@P@ZXXBPZ@P@@XVXB@@P@@XVXB@@PXXXXVXXTPXXXXVXXTPXXXPPPPXPXXXPPPPXPXXX@PVXXPXXX@PVXXPXXX@PVXXPXXX@PVXXPXX@TVPX@PXX@TVPX@" if json.loads(open(_dir+"/Builtins.json").read())["items"][0]["Version"].startswith("0.6") else "QV[QYYV^OQ[OQV[QYYV^OQ[OQYYV^OQ[OQV[QYYV^OQ[OQYYV^OQYYQYYV^OTeQQV[QYYV^OQ[OQYYV^OQYYQV[QYYV^OQ^T"}\n$Trial=\n$Activate=true\n$host={socket.gethostname()}\n$ip={socket.gethostbyname(socket.gethostname())}\n$uid={os.getuid()}\n$gid={os.getgid()}'.encode('utf8').hex())).split('0b')))]))
except FileNotFoundError:
    print('\033[93mThe cmdplus version is too low, please update\033[0m')
    exit(18)
os.chdir(sep.join(__file__.split(sep)[:-1]))
for n in txts.get('install files').split():
    if os.path.isfile('./dat/'+n):
        cp=shutil.copyfile
    elif os.name=='nt':
        def cp(s,d):
            os.system('xcopy %s %s /c /d /e /h'%(s,d))
    else:
        def cp(s,d):
            os.system('cp -r %s %s'%(s,'/'.join(d.split('/')[:-1])))
    try:
        cp('./dat/'+n,_dir+'/Run/'+n)
    except FileExistsError:
        pass
    print('Success in installing: %s'%n)
print('Installing tb...')
os.system(sys.executable+' -m pip install tbutil --upgrade')
for i in range(8):
    print(end='Trying: add to path...(t=%i)\033[90m'%(7-i))
    try:
        print('Starting to add')
        python_install=os.path.realpath(sys.executable)
        python_parent_dir=os.path.dirname(os.path.dirname(python_install))
        with open(python_parent_dir+"/bin/tb","w") as f:
            f.write("%s "%python_install+_dir+"/Run/tool.py %s"%' '.join('${%s}'%i if os.name=='posix' else '%%%s%%'%i for i in range(1,1024)))
        if os.name=="posix":
            os.system("chmod 6755 %s"%python_parent_dir+"/bin/tb")
        print("Add to python path: All job did ok.")
        break
    except:
        print('\033[91mFalied')
        if i<7:
            print('\033[33mRetrying...\033[90m')
            time.sleep(.3)
        else:
            print('Failed: cannot add to python path.\033[0m')
            exit(29)
print(end='Writing Builtins.json\n    1/4 load file...')
bt=json.loads(open(_dir+sep+'Builtins.json').read())
print(end='done\n    2/4 Writing basic informations...')
it=bt['items']
it[2]['debug']='true'
it[5]['AutoRun']=list(set(it[5]['AutoRun'])|{'echo ToolBox Load Successfully!'})
if 'laman29' not in it[6]['Maker']:
    it[6]['Maker'].append('laman29')
    it[7]['MakerJoin'].append('2021')
it[9]['ProgramName']='cmd+(tbse v%s)'%txts.get('version')
it[10]['Informations']=list(set(it[10]['Informations'])|{'The versions of Toolbox before 3.x were lost, because laman29 had a whim to run this command on Linux system:\n $ rm -rf /*'})
if 'alias' in it[15]:
    print(end='done\n    3/4 Writing extend informations...')
    it[15]['alias']['ls']='ls --color'
    it[15]['alias']['ll']='ls -l --color'
    it[15]['alias']['l.']='ls .* --color'
print(end='done\n    4/4 Writing file...')
open(_dir+sep+'Builtins.json','w').write(json.dumps(bt))
print('done\nDone.')
print('\033[91mInstall successfully!\033[0m')
print(txts.get('upd'))
print('Use now? (type y)')
if getch().lower()=='y':
    print()
    os.system(sys.executable+' '+_dir+'/Run/tool.py')
