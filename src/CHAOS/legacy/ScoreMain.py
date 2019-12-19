# AlgorithmSeungHyunExam.py
# Algorithm by Lee SeungHyun


from Student import Student
from Subject import Subject

from ScoreVar import *
from ScorePrint import *
from ScoreUtil import *
from ScoreCommand import *
from ScoreFile import *
from ScoreExecute import *
'''
import sys, tty, termios
class _Getch:
    def __call__(self):
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(sys.stdin.fileno())
            ch = sys.stdin.read(1)
            if ch != "\33": return ch
            elif ch == "\03": return ch
            ch += sys.stdin.read(1)
            # if ch[1] == "\33": return ch
            ch += sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
            return ch
'''
def ExitHandler():
    print()
    sys.exit()


def ExecuteCommand(s):
    msg = s.split(" ")
    try:
    # if True:
        if   msg[0] in commands["exit"].msg: return False
        elif msg[0] in commands["assign"].msg:
            AssignSubject(int(msg[1]),(msg[2],msg[3]))
            PrintConflict()
        elif msg[0] in commands["pop"].msg:      PopSubject(int(msg[1]))
        elif msg[0] in commands["move"].msg:
            MoveSubject(int(msg[1]),(msg[2],msg[3]))
            PrintConflict()
        elif msg[0] in commands["pop"].msg:      PopSubject(int(msg[1]))
        elif msg[0] in commands["execute"].msg:  Execute()
        elif msg[0] in commands["writecsv"].msg: SaveTimetable()
        elif msg[0] in commands["save"].msg:     SaveData()
        elif msg[0] in commands["help"].msg:     PrintCommands(commands)
        elif msg[0] in commands["load"].msg:     LoadData()
        elif msg[0] in commands["conflict"].msg: PrintConflict()
        elif msg[0] in commands["viewstu"].msg:
            if len(msg)==1: PrintStudents(["all"])
            else: PrintStudents(msg[1:])
        elif msg[0] in commands["viewsub"].msg:
            if len(msg)==1: PrintStudents(["listexam"])
            else: PrintSubjects(msg[1:])
        else:
            print(GetStrAwesome("HALT: Unavailable Command"))
            PrintCommands(commands)
        return True
    except:
        print(GetStrAwesome("HALT: Command Couldn't understand"))
        print("Unexcepted Error", sys.exc_info()[0])
        PrintCommands(commands)

if __name__ == '__main__':
    # Manual edit
    DataInit()
    PrintCommands(commands)
    # inp = _Getch()
    while(True):
        print("\n >> ",end="")
        # print("\n >> ",end="\r")
        # msg = ""
        # while (True):
            # m = inp()
            # if   m=="\33[A": print("Up!")
            # elif m=="\33[B": print("Down!")
            # elif m=="\??": print("Backspace")
            # elif m=="\15": break
            # elif m=="\3": ExitHandler()
            # else: msg+=m
            # print(" >> "+msg,end="\r")
        msg = input()
        if msg in commands["history"].msg:
            for k in history: print(k)
            continue
        history.append(msg)
        if ExecuteCommand(msg)==False: break
