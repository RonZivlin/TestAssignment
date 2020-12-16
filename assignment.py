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

numOfMessage = 1
endOfMessage = False

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

            if numOfMessage % 2 == 0:
                print("Res_" + str(int(numOfMessage/2)) + ":\n")
                print("payload:")
                if (isJson(body) != False):
                    print(isJson(body))
                else:
                    print(body)

            else:
                print("Req_" + str(int(numOfMessage/2 + 1)) + ":\n")
                print ("method: " + method)
                print ("end-point: " + endPoint)
                s = urlparse(endPoint).params
                print ("path parameters: " + str(urlparse(endPoint).params.split(';')))
                print ("query string parameters: " + str(urlparse(endPoint).query.split('&')))
                print ("body arguments: ")
                if (isJson(body) != False):
                    print(str(isJson(body)).replace(':', "="))
                else:
                    print()
                print ("header parameters:\n")
                print (headerParameters)

            numOfMessage += 1
            messageSection = message.firstLine
            endOfMessage = False
            body = ""
            headerParameters = ""

        else:
            endOfMessage = True

        continue
    else:
        endOfMessage = False

    if messageSection == message.firstLine:
        words = line.split()
        method = words[0]
        endPoint = words[1]
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