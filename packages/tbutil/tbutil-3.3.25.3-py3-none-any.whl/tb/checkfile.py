import os,sys,time
from tb import *
from tb.std import *
def check(d,**rule):
    if os.name!='posix':
        sys.exit('Must be posix system')
    cls()
    def _color(d,s):
        if os.path.isdir(d+'/'+s):
            return '\033[91m'+s
        elif os.path.isfile(d+'/'+s):
            return '\033[0m'+'\033[92m'.join(os.path.splitext(s))
    def canttype(c):
        ext='_'+os.path.splitext(l[c])[1][1:]
        return (
            os.path.isdir(d+'/'+l[c])
            and 'dir' in rule
            and not rule['dir']
            or (
                os.path.isfile(d+'/'+l[c])
                and (
                    'file' in rule
                    and (
                        rule['file']
                        and ext in rule
                        and not rule[ext]
                        or (
                        	    not rule['file']
                            and not (
                                ext in rule
                                and rule[ext]
                            )
                        )
                    )
                )
            )
        )
    def sift(lst,ptn):
        return (lambda x:x.sort(key=lambda y:[y.index(z) for z in ptn.split()]) or x)([x for x in lst if all(y in x for y in ptn.split())])
    last_d='/sdcard'
    pattern=''
    while 1:
        try:
            listing=os.listdir(d)
        except PermissionError:
            print('\033[31mPermission denied')
            time.sleep(.5)
            d=last_d
            try:
                listing=os.listdir(d)
            except PermissionError as x:
                raise x
        listing.sort()
        l=sift(listing,pattern)
        ss='\n'.join(['\033[96m%3i) %s\033[0m'%(i+1,_color(d,l[i])) for i in range(len(l))]) or 'Nothing'
        while 1:
            cls()
            print(ss)
            print('\033[33m')
            print(d,'\033[94m/'+pattern if pattern else '')
            print('\033[90mUsage:')
            print('  ..:parent dir')
            print(' xxx:change dir by number')
            print(':xxx:change dir by absolute path')
            print('.xxx:select')
            print('/xxx:sift')
            c=input('\033[95m> \033[96m')
            if c.startswith('.'):
                _mode=1
                c=c[1:]
                if c and c.isdigit():
                    c=int(c)-1
                    if c<len(l):
                        print('\033[0m')
                        break
            elif c.startswith('/'):
                _mode=2
                c=c[1:]
                break
            else:
                _mode=0
                if c.startswith(':'):
                    break
                else:
                    if c.isdigit():
                        c=int(c)-1
                        if c<len(l):
                            break
            print('\033[31mFailed')
            time.sleep(.5)
        if _mode==1:
            if canttype(c):
                print('\033[31mYou can not type it.\033[0m')
                time.sleep(.5)
                continue
            #print(d+'/'+l[c])
            return d+'/'+l[c]
        elif _mode==2:
            pattern=c
            continue
        last_d=d
        pattern=''
        if isinstance(c,str) and c.startswith(':'):
            d=c[1:]
        elif c=='..':
            if d=='/':
                continue
            else:
                d='/'.join(d.split('/')[:-1])
                if not d:
                    d='/'
        else:
            if os.path.isdir(d+'/'+l[c]):
                d+='/'+l[c]
            else:
                print("\033[31mIt's not a direction")
                time.sleep(.5)
#check('/sdcard/qpython/Cmd/Command')
#input(check('/sdcard/qpython'))
