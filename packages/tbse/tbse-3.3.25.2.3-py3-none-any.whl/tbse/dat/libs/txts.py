import sys,os
def get(s):
    try:
        return {
'version':'3.3.1-25a',
'path':os.sep.join(sys.argv[0].split(os.sep)[:-2]),
'hlp':'''\
*Escape characters:*
```
#a -> &
#q -> '
## -> #
#. -> blank
#x** -> character from hex **
#u**** -> character from unicode ****
```
*Commands:*
```
alias:make an alias, or search in the list
{alias}
{alias <a>}
{alias <a>=<b>}
busybox:execute busybox command
{busybox <command>}
{busybox --on}\033[90m#type exit to exit\033[0m
clearqq:remove qq cache
{clearqq}
do:open do editor
{do}
echo:print string
{echo <content>}
exit:exit this program
{exit [code]}
help:get helps
{help}
home:set home dir
{home <dir>}
input:make a break
{input}
int/str/bln:define a variable
{<int|str|bln> <variable_name>}
raise:make an error in tool.py
{raise [error]}
ps:toggle ps
{ps [ps_name]}
run:execute a file like *.tb
{run <-p|*.tb>}
sdb:like sdebr
{sdb conn <host:port>}
{sdb on <rand|host:port>}
{sdb off conn}
set:set a value to a variable
{set <variable_name>=<value>}
{set -p <variable_name>}
sh:execute shell command
{sh <command>}
{sh --on}\033[90m#type exit to exit\033[0m
uninstall:uninstall some programs and packages
{uninstall}
update:information for updates
{update}
ver:version
{ver}
wait:make the program pause
{wait <time/ms>}
```
''',
'install files':'tool.py libs/txts.py libs/dol.py libs/clearqq.py libs/bash',
'upd':'''\
Update info:
    ---- 3.3.1 25a ----
1.Comments and strings (ps: echo 'this is a string';here are some comment texts)
2.Escape characters (ps: `echo '#q#a#.##'` output `'& #`
    ---- 3.3 (last release) ----
1.Runtime command (Type shell command like 'tb -c cmd1:arg1 cmd2:arg2 ...')
2.Runtime file running (Type shell command like 'tb file1.tb file2.tb ...')
3.Toggle the shell prompt (Type 'ps' to toggle then type 'insh' to try)
4.Wait a few time (Type 'wait')
5.Extra functions (Testing)
6.Setup package no longer relies package 'tb'
7.Removed Herobrine
'''
}[s]
    except KeyError:
        raise ValueError('txts.py: failed to get "%s"'%s)
if __name__=='__main__':
    print(sys.argv[0])
    for x in ('version','path','hlp','install files','upd','this is a falied key'):
        print('\033[33mtxts.get\033[92;100m(\033[0;95m"%s"\033[92;100m)\033[0m\n%s'%(x,get(x)))
