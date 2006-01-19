import random

class Edmund(QObject):
    """
    An Edmund macro for the Kalam Editor.
    
    Of course, if I really re-implemented Eliza, the responses would bear
    some relevance to the input. Anyway.
    """
    
    def __init__(self, *args):
        QObject.__init__(self)
        self.responses = [
            "First Name?",
            "Come on, you MUST have a first name.",
            "Sod Off?",
            "Madam, without you, life was like a broken pencil...pointless.",
            "So what you are saying, Percy, is something you have never" +
            " seen is slightly less blue than something else . . that you " +
            "have never seen?",
            "I'm afraid that might not be far enough. " +
            "Apparently the head Mongol and the Duke are good friends. " +
            "They were at Eton together.",
            "Ah ah, not so fast! Not that it would make any difference. " +
            "We have the preliminary sketches...",
            "You have absolutely no idea what irony is, have you Baldrick?",
            "Baldric, you wouldn't recognize a subtle plan if it painted  " +
            "itself purple and danced naked on a harpsichord singing " +
            "'subtle plans are here again'.",
            "Baldric, you have the intellectual capacity of a dirty potato.",
            "Ah, yes. A maternally crazed gorilla would come in handy " +
            "at this very moment.",
            "That would be as hard as finding a piece of hay in an " +
            "incredibly large stack of needles.",
            "Normal procedure, Lieutenant, is to jump 200 feet in the air " +
            "and scatter oneself over a wide area.",
            "I think I'll write my tombstone - Here lies Edmund Blackadder" +
            ", and he's bloody annoyed.",
            "As a reward, Baldrick, take a short holiday. " +
            ".... Did you enjoy it?"
    ]

        self.doc, self.view = createDocument()
        self.doc.setTitle("Talk to Edmund BlackAdder")
        self.connect(self.view,
                     PYSIGNAL("returnPressed"),
                     self.respond)
        self.view.append("Welcome\n")
        self.view.goEnd()
        
    def respond(self):
        input = str(self.view.textLine(self.view.numLines() - 2))
        if input.find("love") > 0:
            response = self.responses[3]
        elif input.find("dead") > 0:
            response = self.responses[15]
        elif input.find("fear") > 0:
            response = self.responses[5]
        else:
            choice = random.randrange(0,len(self.responses),1)
            response = self.responses[choice]
        self.view.append(response + "\n\n")
        self.view.goEnd()


edmund = Edmund()
