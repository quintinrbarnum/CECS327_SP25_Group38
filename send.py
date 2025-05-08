import socket, ipaddress

serverIP = input('Please enter IP for host: ')

def is_valid_ip(ip_str):
    try:
        ipaddress.ip_address(ip_str)
        return True
    except ValueError:
        return False

while not is_valid_ip(serverIP):
    serverIP = input('Invalid IP. Please enter IP for host: ')
    is_valid_ip(serverIP)

serverPort = int(input('Please enter port: '))


myTCPSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
myTCPSocket.connect((serverIP, serverPort))
user_input = "0"
while user_input != "4":
    someData = input("""Select one of the options below: 
                 1. Average Moisture
                 2. Average Water Consumption
                 3. Most Electricity Consumed
                 4. Quit""")
    if(someData == "4" or someData.lower() == "quit"):
        break
    myTCPSocket.send(bytearray(str(someData), encoding='utf-8'))
    serverResponse = myTCPSocket.recv(512)
    print(serverResponse)
myTCPSocket.close()
