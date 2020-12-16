# in this code i'm assuming that the input is valid as described in the assignment description

import enum
import json
from urllib.parse import urlparse


# function that checks if a string is a valid json
def isJson(body):
    try:
        return json.loads(body)
    except ValueError as e:
        return False


# getting from user a file path to a file containing a sequence of HTTP 1.1 messages and their responses.
filePath = input("enter file path:")
f = open(filePath, "r", encoding="utf-8")
lines = f.readlines()

# true if we reach a crlf line, false otherwise
endOfMessage = False

#list of requests
req = []

#list of responses
res = []
isReq = False

#Represents a CR-LF, a line with 80 "-"
crlf = ""

for i in range(80):
    crlf += "-"

#enum with the different parts of Http message
class message(enum.Enum):
    firstLine = 1
    header = 2
    messageBody = 3


messageSection = message.firstLine
body = ""
headerParameters = ""

#reading the file line by line and getting the necessary information about the messages.
for line in lines:

    #checking if we reached a crlf line
    if line == crlf or line == crlf + "\n":

        #if this is the second crlf line then the message ended
        if endOfMessage:

            #checking if the corrent massage is a request or response and creating a string with the information
            #about the message
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

                #adding the info about the request to the req list.
                req.append(messageInfo)
            else:
                messageInfo = "payload:\n"
                if (isJson(body) != False):
                    messageInfo += str(isJson(body)) + "\n"
                else:
                    messageInfo += body

                # adding the info about the response to the req list.
                res.append(messageInfo)

            #reseting the variables
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
        #splitting the first line of the message to words.
        words = line.split()

        #the method of the req is the first word in the ine and the end-point is the second.
        method = words[0]
        endPoint = words[1]

        #if the first word of the message is HTTP/1.1 then the message is response
        if words[0] == "HTTP/1.1":
            isReq = False
        else:
            isReq = True

        #after the first line comes the header
        messageSection = message.header
        continue

    if messageSection == message.header:

        #if the line is empty then the body of the message starts in the next line
        if line == "\n":
            messageSection = message.messageBody
            continue

        #adding the header arguments to the headerParameters variable
        if line.split()[0] != "Host:":
            headerParameters += line
        continue

    #adding the body of the message to the body variable
    if messageSection == message.messageBody:
        body += line
        continue

#printing the information about the requests and responses.
for i in range(len(req)):
    print("Req_" + str(i + 1) + ":\n\n" + req[i])
    print("Res_" + str(i + 1) + ":\n\n" + res[i])
