import os
def sfz(s17):
    nsum=0
    t=(7,9,10,5,8,4,2,1,6,3,
       7,9,10,5,8,4,2)
    for i in range(17):
        nsum+=t[i]*int(s17[i])
    n=str((1-nsum)%11)
    if n=='10':n='X'
    return s17+n+'\n'+' '*17+'^\n'
if __name__=='__main__':
    import tb
    tb.std.cls()
    while 1:
        print(sfz(input()))
