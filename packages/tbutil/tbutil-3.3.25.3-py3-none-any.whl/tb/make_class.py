make=lambda *a,**b:type(a[0],tuple(a[1:]),b) if a else type('tb_making_on_'+str(__import__('time').time()),(object,),b)
