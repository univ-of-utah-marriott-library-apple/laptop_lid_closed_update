#!/usr/bin/env python

from datetime import datetime
import time
import sys
import subprocess
import re
import os
import shutil
import smtplib
# from email.mime.text import MIMEText

#define time variables
def main (args):
    theTime = datetime.now()
    weekday = theTime.strftime('%A').lower()

    startTime = 1 #i.e. 11 at night
    endTime = 4 #i.e 4 in the morning



    createTaskList(weekday)


    timerThread(weekday, theTime, startTime, endTime)

def createTaskList(weekday):
    open('current.txt', 'w').close()
    #wipe file before using it

    #get the daiy task
    shutil.copyfile(weekday+'.txt', 'current.txt')

    #get the last task that were never finished last run

    with open (os.path.dirname(os.path.realpath(__file__))+'/overflow.txt', "r") as theOverFlow:
        overFlow = theOverFlow.readlines()
        cleanOverFlow = [l.strip() for l in overFlow if l.strip()]
        #strip any empty lines
        theOverFlow.close()
    #add to the new list to do this day
    with open(os.path.dirname(os.path.realpath(__file__))+'/current.txt', 'a') as theCurrentList:
        theCurrentList.writelines(cleanOverFlow)
        theCurrentList.close()

def timerThread(weekday, theTime, startTime, endTime):
    output = ''
    attempted = False

    #start a thread that runs all night

    while (True):

        #if it is the right time
        if (theTime.hour < endTime or theTime.hour > startTime):

            output += attemptConnection()
            # attempt to connect and send SSH command
            #store variables in variable

            attempted = True
            #to determine if task were attempted

        else:
            #if the thread had run and the time is out of range then log the results and break the loop
            if(attempted):
                logResults(output, theTime)
            break

        #every iteration update the current mac machine list, log the results, and sleep for x amount of time
        updateList(output)
        time.sleep(20)

def attemptConnection():
    s = (subprocess.check_output([os.path.dirname(os.path.realpath(__file__))+"/wake.sh", 'current.txt']))
    s = s.decode('ascii')
    print(s)

    return s

def updateList(output):
    f = open (os.path.dirname(os.path.realpath(__file__))+'/current.txt', 'w+')
    f.write(output)
    f.close()

def logResults(output, theTime):
    with open(os.path.dirname(os.path.realpath(__file__))+'/log.txt', 'a') as theLog:
        theLog.write("###############################" + '\n')
        theLog.write(str(theTime.today()) + '\n')
        theLog.write("Failed Machines" + '\n' + '\n')
        theLog.write(output + '\n')
        theLog.write("________________________________" + '\n')
        theLog.close()
    shutil.copyfile('current.txt', 'overflow.txt')
	#send email
    return

def sendEmail():
    fp = open ("log.txt", 'rb')
    msg = MIMEText(fp.read())
    fp.close()

    me = 'wakeOnLanLogger@utah.edu'
    you = 'justin.barsketis@utah.edu'
    msg['Subject'] = 'The contents of '
    msg['From'] = me
    msg['To'] = you
    # Send the message via our own SMTP server, but don't include the
    # envelope header.
    s = smtplib.SMTP('localhost')
    s.sendmail(me, [you], msg.as_string())
    s.quit()

if __name__ == "__main__":
    main(sys.argv)
