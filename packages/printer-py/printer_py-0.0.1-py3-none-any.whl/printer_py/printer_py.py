def printer(*args,newln=False):
    brek = ' {} ,'*len(args) if newln == False else ' {} \n'*len(args)
    print(brek.format(*args)[:-1])