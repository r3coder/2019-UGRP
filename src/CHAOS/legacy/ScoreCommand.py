
from ScoreVar import *
# Command Class: holding command's data
class Command:
    def __init__(self, name, msg, group, explain = ""):
        self.name = name # name of command (str) ex) help
        self.msg = msg # command alias as list(str) ex) help, H, h
        self.group = group # what group this command is in
        self.explain = explain # Comment of the commend


history = list()
category = ["Algorithm / Edit", "View", "Save, Load, Utils"]
commands = dict()
# Add commands
commands["execute"]  = Command("execute",["execute", "X", "x"], 0
        ,"Execute algorithm")
commands["assign"]       = Command("assign",["assign", "A", "a"], 0
        ,"a [id] [day] [time] - Force assign subject and show if conflicts")
commands["pop"]    = Command("pop",["pop", "o", "o"], 0
        ,"o [id] - pop subject from timetable")
commands["move"]      = Command("move",["move", "M", "m"], 0
        ,"move [id] [day] [time] - Force Move subject and show if conflicts")

commands["conflict"]  = Command("conflict",["conflict", "C", "c"], 1
        ,"Show conflicting subjects")
commands["viewstu"]    = Command("viewstu",["viewstu", "VT", "vt"], 1
        ,"View student info\n"+
        "vt all - Show all students\n"+
        "vt [stu id list] - Show students with specific id\n"+
        "vt ideal [gap] [maxexam] - Show students with not ideal timetable\n"+
        "vt subs [sub id list] - Show students who taking subject id\n"+
        "vt [stu id start]:[stu id end] - Show students with Id from start to end")
commands["viewsub"]     = Command("viewsub",["viewsub", "VS", "vs"], 1
        ,"View subject info\n"+
        "vs all - Show all subjects\n"+
        "vs exam - Show specific subject information if exam\n"+
        "vs [sub id list] - Show subjects with specific id\n"+
        "vs listexam / le - Show subjects list if exam\n"+
        "vs listall / la - show sujbects list\n"+
        "vs [sub id start]:[sub id end] - Show subjects with Id from start to end")

commands["history"]  = Command("history",["history", "Y", "y"], 2
        ,"Show command history")
commands["save"]     = Command("save",["save", "S", "s"], 2
        ,"Save subject data")
commands["writecsv"]  = Command("writecsv",["writecsv", "W", "w"], 2
        ,"Save timetable data as csv")
commands["load"]     = Command("load",["load", "L", "l"], 2
        ,"load subject data")
commands["exit"]  = Command("exit",["exit", "XX", "xx"], 2
        ,"Exit program")
commands["help"]  = Command("help",["help", "H", "h"], 0
        ,"Help page")

# Print command list as groups
def PrintCommands(commands):
    for i in range(3):
        print("\n "+category[i])
        for j, k in commands.items():
            if k.group == i:
                # if explain is several lines, apply tabs on each line 
                x = k.explain.split("\n")
                print(" ({:2s}) {:10s}:".format(k.msg[1],k.name,k.explain),end="")
                print(x[0])
                for si in x[1:]: print("\t\t",si)



