import os
if os.name=='nt':
    import msvcrt
    def getch():
        return msvcrt.getch.getch().decode('ASCII')
else:
    import sys,tty,termios
    fd=sys.stdin.fileno()
    old_settings=termios.tcgetattr(fd)
    def getch():
        try:
            tty.setraw(fd,termios.TCSANOW)
            ch=sys.stdin.read(1)
            sys.stdout.write(ch)
            sys.stdout.flush()
        except:
            ch=b'\x00'
        finally:
            termios.tcsetattr(fd,termios.TCSADRAIN,old_settings)
            return ch
