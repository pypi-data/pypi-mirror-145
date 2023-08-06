import socket

msgFromClient       = "Test Message from Samanvay"

bytesToSend         = str.encode(msgFromClient)

serverAddressPort   = ("10.20.0.85", 1234)


# Create a UDP socket at client side

UDPClientSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)

 

# Send to server using created UDP socket

UDPClientSocket.sendto(bytesToSend, serverAddressPort)

