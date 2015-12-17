# Echo client program
import socket, sys, getopt, os, base64
import rsa

HOST = '127.0.0.1'
#HOST = '147.46.242.21'  # The remote host
PORT = 8080        # The same port as used by the server

def main(argv):
    pattern = ''
    try:
        opts, args = getopt.getopt(argv,"hrs")
    except getopt.GetoptError:
        print 'socket_client.py -h'
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print 'test.py <access type>'
            print '<access type> : -s -> for sequential'
            print '              : -r -> for random'
            sys.exit()
        elif opt in ("-s"):
            pattern = 0 #SEQUENTIAL
        elif opt in ("-r"):
            pattern = 1 #RANDOM

    #make socket connection to server
    print "Connecting to server..."
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((HOST, PORT))
    print "Connect to server complete !!"

    print "Sending file to server for writing..."
    
    
    (pubkey, privkey) = rsa.newkeys(1024)
    db = []
    i = 0

    
    myFile = open("mydbgenrsa","rb")
    while True:
        val = myFile.read(117)
        if not val:
            break

        enc = rsa.encrypt(val, pubkey)
        db.append(enc)
        s.send(enc)
    myFile.close()
    print "Complete sending file for writing !!"
    
    #SEQUENCTIAL
    if pattern == 0 :
        #SEND DBGEN TO SERVER && SEND TRACGER_SEQ TO SERVER
        print "Sending sequential pattern to server..."
       
        myFile = open("mytracegen","r")
        for line in myFile.readlines():
            val = line.split()
            #print "Client send - " + val[0]
            s.send(val[0])
            data = s.recv(117)
            #print 'Received data :: '+ data

            #DECRYPT AFTER RECEIVED
            message = rsa.decrypt(db[i], privkey)
            i += 1
        myFile.close()        
        
    #RANDOM    
    else: 
        #SEND DBGEN TO SERVER && SEND TRACGER_SEQ TO SERVER        
        print "Sending random pattern to server & retrieving data from server..."
        
        myFile = open("mytracegen","r")
        for line in myFile.readlines():
            val = line.split()
            #print "Client send - " + val[0]
            s.send(val[0])
            data = s.recv(1024*2)
            #print 'Received data :: '+ data

            #DECRYPT AFTER RECEIVED
            message = rsa.decrypt(data, privkey)           
        myFile.close()
    
    print "Complete retreiving data from server !!"
    s.close()
    print "Connection to server is closed !!"
        
if __name__ == "__main__":
    main(sys.argv[1:])
