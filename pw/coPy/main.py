#!/usr/bin/python

import os,sys,glob,MySQLdb,dialog

Host="localhost"
User=""
Pass=""
Db  ="mysql"

def Connection(_host,_user,_pass,_data):
    try:
        Link = MySQLdb.connect (host = _host,
                                user = _user,
                                passwd = _pass,
                                db = _data)
        return Link.cursor()
    except Exception,err:
        print "Connection Error :",err[1],"\nExiting.."
    return 0

def UpdateContent(_nicetitle,_di):
    try:
        #Get the values..
        Fp = open(_nicetitle,"r")

        NiceTitle = _nicetitle[2:].split('.')[0]
        Raw = Fp.readline().rstrip().split('::')
        Content = Fp.read().rstrip()
        #Check parameters, if doesn't given ask to user
        if len(Raw)>=4:
            Lang = Raw[0]
            Parent = Raw[1]
            PType  = Raw[2]
            Title  = Raw[3]
        else:
            Lang = _di.inputbox("Language for %s file"%NiceTitle)
            (x,Parent) = _di.menu("What's the parent of %s ?"%NiceTitle,
            width=40,
            choices=[("B", "Bireysel"),
                     ("G", "Gelistirici"),
                     ("K", "Kurumsal"),
                     ("M", "Ana Sayfa"),
                     ("P", "Basin")])
            (x,Ptype) = _di.menu("What's the type of %s page?"%NiceTitle,
            width=40,
            choices=[("P", "Sayfa"),
                     ("D", "Dokuman")])
            Title = _di.inputbox("Title for %s "%NiceTitle)

        _di.msgbox(NiceTitle+Title)
        return Title
    except Exception,er:
        print "File %s corrupted !, passed." % er

def main():
    Di = dialog.Dialog(dialog="dialog")
    Di.add_persistent_args(["--backtitle","coPy Python Bindings for PW"])
    Titles = ""

    if len(sys.argv)==2:
        Dir = sys.argv[1]
    else:
        Dir = "./"

    answer = Di.yesno("""This operation will add or update .html files in given directory. 
coPy uses filename as NiceTitle, first line of file as Title and 
file content as Content on %s database.

Do you want to continue ?
""" % Host,width=80)

    if answer == Di.DIALOG_OK:
        for Fp in glob.glob('%s/*.htm*' % Dir):
            UpdateContent(Fp,Di)
            #Titles = ' - ' + Fp[2:] + '\n' + Titles

    else:
        Di.infobox("Good Bye")
    #Cursor = Connection(Host,User,Pass,Db)

    #if Cursor: 
    #    print "Connected."

if __name__ == "__main__":
    sys.exit(main())
