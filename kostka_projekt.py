import socket
from gui import Ui_MainWindow
from PyQt5 import QtCore, QtWidgets


# updating label text
def update_data():
    data = client.recv(size)
    global previous_value
    if data:
        data = int.from_bytes(data, "little")
    if data in dice_value:
        if data != previous_value:
            print(data)
            ui.label_2.setText("Dice value is: \n" + str(data))
            previous_value = data
    if data == 7:
        if data != previous_value:
            print("Waiting for roll")
            ui.label_2.setText("Waiting for roll")
            previous_value = data
    elif data == 8:
        if data != previous_value:
            print("Rolling")
            ui.label_2.setText("Rolling")
            previous_value = data
    elif data == 9:
        if data != previous_value:
            print("Dice value is")
            ui.label_2.setText("Dice value is:")
            previous_value = data


if __name__ == "__main__":
    import sys
    #bluetooth initialization
    hostMACAddress = '0C:7A:15:D6:8D:04'  # The MAC address of a Bluetooth adapter on the server. The server might have multiple Bluetooth adapters.
    port = 5  # 3 is an arbitrary choice. However, it must match the port used by the client.
    backlog = 1
    size = 1024
    s = socket.socket(socket.AF_BLUETOOTH, socket.SOCK_STREAM, socket.BTPROTO_RFCOMM)
    s.bind((hostMACAddress, port))
    s.listen(backlog)
    # global values
    dice_value = [1, 2, 3, 4, 5, 6]
    previous_value = 0
    # PyQt setup
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    # bluetooth connection
    client, address = s.accept()
    # label update timer
    timer = QtCore.QTimer()
    timer.timeout.connect(update_data)
    timer.start(10)
    sys.exit(app.exec_())


