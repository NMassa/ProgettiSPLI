import socket                   # Import socket module

def caesar(plainText, shift): 
  cipherText = ""
  for ch in plainText:
    if ch.isalpha():
      stayInAlphabet = ord(ch) + shift 
      if stayInAlphabet > ord('z'):
        stayInAlphabet -= 26
      finalLetter = chr(stayInAlphabet)
      cipherText += finalLetter
  #print "Your ciphertext is: ", cipherText
  return cipherText
def server():
    port = 60000                    # Reserve a port for your service.
    s = socket.socket()             # Create a socket object
    host = socket.gethostname()     # Get local machine name
    s.bind((host, port))            # Bind to the port
    s.listen(1)                     # Now wait for client connection.

    print ('Server listening....')      

    while True:
        conn, addr = s.accept()     # Establish connection with client.
        #print ('Got connection from', addr)
        #data = conn.recv(1024)
        #print('Server received', str(data))
        print ("Insert Shift")
        shift=input()
        filename='Spli2.txt'
        f = open(filename,'rb')
        l=f.read(1024)
        cs = caesar(str(l),int(shift))
        tr=cs.encode()
        while (l):
           conn.send(tr)
           print('Sent ',repr(tr))
           l = f.read(1024)
           cs = caesar(str(l),int(shift))
           tr=cs.encode()
        f.close()

        print('Done sending')
        #conn.send('Thank you for connecting')
        conn.close()
        

def client():
    s = socket.socket()             # Create a socket object
    host = socket.gethostname()     # Get local machine name
    port = 60000                    # Reserve a port for your service.

    s.connect((host, port))
    #s.send(str("Hello server!"))

    with open('received_file.txt', 'wb') as f:
        print ('file opened')
        while True:
            print('receiving data...')
            data = s.recv(1024)
            print('data=%s', (data))
            if not data:
                break
            # write data to a file
            f.write(data)

    f.close()
    print('Successfully get the file')
    s.close()
    print('connection closed')

def menu():
    print('---1--- Send message    --')
    print('---2--- Receive message --')
    print('---0--- Exit            --')

if __name__ == '__main__':
    menu()
    print("Choose an option:")
    scelta=input()
    if ( scelta == '1'):
        server()
    if( scelta == '2'):
        client()
    #if( scelta == '0'):
     


