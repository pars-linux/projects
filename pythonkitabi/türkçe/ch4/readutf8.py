#
# readutf8.py - read an utf-8 file into a Python Unicode string
#

import sys, codecs

def usage():
    print """
Usage: 

python readutf8.py file1 file2 ... filen
"""

def main(args):
    if len(args) < 1:
        usage()
        return

    files=[]
    print "Reading",
    for arg in args:
        print arg, 
        f=open(arg,)
        s=f.read()
        u=unicode(s, 'utf-8')
        files.append(u)
    print
    
    files2=[]
    print "Reading directly as Unicode",
    for arg in args:
        print arg,
        f=codecs.open(arg, "rb", "utf-8")
        u=f.read()    
        files2.append(u)
    print

    for i in range(len(files)):
        if files[i]==files2[i]:
            print "OK"

if __name__=="__main__":
    main(sys.argv[1:])
