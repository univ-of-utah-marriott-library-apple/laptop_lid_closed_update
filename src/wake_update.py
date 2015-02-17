#!/usr/bin/env python
from datetime import datetime
import socket
import subprocess
import sys
import argparse
import os

# This script remotely wakes up managed devices and sends an SSH command to them
# to trigger a radmind script to begin updating the file system
# 
#
#
#



def main (args):
    script_name = 'Laptop Maitenence Scheduler'
    name = '_'.join(script_name.lower().split())
    version = '1.0.0'
    current_time = datetime.now()
    weekday = current_time.strftime('%A').lower()

    args = parse()
    #parse the arguments

    start_time = args.start
    end_time = args.end


    if args.override:
        over_ride_file = args.override
        
        #get the list of computers for the day
        task_list = createTaskList(over_ride_file)
        
        #begin attempting to wake and run maitenence on the machines
        timerThread(task_list, current_time, start_time, end_time)
    else:
        task_list = createTaskList(weekday)
        timerThread(task_list, current_time, start_time, end_time)
        

    
    
    

def parse():

    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument('-h', '--help')
    parser.add_argument('-v', '--version')
    parser.add_argument('-a', '--add', type=str)
    parser.add_argument('-s', '--start', type=int, default=1)
    parser.add_argument('-e', '--end', type=int, default=23)
    parser.add_argument('-o', '--override', type=str)

    args = parser.parse_args()

    if args.help:
        usage(options)
        sys.exit(0)
    if args.version:
        version(script_name, version)
        sys.exit(0)

    

    return args


    
    #if args.add:
    #    add_ip_address(args.add)
    #to be add later, add to text files when necessary

def createTaskList(weekday):

    task_list = []
    #used to hold list of computer to run

    
    #get any computers from previous attempts, add them to the current list
    with open (os.path.dirname(os.path.realpath(__file__))+'/overflow.txt', "r") as _theOverFlow:
        
        for _line in _theOverFlow:
            task_list.append(_line)
            
        _theOverFlow.close()

    #add to the new list to do this day
    with open (os.path.dirname(os.path.realpath(__file__))+ '/' + weekday +'.txt', "r") as _theOverFlow:
        
        for _line in _theOverFlow:
            task_list.append(_line)
            
        _theOverFlow.close()
    return task_list

def timerThread(task_list, current_time, start_time, end_time):
    log_output = ''
    attempted = False

    if not task_list:
        log('Empty List', False)
        return
    #while there are task to perform
    while task_list:
        #if it is the right time
        if (current_time.hour < end_time or current_time.hour > start_time):
            
            for _item in task_list:
                #iterate through the list
                if (attemptConnection(_item)):
                    task_list.remove(_item)
        else:
            break
    log(log_output)

def attemptConnection(item):
    machine_info = item.split()
    mac_address = machine_info[1]
    ip_address = machine_info[2]
    
    command_wake = 'sh wake.sh ' + item
    command_update = 'ssh -p 22022 mac@' + ip_address + ' "echo success > /var/tmp/test.txt"' 
    #'sleep 3 && touch /tmp/radmind && caffeinate -t 120 &'

    wake_output = subprocess.check_output([command_wake], shell=True)
    ssh_output = ''
    #log(wake_output, False)

    if (('success' in wake_output) and ssh_allowed(ip_address)):
        print (command_update)
        subprocess.call([command_update], shell=True)
        log('SUCCESSS!!! ' + machine_info[0], False)
        return True
    else:
        return False
        

def ssh_allowed(ip_address):
    open_port = False
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        s.connect((ip_address, 22022))
        open_port = True
        s.close()
    except:
        print 'Could not SSH'
        
    return open_port
    
def log (output, final):

    output = str(output)

    
    with open(os.path.dirname(os.path.realpath(__file__))+'/log.txt', 'a') as theLog:
        if final:
            theLog.write("###############################" + '\n')
            theLog.write(str(datetime.today()) + '\n')
            theLog.write("Failed Machines" + '\n' + '\n')
            theLog.write(output + '\n')
            theLog.write("________________________________" + '\n')
        else:
            theLog.write(output + '\n')
            
        theLog.close()

        
    #shutil.copyfile('current.txt', 'overflow.txt')
        #overflow
	#send email

if __name__ == "__main__":
    main(sys.argv)


        
