# importing the required module 
import matplotlib.pyplot as plt 
from datetime import datetime

def parse_data(raw_data):
    x = []
    y = []
        
    for raw_data_entry in raw_data.splitlines():
        data = raw_data_entry.split(",")
        humid_one = data[0]
        humid_two = data[1]   
        humid_three = data[2]
        humid_four = data[3]
        data[4] = data[4] + " " + data[5]
        data[4] = data[4].strip(" ")
        data[4] = data[4].strip("\n")
        data[4] = data[4].strip("\r")
        date = datetime.strptime(data[4], '%m/%d/%Y %H:%M:%S')
        
        y.append(humid_one)
        x.append(date)
        
    return [x, y]

if __name__ == "__main__":
    data = "725,259,138,84,03/25/2020,21:00:02\n" \
           "723,211,197,151,03/25/2020,22:00:01\n"\
           "726,291,176,36,03/25/2020,23:00:02\n" \
           "730,270,149,93,03/26/2020,00:00:01\n" \
           "727,276,165,35,03/26/2020,01:00:01\n" \
           "731,257,165,104,03/26/2020,02:00:01\n"\
           "726,217,102,134,03/26/2020,03:00:01\n"\
           "726,222,141,123,03/26/2020,04:00:01\n"\
           "727,249,173,103,03/26/2020,05:00:01\n"\
           "726,291,159,155,03/26/2020,06:00:01\n"\
           "734,209,207,90,03/26/2020,07:00:01\n" \
           "732,289,149,178,03/26/2020,08:00:01\n"\
           "733,279,124,122,03/26/2020,09:00:01\n"\
           "735,209,124,122,03/26/2020,10:00:01\n"\
           "736,236,195,166,03/26/2020,11:00:01\n"\
           "728,284,210,165,03/26/2020,12:00:01\n"\
           "723,182,116,89,03/26/2020,13:00:01\n" \
           "723,176,147,126,03/26/2020,14:00:01\n"\
           "719,237,131,189,03/26/2020,15:00:01\n"\
           "710,208,141,27,03/26/2020,16:00:01\n" \
           "705,176,112,162,03/26/2020,17:00:01\n"  

    [x, y] = parse_data(data)
    
    # plotting the points 
    plt.plot(x, y) 

    # naming the x axis 
    plt.xlabel('x - axis') 
    # naming the y axis 
    plt.ylabel('y - axis') 

    # giving a title to my graph 
    plt.title('My first graph!') 

    # function to show the plot 
    plt.show() 
