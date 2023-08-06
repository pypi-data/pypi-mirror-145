import builtins,sys,os,re,tb
def print(*objects,sep=' ',end='\n',file=sys.stdout,flush=False):
    if os.name=='posix' and file==sys.stdout:
        file.write('\033[?25l')
    s=sep.join([str(x) for x in objects])+end
    if os.name!='posix' and file==sys.stdout:
        s=re.sub('\033\[[^a-zA-Z]*[a-zA-Z]','',s)
    elif os.name=='posix' and file==sys.stdout:
        s=s.replace('\033[0','\033[%s'%_norm)
    file.write(s)
    if flush or (os.name=='posix' and file==sys.stdout):
        file.flush()
    if os.name=='posix' and file==sys.stdout:
        file.write('\033[?25h')
        file.flush()
def input(s=''):
    print(end=str(s))
    return builtins.input()
class simpcout():
    def __sub__(self,x):
        print(end=x)
        return self
class cout():
    __lshift__=simpcout.__sub__
cout=cout()
def cls():
    if os.name=='posix':
        os.system('clear')
    else:
        os.system('cls')
o=simpcout()
endl='\n'
_norm='0'
print(end='\033[0m')
if __name__=='__main__':
    cls()
    o-'awa'-'123'-endl
    o-'ohh'
    o-endl
    print(input('awa:'))
