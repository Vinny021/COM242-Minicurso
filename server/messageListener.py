import json
import stomp

class MessageListener(stomp.ConnectionListener):
    def __init__(self, conn, clientId):
        self.conn = conn
        self.clientId = clientId

    def on_error(self, frame):
        print('\nreceived an error "%s"' % frame.body)

    def on_message(self, frame):
        data = json.loads(frame.body)

        print('\nMessageListener received a message "%s"' % data['body'])
        
        if(data['body'][:5] == 'diga '):
            sendData = json.dumps({ "clientId": data['clientId'], "body": data['body'][5:] })
            self.conn.send(body=''.join(sendData), destination='/topic/response')