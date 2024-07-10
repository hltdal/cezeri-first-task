import socket
import pandas as pd
import pickle
import time

#veri okuma
with open("files.csv", "r") as file:
    df=pd.read_csv(file)
print(df)
data=df.values.tolist()
file.close()
#print(data)

def send_data(connection, veri):
    for sira, veri in enumerate(veri):
        try:
            print(f"Data: {sira} : {veri}")
            connection.sendall(pickle.dumps(veri))
            print("Data sent to the client")
            time.sleep(0.5)
        except:
            print("Data could not be sent to the client")
            return False
    return True

try:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.bind((socket.gethostbyname(socket.gethostname()), 5050))
        server_socket.listen()
        print("Server is listening...")
        connection, address=server_socket.accept()
        with connection:
            while True:
                #verileri sırasıyla gönder
                if not send_data(connection, data):
                    break
                #verileri ters sırayla gönder
                if not send_data(connection, data[::-1]):
                    break
except:
    print("Server could not be created")
    exit()
