#!/usr/bin/env python

import os, signal, time, sys

def execute(command, command1, t0):
    
    #Creating pipe
    r,w=os.pipe()  
    
    #Child
    child_pid = os.fork()    
    if child_pid == 0:    	
	res = os.system(command)
	os.write(w, str(res))	
    
    #Parent			
    else:            	    	
        has_stopped = False
        has_Failed = False
        runtime_error = 0
        run_status = ""    
        runtime = 0
                        
	start = time.time()	
		
		
	while(1):		  
	   try:
	      os.waitpid(child_pid, os.WNOHANG)				#to check if child process has stopped	    
	   except OSError: 						#incase it has stopped, system returns error
	      has_stopped = True		    
	      runtime_error = int(os.read(r, 1024))			#runtime_error = 0 if no error, !=0 if error	 
	      runtime = time.time() - start
	      break
	    	    	    	    	  	
	   if((time.time() - start) >= t0):				#checking if time exceeded t0
	      #print "Time Exceeded"
	      new_command = "ps -ef | grep " + '"' + command1 + '"' +  "| awk '{print $2}' > pid.txt"
	      #print new_command
	      a = os.system(new_command)
	      f = open('pid.txt' , 'r')
	      for line in f:
	        #print line
	      	line = line.split('\n')[0]
	      	#print line
	      	os.system("kill -9 "+line);
	      os.kill(child_pid, signal.SIGTERM)
	      os.wait()	    		#in that case kill child
	      break
		
	if(runtime_error != 0):						#if runtime error, do nothing else
	    run_status = "runtime error"
	    has_Failed = True;
	    runtime = -1			
	else:								#if no runtime error, it could also be possible that time exceeded! check that
	    if(has_stopped == True):				        #this could be true only if the child stopped on its own
	      run_status = "ok"		
	    else:
	      run_status = "runtime exceeded"				#this could be true only if the child stopped by the signal
	      runtime = -1	
					
	#print
	#print "Command    :" + command
	#print "T0         :" + str(t0)	        
        #print "Failed     :" + str(has_Failed)
        #print "Stopped    :" + str(has_stopped)
        #print "Status     :" + str(run_status)        
        
        dic = dict()	
        dic['run_status'] = run_status
        dic['runtime'] = runtime
        
        #print "Dictionary :" + str(dic)
        #print
        return dic

# to test this code, just enter a valid command in run below and a time u require in seconds	
if __name__ == "__main__":
    execute("python abc1.py", "python abc1.py", 10)    
