import socket


# bluetooth initialization
def bluetooth_Init():
    server_mac = '0C:7A:15:D6:8D:04'
    port = 5
    s = socket.socket(socket.AF_BLUETOOTH, socket.SOCK_STREAM, socket.BTPROTO_RFCOMM)
    s.connect((server_mac, port))
    return s
