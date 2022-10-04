import stomp
import uuid
import time
from messageListener import MessageListener
from fileListener import FileListener
from functionListener import FunctionListener

def tryConnect(conn):
    try:
        clientId = str(uuid.uuid4())
        conn.connect('admin', 'admin', wait=True, headers={'client-id': clientId})
        return clientId
    except:
        print("ID "+ str(clientId)+" já existe" )
        return ''

IP = '127.0.0.1'
PORT = 61613

#Configuração do messageListener
messageConn = stomp.Connection([(IP, PORT)])

messageListenerId = ''
while(len(messageListenerId) == 0):
    messageListenerId = tryConnect(messageConn)

print("Message ID: ", messageListenerId)
messageConn.set_listener('messageListener', MessageListener(messageConn, messageListenerId))
messageConn.subscribe('/queue/message', id=messageListenerId)

#Configuração do fileListener
fileConn = stomp.Connection([(IP, PORT)])

fileListenerId = ''
while(len(fileListenerId) == 0):
    fileListenerId = tryConnect(fileConn)

print("File ID: ", fileListenerId)
fileConn.set_listener('fileListener', FileListener(fileConn, fileListenerId))
fileConn.subscribe('/queue/file', id=fileListenerId)

#Configuração do functionListener
functionConn = stomp.Connection([(IP, PORT)])

functionListenerId = ''
while(len(functionListenerId) == 0):
    functionListenerId = tryConnect(functionConn)

print("Function ID: ", functionListenerId)
functionConn.set_listener('functionListener', FunctionListener(functionConn, functionListenerId))
functionConn.subscribe('/queue/function', id=functionListenerId)

op = 1
while op != 0:
    op = int(input('Digite 0 para sair: '))

time.sleep(2)
messageConn.disconnect()
fileConn.disconnect()
functionConn.disconnect()