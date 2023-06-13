from locale import normalize
from pickle import APPEND
import tkinter as tk
from turtle import update
from tensorflow import keras
import pandas as pd
import datetime
from datetime import datetime, timedelta
from geopy import distance
from PIL import ImageTk, Image

root= tk.Tk()
root.title('NCT Parking Recommendation System')      #Title of window

canvas = tk.Canvas(root, width = 800, height = 500,  relief = 'raised') #set size of window
canvas.pack()

#title
title = tk.Label(root, text='NCT Parking Recommendation System')  #Title of application
title.config(font=('ariel', 25))
canvas.create_window(200, 25, window=title)

title.place(relx = 0.5,
            rely = 0.1,
            anchor = 'center')

def take_long_lat():                    #get longitude and latitude value from entry box
   global longitude_entry
   global latitude_entry
   longitude = longitude_entry.get()
   latitude = latitude_entry.get()
   return (latitude, longitude)

longitude = tk.Label(root, text='Longitude:')          #longitude
longitude.config(font=('ariel', 15))
canvas.create_window(200, 100, window=longitude)

longitude.place(relx = 0.1,
            rely = 0.25,
            anchor = 'w')

longitude_entry = tk.Entry(root) 
canvas.create_window(200, 140, window=longitude_entry)

longitude_entry.place(relx = 0.23,
                    rely = 0.25,
                    anchor = 'w')
                                                           
latitude = tk.Label(root, text='Latitude:')             #latitude
latitude.config(font=('ariel', 15))
canvas.create_window(200, 100, window=latitude)

latitude.place(relx = 0.1,
            rely = 0.35,
            anchor = 'w')

latitude_entry = tk.Entry(root) 
canvas.create_window(200, 140, window=latitude_entry)

latitude_entry.place(relx = 0.23,
                    rely = 0.35,
                    anchor = 'w')

def selected_lot():                         #select parking lot
    global choice
    choice = clicked.get()

    longitude_entry.delete(0, tk.END)
    latitude_entry.delete(0, tk.END)

    if choice == parking_lots_options[0]:       #enters longitude and latitude to entry box
        long = "-1.1503980594365735"
        lat = "52.949666417482785"
    elif choice == parking_lots_options[1]:
        long = "-1.1524275998036517"
        lat = "52.955225480573894"
    elif choice == parking_lots_options[2]:
        long = "-1.1661435016548733"
        lat =  "52.965485966616875"
    elif choice == parking_lots_options[3]:
        long = "-1.1958643710741508"
        lat = "53.03784591146996"
    elif choice == parking_lots_options[4]:
        long =  "-1.1446963920612943"
        lat =  "52.95929284644711"
    elif choice == parking_lots_options[5]:
        long = "-1.1451816387888538"
        lat="52.95240000227503"
    elif choice == parking_lots_options[6]:
        long="-1.187411217105727"
        lat= "53.014652654006916"
    elif choice == parking_lots_options[7]:
        long="-1.14"
        lat="52.95"
    elif choice == parking_lots_options[8]:
        long="-1.1554536766311803"
        lat="52.9529470115942"
    elif choice == parking_lots_options[9]:
        long="-1.1666993275731934"
        lat="52.92870917989375"
    elif choice == parking_lots_options[10]:
        long="-1.153754957585276"
        lat="52.95186370746648"
    elif choice == parking_lots_options[11]:
        long="-1.1441963813046423"
        lat="52.95793491224213"
    elif choice == parking_lots_options[12]:
        long="-1.1435093882723208"
        lat="52.95259272957111"
    elif choice == parking_lots_options[13]:
        long="-1.1494252864209336"
        lat="52.95662350856339"
    elif choice == parking_lots_options[14]:
        long="-1.1461637463654573"
        lat="52.95684938034469"
    elif choice == parking_lots_options[15]:
        long="-1.178014001763845"
        lat="52.97288075329784"

    longitude_entry.insert(tk.END, long)
    latitude_entry.insert(tk.END, lat)

