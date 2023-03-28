# TO DO
# ADD TIME STAMPS
# WRITE TO LOG FILE
import time

def initLog():
    f = open("log.txt", "a")
    f.close()

def logComment(comment):
    f = open("log.txt", "a")
    t = time.asctime()
    s = t + ' ' + comment + "\n"
    f.write(s)
    f.close()

def logContainerMove(name, oldX, oldY, newX, newY):
    f = open("log.txt", "a")
    t = time.asctime()
    s = t + ' Move container ' + name + ' from ' + str(oldX) + ' , ' + str(oldY) + ' to ' + str(newX) + ' , ' + str(newY)

def logLogIn(username):
    f = open("log.txt", "a")
    t = time.asctime()
    s = t + ' ' + username + " logged in" + "\n"
    f.write(s)
    f.close()