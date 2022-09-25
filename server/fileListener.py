import stomp
import json

class FileListener(stomp.ConnectionListener):
    def __init__(self, conn, clientId):
        self.conn = conn
        self.clientId = clientId

    def on_error(self, frame):
        print('\nreceived an error "%s"' % frame.body)

    def on_message(self, frame):
        data = json.loads(frame.body)

        print('\nFileListener received a message "%s"' % data['body'])
        
        if(len(data['body']) != 0):
            file = open('sample.txt', 'a')
            file.write(data['body']+'\n')
            file.close()

            sendData = json.dumps({ "clientId": data['clientId'], "body": 'Inserido no documento'})

            self.conn.send(body=''.join(sendData), destination='/topic/response')