parking_lots_options = ["Arndale", "Euro", "Forest Park and Ride", "Hucknall Park and Ride", "Huntingdon Street",       #drop down menu menu
                        "Lace Market", "Moor Bridge Park and Ride", "Mount St Lower", "Mount Street",
                        "Queens Drive Park and Ride", "St. James Street", 'St. Marks Place', "Stoney Street", 
                        "Trinity Square CP", "Victoria Centre STH", "Wilkinson Street Park and Ride"]

clicked = tk.StringVar()

drop = tk.OptionMenu(root , clicked , *parking_lots_options, command = selected_lot)    # Create Dropdown menu
drop.pack()

drop.place(relx = 0.15,
           rely = 0.45,
           anchor = 'center')

def selected_prediction_spectrum():         #select prediction spectrum
    global spectrum
    spectrum = predictive_spectrum.get()

predictive_spectrum_options = ["Now", "5 minutes", "10 minutes", "20 minutes", "30 minutes", "1 hour"]

predictive_spectrum = tk.StringVar()

predictive_spectrum.set("Now")

predictive_spectrum_drop = tk.OptionMenu(root, predictive_spectrum, *predictive_spectrum_options, command=selected_prediction_spectrum)

predictive_spectrum_drop.place(relx = 0.15,
                               rely = 0.55,
                               anchor='center')

def findLotDist(coords):           # finding distance of entered location and parking lot
    global shortest_dist

    options = [("Arndale", (52.94966641748278, -1.1503980594365735)), 
                ("Euro", (52.955225480573894, -1.1524275998036517)), 
                ("Forest Park and Ride", (52.965485966616875, -1.1661435016548733)), 
                ("Hucknall Park and Ride", (53.03784591146996, -1.1958643710741508)), 
                ("Huntingdon Street", (52.95929284644711, -1.1446963920612943)), 
                ("Lace Market", (52.95240000227503, -1.1451816387888538)), 
                ("Moor Bridge Park and Ride", (53.014652654006916, -1.187411217105727)), 
                ("Mount St Lower", (52.95, -1.14)), 
                ("Mount Street", (52.9529470115942, -1.1554536766311803)), 
                ("Queens Drive Park and Ride", (52.92870917989375, -1.1666993275731934)), 
                ("St. James Street", (52.95186370746648, -1.153754957585276)), 
                ('St. Marks Place', (52.95793491224213, -1.1441963813046423)), 
                ("Stoney Street", (52.95259272957111, -1.1435093882723208)), 
                ("Trinity Square CP", (52.95662350856339, -1.1494252864209336)), 
                ("Victoria Centre STH", (52.95684938034469, -1.1461637463654573)), 
                ("Wilkinson Street Park and Ride", (52.97288075329784, -1.178014001763845))]

    shortest_dist = distance.distance(coords, options[0][1]).km
    result = options[0][0]

    all_dist = []

    for option in options:
        all_dist.append((option[0], distance.distance(coords, option[1]).km))

    all_dist.sort(key=lambda option: option[1])

    shortest_dist = all_dist[0:2]

    return all_dist[0]

