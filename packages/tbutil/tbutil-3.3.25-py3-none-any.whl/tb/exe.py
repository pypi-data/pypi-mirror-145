import sys,os
def exe(s):
#   print(os.getcwd())
    return os.system(sys.executable+' '+s)
