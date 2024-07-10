import socket
import pandas as pd
import pickle
import time

# Taking the data(cords_x and cords_y) from the csv file
with open("files.csv", "r") as file:
    df=pd.read_csv(file)
print(df)
data=df.values.tolist()#convert the dataframe to a list
file.close()

# Function to send data to the client
def send_data(connection, veri):
    for sira, veri in enumerate(veri):
        try:#If the data is sent successfully, print the data
            print(f"Data: {sira} : {veri}")
            connection.sendall(pickle.dumps(veri))
            print("Data sent to the client")
            time.sleep(0.5)#Data is sent every 0.5 seconds
        except:#If the data is not sent successfully, print the error message
            print("Data could not be sent to the client")
            return False
    return True

try:#If the server is created successfully, print the message
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.bind((socket.gethostbyname(socket.gethostname()), 5050))
        server_socket.listen()
        print("Server is listening...")
        connection, address=server_socket.accept()
        with connection:#If the connection is successful with the client the data is sent to the client
            while True:
                #Send data in correct order to the client using the send_data function
                if not send_data(connection, data):
                    break
                #Send data in reverse order to the client using the send_data function
                if not send_data(connection, data[::-1]):
                    break
except:#If the server is not created successfully, print the error message
    print("Server could not be created")
    exit()
