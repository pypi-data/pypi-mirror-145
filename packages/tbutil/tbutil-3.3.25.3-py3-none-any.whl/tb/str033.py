def color(c,s):
    return '\033[%s%s\033[0m'%(c,s)
def say(c,s):
    print(color(c,s))
if __name__=='__main__':
    I=(30,31,32,33,34,35,36,37,90,91,92,93,94,95,96,97)
    J=(40,41,42,43,44,45,46,47,100,101,102,103,104,105,106,107)
    for i in I:
        for j in J:
            print(end='')
