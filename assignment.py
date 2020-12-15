import enum
import json


def printPayload(body):
  try:
    print(json.loads(body))
    print()
  except ValueError as e:
    print(body)
  return True


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

for line in lines:

    if line == crlf or line == crlf + "\n":
        if endOfMessage:

            if numOfMessage % 2 == 0:
                print("Res_" + str(int(numOfMessage/2)) + ":\n")
                print("payload:")
                printPayload(body)

            else:
                print("Req_" + str(int(numOfMessage/2 + 1)) + ":\n")
                print ("method: " + method)
                print ("end-point: " + endPoint)
                print()

            numOfMessage += 1
            messageSection = message.firstLine
            endOfMessage = False
            body = ""

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

    if messageSection == message.header and line == "\n":
        messageSection = message.messageBody
        continue

    if messageSection == message.messageBody:
        body += line
        continue