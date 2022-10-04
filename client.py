import time
import stomp
import json

def tryConnect(conn, idInicial):
    try:
        clientId = 'clientId'+str(idInicial)
        conn.connect('admin', 'admin', wait=True, headers={'client-id': clientId})
        return clientId
    except:
        print("ID "+ str(clientId)+" já existe" )
        return ''

class ClientListener(stomp.ConnectionListener):
    def __init__(self, clientId):
        self.clientId = clientId

    def on_error(self, frame):
        print('received an error "%s"' % frame.body)

    def on_message(self, frame):
        data = json.loads(frame.body)
        print('\nReceived a message "%s"' % data['body'])

IP = '127.0.0.1'
PORT = 61613

conn = stomp.Connection([(IP, PORT)])

clientId = ''
idInicial = 1
while(len(clientId) == 0):
    clientId = tryConnect(conn, idInicial)
    idInicial += 1

print("Client ID: ", clientId)
conn.set_listener(str(clientId), ClientListener(clientId))
queueString = '/queue/response/' + clientId
conn.subscribe(queueString, id=clientId)

op = 1
while op != 0:
    print('=== Menu ===')
    print('0 - Sair')
    print('1 - Enviar uma mensagem')
    print('2 - Alterar aquivo de texto')
    print('3 - Calcular')

    op = int(input('Digite uma opção: '))

    if(op == 1):
        mensagem = input("Digite a mensage: ")
        
        data = { "clientId": clientId, "body": mensagem }
        sendData = json.dumps(data)
        
        conn.send(body=''.join(sendData), destination='/queue/message')
        time.sleep(1)
    
    if(op == 2):
        mensagem = input("Digite algo para inserir no arquivo : ")

        data = { "clientId": clientId, "body": mensagem }
        sendData = json.dumps(data)

        conn.send(body=''.join(sendData), destination='/queue/file')
        time.sleep(1)
    
    if(op == 3):
        print('1 - SOMA')
        print('2 - SUBTRAÇÃO')
        print('3 - DIVISÃO')
        print('4 - MULTIPLICAÇÃO')
        operacao = input("escolha a operação: ")

        num1 = input("Digite o primeiro número: ")
        num2 = input("Digite o segundo número: ")
        
        if(operacao == '3' and num2 == '0'):
            print("Não é possível fazer divisão por 0")
        else:
            data = {
                "1": num1,
                "2": num2,
                "op": operacao
            }

            jsonData = json.dumps(data)

            data = { "clientId": clientId, "body": jsonData }
            sendData = json.dumps(data)

            conn.send(body=''.join(sendData), destination='/queue/function')
            time.sleep(1)