def predict():
    dt = datetime.now()             # get current datetime  
    
    global prediction
    global spectrum
    global choice
    selected_lot()
    selected_prediction_spectrum()
    findLotDist(take_long_lat())[0]
    

    result_box.configure(state='normal')
    parking_lot_result.configure(state='normal')
    shortest_dist_box.configure(state='normal')
    lowest_PO_box.configure(state='normal')
    
    result_box.delete(1.0,tk.END)
    parking_lot_result.delete(1.0, tk.END)
    shortest_dist_box.delete(1.0, tk.END)
    lowest_PO_box.delete(1.0, tk.END)
    
    if spectrum == "Now":                           #adding time to current time based on prediction spectrum
        updated_time = dt
    elif spectrum == "5 minutes":
        updated_time = dt + timedelta(minutes=5)
    elif spectrum == "10 minutes":
        updated_time = dt + timedelta(minutes=10)
    elif spectrum == "20 minutes":
        updated_time = dt + timedelta(minutes=20)
    elif spectrum == "30 minutes":
        updated_time = dt + timedelta(minutes=30)
    elif spectrum == "1 hour":
        updated_time = dt + timedelta(minutes=60)  
    
    day = dt.day    
    hour = updated_time.hour
    minute = updated_time.minute
    weekday = dt.weekday()
    
    data = {'Day': day, 'Weekday': weekday, 'Hour': hour, 'Minute': minute}  
    df = pd.DataFrame(data, index = [0])

    prefix = "App/Parking Occupancy Prediction Models/"                       # prefix of file location of prediction model

    parking_lot = []
    parking_percentage = []
    parking_distance = []
    penalty_list = []

    for i in range(2):                          
        choice = shortest_dist[i][0]    # getting name of the parking lot

        if choice == parking_lots_options[0]:
            norm_value_mean = [15.906864, 3.474817, 11.632366, 28.972476]       # mean statistics for data normalising
            norm_value_std = [8.862515, 1.961378, 6.765432, 16.310415]          # standard deviation for data normalising
            model = keras.models.load_model(prefix + 'Arndale.h5')               # model loaded based on parking lot
        elif choice == parking_lots_options[1]:
            norm_value_mean = [15.935187, 3.304877, 11.136535,29.759651]
            norm_value_std = [8.908989,1.994872,6.555085,16.522629]
            model = keras.models.load_model(prefix +'Euro.h5')
        elif choice == parking_lots_options[2]:
            norm_value_mean = [15.938842, 3.285747, 11.261421,27.855413]
            norm_value_std = [8.914013, 1.997773, 6.564768, 16.382039]
            model = keras.models.load_model(prefix+'Forest Park and Ride.h5')
        elif choice == parking_lots_options[3]:
            norm_value_mean = [15.906693,3.474646,11.638191,29.340110]
            norm_value_std = [8.862311,1.961463,6.770623, 16.600109]
            model = keras.models.load_model(prefix+'Hucknall Park and Ride.h5')
        elif choice == parking_lots_options[4]:
            norm_value_mean = [15.926393,3.357640,11.358954,29.369575]
            norm_value_std = [8.894595, 1.986090, 6.580869,116.404055]
            model = keras.models.load_model(prefix+'Huntingdon Street.h5')
        elif choice == parking_lots_options[5]:
            norm_value_mean = [15.937757,3.239459,10.953004,29.165487]
            norm_value_std = [8.913188, 1.997167, 6.701660, 16.188944]
            model = keras.models.load_model(prefix+'Lace Market.h5')
        elif choice == parking_lots_options[6]:
            norm_value_mean = [15.906864, 3.474817, 11.634765, 29.332857]
            norm_value_std = [8.862515, 1.961378, 6.771451, 16.115441]
            model = keras.models.load_model(prefix+'Moor Bridge Park and Ride.h5')
        elif choice == parking_lots_options[7]:
            norm_value_mean = [15.920055,3.395672,11.500457,29.487494]
            norm_value_std = [8.884201,1.978864,6.638800,16.538945]
            model = keras.models.load_model(prefix+'Mount St Lower.h5')
        elif choice == parking_lots_options[8]:
            norm_value_mean = [15.933531,3.314813,11.099018,29.719450]
            norm_value_std = [8.906281,1.993328,6.635334,16.386543]
            model = keras.models.load_model(prefix+'Mount Street.h5')
        elif choice == parking_lots_options[9]:
            norm_value_mean = [20.931076,3.495146,13.400811,29.368661]
            norm_value_std = [8.107861, 1.760738,7.408975,14.939220]
            model = keras.models.load_model(prefix+'Queens Drive Park and Ride.h5')
        elif choice == parking_lots_options[10]:
            norm_value_mean = [15.936729, 3.295626, 10.975331,29.032378]
            norm_value_std = [8.911509, 1.996264,6.697479,16.270191]
            model = keras.models.load_model(prefix+'St. James Street.h5')
        elif choice == parking_lots_options[11]:
            norm_value_mean = [15.938100,3.287403,11.024669,30.100845]
            norm_value_std = [8.913748, 1.997476,6.591213,16.795855]
            model = keras.models.load_model(prefix+'St. Marks Place.h5')
        elif choice == parking_lots_options[12]:
            norm_value_mean = [15.936729,3.295626,11.003826,29.315955]
            norm_value_std = [8.911509,1.996264,6.656980,16.180219]
            model = keras.models.load_model(prefix+'Stoney Street.h5')
        elif choice == parking_lots_options[13]:
            norm_value_mean = [15.937357,3.291857,10.962540,29.990863]
            norm_value_std = [8.912535,1.996818,6.702738,16.318521]
            model = keras.models.load_model(prefix+'Trinity Square CP.h5')
        elif choice == parking_lots_options[14]:
            norm_value_mean = [15.933474,3.315155,11.102615,30.667999]
            norm_value_std = [8.906187,1.993274,6.641228,16.459751]
            model = keras.models.load_model(prefix+'Victoria Centre STH.h5')
        elif choice == parking_lots_options[15]:
            norm_value_mean = [23.200891,3.715110,7.010279,34.072236]
            norm_value_std = [3.806880,1.473108,6.612772,12.980320]
            model = keras.models.load_model(prefix+'Wilkinson Street Park and Ride.h5')
        else:
            print("Parking lot does not exist")
        
        normed_data = (df - norm_value_mean) / norm_value_std       # normalising data
        prediction = model.predict(normed_data)                     # predicting parking occupancy
        prediction = prediction[0][0]                               
        rounded_prediction = round(prediction)                      # rounding prediction
        parking_percentage.append(rounded_prediction)               # appending parking prediction in a list
        parking_lot.append(choice)                                  # appending parking lot name in a list
        parking_distance.append(shortest_dist[i][1])                # appending parking lot distance in a list

    lowest_percentage = min(parking_percentage)                     # selecting parking lot with lowest predicted parking occupancy
    lowest_dist = min(parking_distance)                             # selecting parking lot with shortest distance

    lowest_PO_index = parking_percentage.index(lowest_percentage)   # getting index of parking lot with the lower parking occupancy
    shortest_dist_index = parking_distance.index(lowest_dist)       # getting index of parking lot with the shorter distance

    if lowest_dist == 0:
        lowest_dist_ratio = 0.01                                    # to prevent division by 0
    else:
        lowest_dist_ratio = lowest_dist

    if lowest_percentage == 0:
        lowest_percentage_ratio = 0.01
    else:
        lowest_percentage_ratio = lowest_percentage
 
    scaled_PO_0 = parking_percentage[0]/lowest_percentage_ratio          # ratio calculating
    scaled_dist_0 = parking_distance[0]/lowest_dist_ratio

    scaled_PO_1 = parking_percentage[1]/lowest_percentage_ratio
    scaled_dist_1 = parking_distance[1]/lowest_dist_ratio

    scale_val = scale.get()                                         # priority penalty multiplier
    if scale_val == 1:
        dist_priority = 4
        PO_priority = 0
    elif scale_val == 2:
        dist_priority = 3
        PO_priority = 1
    elif scale_val == 3:
        dist_priority = 2
        PO_priority = 2
    elif scale_val == 4:
        dist_priority = 1
        PO_priority = 3
    elif scale_val == 5:
        dist_priority = 0
        PO_priority = 4

    penalty_0 = scaled_PO_0 * PO_priority + scaled_dist_0 * dist_priority      # penalty calculation
    penalty_1 = scaled_PO_1 * PO_priority + scaled_dist_1 * dist_priority

    penalty_list = [penalty_0, penalty_1]
    
    min_penalty = min(penalty_list)                                 # getting parking lot with a lower penalty
    min_penalty_index = penalty_list.index(min_penalty)

    result_box_string = parking_percentage[min_penalty_index],"%"

    result_box.insert(tk.END, result_box_string)                            # inserting parking occupancy result into result box 
    parking_lot_result.insert(tk.END, parking_lot[min_penalty_index])       # inserting result of selected parking lot
    shortest_dist_box.insert(tk.END, parking_lot[shortest_dist_index])      # inserting parking lot with shortest distance
    lowest_PO_box.insert(tk.END, parking_lot[lowest_PO_index])              # inserting parking lot with lowest parking occupancy

    result_box.configure(state='disabled')
    parking_lot_result.configure(state='disabled')
    shortest_dist_box.configure(state='disabled')
    lowest_PO_box.configure(state='disabled')


