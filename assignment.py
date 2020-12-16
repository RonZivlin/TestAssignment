import enum
import json
from urllib.parse import urlparse

def isJson(body):
  try:
    return json.loads(body)
  except ValueError as e:
    return False


#getting from user a file path to a file containing a sequence of HTTP 1.1 messages and their responses.
filePath = input("enter file path:")
f = open(filePath, "r", encoding="utf-8")
lines = f.readlines()

endOfMessage = False
req = []
res = []
isReq = False

crlf = ""

for i in range(80):
    crlf += "-"

class message(enum.Enum):
   firstLine = 1
   header = 2
   messageBody = 3

messageSection = message.firstLine
body = ""
headerParameters = ""

for line in lines:

    if line == crlf or line == crlf + "\n":
        if endOfMessage:

            if isReq:
                messageInfo = "method: " + method + "\n"
                messageInfo += "end-point: " + endPoint + "\n"
                s = urlparse(endPoint).params
                messageInfo += "path parameters: " + str(urlparse(endPoint).params.split(';')) + "\n"
                messageInfo += "query string parameters: " + str(urlparse(endPoint).query.split('&')) + "\n"
                messageInfo += "body arguments:\n"
                if (isJson(body) != False):
                    messageInfo += str(isJson(body)).replace(':', "=") + "\n"
                else:
                    messageInfo += "\n"
                messageInfo += "header parameters:\n\n"
                messageInfo += headerParameters

                req.append(messageInfo)
            else:
                messageInfo = "payload:\n"
                if (isJson(body) != False):
                    messageInfo += str(isJson(body)) + "\n"
                else:
                    messageInfo += body

                res.append(messageInfo)

            messageSection = message.firstLine
            endOfMessage = False
            body = ""
            headerParameters = ""
            messageInfo = ""

        else:
            endOfMessage = True

        continue
    else:
        endOfMessage = False

    if messageSection == message.firstLine:
        words = line.split()
        method = words[0]
        endPoint = words[1]
        if words[0] == "HTTP/1.1":
            isReq = False
        else:
            isReq = True
        messageSection = message.header
        continue


    if messageSection == message.header:

        if line == "\n":
            messageSection = message.messageBody
            continue

        if line.split()[0] != "Host:":
            headerParameters += line
        continue

    if messageSection == message.messageBody:
        body += line
        continue

for i in range(len(req)):
        print ("Req_" + str(i + 1) + ":\n\n" + req[i])
        print ("Res_" + str(i + 1) + ":\n\n" + res[i])