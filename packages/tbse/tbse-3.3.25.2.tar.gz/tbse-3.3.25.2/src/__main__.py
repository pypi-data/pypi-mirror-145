import os,subprocess,sys
pd=os.path.dirname(os.path.realpath(__file__))
subprocess.call((' '.join((sys.executable,pd+'/dat/tool.py ',*(sys.argv[1:])))),shell=True)

