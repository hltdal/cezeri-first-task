import socket
import matplotlib.pyplot as plt
import pickle
import numpy as np
from sklearn.linear_model import LinearRegression

prediction = [] #It stores the predicted points
errors = []  #It stores the errors of the predictions

# The function that processes the last 5 data points and predicts the next point
def process_last_5(data):
    # last_5[i][0]=cords x, last_5[i][1]=cords y
    last_5 = data[-5:]
    if len(last_5)>=2: #It needs at least 2 data points to predict the next point
        # Fit a linear regression model to the last 5 data points
        x = np.array([point[0] for point in last_5]).reshape(-1, 1)
        y = np.array([point[1] for point in last_5])
        # Assuming that given 5 points follow a linear trend, you can model this trend using linear regression and predict point 6
        model=LinearRegression()
        model.fit(x, y)
        x6=last_5[-1][0]+(last_5[-1][0]-last_5[-2][0])
        y6=model.predict([[x6]])
        global prediction, errors
        # Store the prediction
        prediction.append((round(x6,2) ,round(y6[0],2)))
        print("Prediction: ", prediction[-6:])
        # After making the initial guess take the actual value and record the errors after the error is calculated
        if len(prediction)>=2: # It needs at least 2 predictions to calculate the error of the prediction
            # Calculate and store the error
            errors.append(round(abs((prediction[-2][1] - last_5[-1][1])/last_5[-1][1]*100),2))
            print("Errors: ", errors[-6:])
    return last_5

# The function that receives data from the server
def receive_data(client_socket):
    data=client_socket.recv(4096)
    if not data:
        raise ConnectionError("Data could not be received from the server")
    return pickle.loads(data)


# Initial empty data for cords_x and cords_y
x = [0] * 5
y = [0] * 5

# Create a figure and axis for data visualization
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 8))
line, = ax1.plot(x, y)
scatter = ax1.scatter(x, y, label='Data Points', color='b')
line_prediction, = ax1.plot([], [], color='r')
scatter_prediction = ax1.scatter([], [], color='r', marker='o', label='Predictions Points')
line_new_prediction, = ax1.plot([], [], color='g')
scatter_new_prediction = ax1.scatter([], [], color='g', marker='x', label='New Prediction Point')
ax1.set_xlabel('Cords X')
ax1.set_ylabel('Cords Y')
ax1.set_title('Real Time Data Visualization')

# Create a figure and axis for error visualization
error_line, = ax2.plot([], [], label='Prediction Error', color='m')
error_scatter = ax2.scatter([], [], color='m', marker='o', label='Error Points')
ax2.set_xlabel('Time')
ax2.set_ylabel('Error')
ax2.set_title('Prediction Error Over Time')


# Update the data and error visualization (making real-time)
def update(frame):
    global x, y, scatter, prediction, scatter_prediction, scatter_new_prediction, errors, error_line, error_scatter
    x = [point[0] for point in frame]
    y = [point[1] for point in frame]
    line.set_ydata(y)
    line.set_xdata(x)
    scatter.set_offsets(np.c_[x, y])
    if len(prediction) >= 1: # It needs at least 1 prediction to visualize (drawing lines and points for predictions)
        pred_x = [point[0] for point in prediction[-6:]]
        pred_y = [point[1] for point in prediction[-6:]]
        line_prediction.set_ydata(pred_y[:-1])
        line_prediction.set_xdata(pred_x[:-1])
        scatter_prediction.set_offsets(np.c_[pred_x[:-1], pred_y[:-1]])
        scatter_new_prediction.set_offsets(np.c_[pred_x[-1:], pred_y[-1:]])
        line_new_prediction.set_ydata(pred_y[-1:])
        line_new_prediction.set_xdata(pred_x[-1:])
    if len(errors) >= 1: # It needs at least 1 error to visualize (drawing lines and points for errors)
        error_line.set_ydata(errors[-6:])
        error_line.set_xdata(range(len(errors[-6:])))
        error_scatter.set_offsets(np.c_[range(len(errors[-6:])), errors[-6:]])
    ax1.relim()
    ax1.autoscale_view()
    ax2.relim()
    ax2.autoscale_view()
    return line,scatter,line_prediction, scatter_prediction, line_new_prediction, scatter_new_prediction, error_line, error_scatter

# The client receives the data from the server, processes the last 5 data points, and visualizes them.
def get_data():
    my_data = []
    server_ip = socket.gethostbyname(socket.gethostname()) # Get the IP address of the server
    server_port = 5050
    try:  #If the server is available, the client will be created
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
            client_socket.connect((server_ip, server_port))
            while True:
                try:
                    # Receives data from the server through the function receive_data
                    data = receive_data(client_socket)
                    my_data.append(data)
                    print("Data received from the server")
                    # Processes the last 5 data points through the function process_last_5
                    last_5 = process_last_5(my_data)
                    print("Last 5 data: ", last_5)
                    # Visualize the last 5 data points and predictions through the function update
                    update(last_5)
                    plt.pause(0.5) 
                except ConnectionError as e: #If the data cannot be received from the server, the client will be closed
                    print(e)
                    break
    except ConnectionRefusedError: #If the server is not available, the client will not be created
        print("Server is not available")

plt.ion()  # Turn on interactive mode for matplotlib
get_data()
ax1.legend()
ax2.legend()
plt.show()