predict_button = tk.Button(root, text ="Find Best Parking Lot", height=5, width=40, command=predict)     # predict button

predict_button.place(relx = 0.5,
                    rely = 0.22)


parking_lot_result = tk.Text(root, height=0.5, width=30)         
parking_lot_result.pack()

parking_lot_result.place(relx=0.63,
                         rely=0.75)

result_box_label = tk.Label(root, text='Final parking lot chosen:')
result_box_label.config(font=('ariel', 10))

result_box_label.place(relx = 0.42,
                    rely = 0.75)

result_box = tk.Text(root, height=0.5, width=4)
result_box.configure(state='disabled')

result_box.place(relx=0.63,
                rely=0.85)

result_box_label = tk.Label(root, text='Predicted parking occupancy:')
result_box_label.config(font=('ariel', 10))

result_box_label.place(relx = 0.39,
                    rely = 0.85)
            
scale = tk.Scale(root, from_=1, to=5, orient=tk.HORIZONTAL, length=250)
scale.set(3)
scale.place(relx=0.3,
            rely=0.4)

scale_distance_label = tk.Label(root, text='Distance')
scale_distance_label.config(font=('ariel', 8))

scale_distance_label.place(relx = 0.3,
                           rely = 0.48)

scale_PO_label = tk.Label(root, text='Parking Occupancy')
scale_PO_label.config(font=('ariel', 8))

