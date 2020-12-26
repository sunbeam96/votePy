import zmq

context = zmq.Context()
socket = context.socket(zmq.REQ)
socket.connect("tcp://localhost:5555")

#  Do 10 requests, waiting each time for a respons
def sendMsg(message):
    print("Sending request %s …")
    socket.send(message)

    response = socket.recv()
    print("Received reply %s [ %s ]" % (response))