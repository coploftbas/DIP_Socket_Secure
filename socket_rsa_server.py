# Echo server program
import socket
import sys
from thread import *

HOST = ''   # Symbolic name meaning all available interfaces
PORT = 8080 # Arbitrary non-privileged port
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print 'Socket created'

#Bind socket to local host and port
try:
    s.bind((HOST, PORT))
except socket.error as msg:
    print 'Bind failed. Error Code : ' + str(msg[0]) + ' Message ' + msg[1]
    sys.exit()

print 'Socket bind complete'

#Start listening on socket
s.listen(10)
print 'Socket now listening'

#Function for handling connections. This will be used to create threads
def clientthread(conn):
    #infinite loop so that function do not terminate and thread do not end.
    i = 0
    j = 0
    db = []
    while True:
	#get data from client
        #data = conn.recv(1028)
	data = conn.recv(1032)
	
	if not data:
	    print "Done..." 
	    i = 0
	    j = 0
	    db = []
	    break	
	
	#print len(data)
        if len(data) == 128 or (i<1024): #1033:
        #if (len(data) == 1028) or (i<=10000):
	    if (i == 0):
		print "Receiving data from client to write..."
	    #print "i=",i," len=",len(data)
	    #tmp = data[4:].encode('utf8', errors='ignore')
            tmp = data.decode('utf-8', errors='ignore')
            #print tmp
            db.append(tmp)
            i += 1
        else:
            if ( j==0 ):
		print "Sending data back to client..."
		j += 1
	    #print 'db['+data+']::' + db[int(data)]
            #conn.sendall(db[int(data)])
	    conn.sendall(db[20])

    #came out of loop
    conn.close()

#now keep talking with the client
while 1:
    #wait to accept a connection - blocking call
    conn, addr = s.accept()
    print 'Connected with ' + addr[0] + ':' + str(addr[1])

    #start new thread takes 1st argument as a function name to be run, second is the tuple of arguments to the function.
    start_new_thread(clientthread ,(conn,))

s.close()