scale_PO_label.place(relx = 0.49,
                     rely = 0.48)  

shortest_distance_label = tk.Label(root, text='Parking lot with shortest distance:')
shortest_distance_label.config(font=('ariel', 10))

shortest_distance_label.place(relx = 0.35,
                            rely = 0.54)

shortest_dist_box = tk.Text(root, height=0.5, width=30)
shortest_dist_box.configure(state='disabled')
shortest_dist_box.pack()

shortest_dist_box.place(relx=0.63,
                        rely=0.55)

lowest_PO_label = tk.Label(root, text='Parking lot with lowest parking occupancy:')
lowest_PO_label.config(font=('ariel', 10))

lowest_PO_label.place(relx = 0.29,
                    rely = 0.64)

lowest_PO_box = tk.Text(root, height=0.5, width=30)
lowest_PO_box.configure(state='disabled')
lowest_PO_box.pack()

lowest_PO_box.place(relx=0.63,
                    rely=0.65)

# Insert image

# image = Image.open("Creator.jpg")
# resize_image = image.resize((106, 136))
# img = ImageTk.PhotoImage(resize_image)
# image = tk.Label(root, image = img)
# image.place(relx=0.09,
#             rely=0.6)

creator_label = tk.Label(root, text='Created By: Lim Yen Kai (2022)')
creator_label.config(font=('ariel', 10))

creator_label.place(relx = 0.06,
                    rely = 0.9)

supervisor_label = tk.Label(root, text='Supervised By: Prof. Peer-Olaf Siebers (2022)')
supervisor_label.config(font=('ariel', 10))

supervisor_label.place(relx = 0.06,
                    rely = 0.95)


root.mainloop()