import stomp
import json

class FunctionListener(stomp.ConnectionListener):
    def __init__(self, conn, clientId):
        self.conn = conn
        self.clientId = clientId

    def on_error(self, frame):
        print('\nreceived an error "%s"' % frame.body)

    def on_message(self, frame):
        sentData = json.loads(frame.body) 
        body = sentData['body']

        print('\nFunctionListener received a message "%s"' % body)
        
        data = json.loads(body)

        result = 0
        match data['op']:
            case '1':
                result = float(data["1"]) + float(data["2"]) 
            case '2':
                result = float(data["1"]) - float(data["2"]) 
            case '3':
                result = float(data["1"]) / float(data["2"]) 
            case '4':
                result = float(data["1"]) * float(data["2"]) 

        bodyText = 'O resultado foi ' + str(result)

        sendData = json.dumps({ "clientId": sentData['clientId'], "body": bodyText})

        destinationString = '/queue/response/'+sentData['clientId']
        self.conn.send(body=''.join(sendData), destination=destinationString)