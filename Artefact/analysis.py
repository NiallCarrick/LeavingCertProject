#Library used to read in csv files
import csv

#Datascience libraries used to help organise the data
import numpy as np
from numpy.polynomial.polynomial import polyfit
import pandas as pd

#Matplotlib used to output useful graphs
import matplotlib.pyplot as plt


hasLoaded = False

#Linear Regression model used to predict future data
from sklearn.linear_model import LinearRegression


try:
    with open("microbit.csv") as csv_file:
        #Skips header line of the csv file
        next(csv_file)
        
        
        
        totalData = {"Sleep":[],"Physical":[],"Screen":[]}
        
        csv_reader = csv.reader(csv_file, delimiter=",")
        
        #Picks out the relevant data from the csv fle for each day and converts it to a dictionary
        for row in csv_reader:
            
            if(int(row[1]) == -1):
                time = round(float(row[0]) - float(prevRow[0]),2)
                physical = int(prevRow[2])
                screen = int(prevRow[3])
                                
                totalData["Sleep"].append(time)
                totalData["Physical"].append(physical)
                totalData["Screen"].append(screen)
            else:
                prevRow = row
    print("Data read succesfully")
    hasLoaded = True
except:
    hasLoaded = False

#Graphs the time spent on screens active against time slept
def graph_screen():
    #Clears the screen of any previous graph
    plt.clf()
    
    x = np.array(totalData["Screen"])
    y = np.array(totalData["Sleep"])

    b, m = polyfit(x, y, 1)
        
    #Creates a scatter plot of the data
    plt.plot(x, y, '.')
    
    #Plots line of best fit on the same graph
    plt.plot(x, b + m * x, '-')
    
    #Labels the axes
    plt.xlabel("Screen Time")
    plt.ylabel("Time Slept")
            
    plt.show()

#Graphs the time spent physically active against time slept
def graph_phys():
    plt.clf()
    x = np.array(totalData["Physical"])
    y = np.array(totalData["Sleep"])
            
    b, m = polyfit(x, y, 1)
            
    plt.plot(x, y, '.')
    plt.plot(x, b + m * x, '-')
            
    plt.xlabel("Physical activity")
    plt.ylabel("Time Slept")
                
    plt.show()

#Graphs sleep over time
def graph_sleep():
    plt.clf()
    y = np.array(totalData["Sleep"])
    x = np.arange(1,len(y)+1,1,dtype=int)

    b, m = polyfit(x, y, 1)
            
    plt.plot(x, y, '.')
    plt.plot(x, y, '-')
            
    plt.xlabel("Time(Days)")
    plt.ylabel("Sleep(hours)")
                
    plt.show()

#Predicts sleep time given screen time and physical activity
def predict_sleep(screen,phys):
    x = np.array(totalData["Physical"])
    y = np.array(totalData["Sleep"])
    
    #Model which predicts time slept relative to screen time
    model1 = LinearRegression().fit(x.reshape(-1,1),y)
    #Prediction 1
    p1 = float(model1.predict([[phys]]))
    
    
    x = np.array(totalData["Screen"])
    
    #Model which predicts time slept relative to time spent physically active
    model2 = LinearRegression().fit(x.reshape(-1,1),y)
    #Prediction 2
    p2 = float(model2.predict([[screen]]))
    
    #Average of both predictions
    p_avg = (p1+p2)/2
    
    #Time slept cannot be less than zero so it is set 0 if the model predicts a negative value
    if(p_avg<0):
        p_avg = 0
    #Returns the predicted time slept
    return round(p_avg,2)

#Predicts screen time given time slept
def predict_screen(sleep):
    x = np.array(totalData["Sleep"])
    y = np.array(totalData["Screen"])
        
    model = LinearRegression().fit(x.reshape(-1,1),y)
        
    
    p = float(model.predict([[sleep]]))
    if(p<0):
        p = 0
    return round(p,2)

#Predicts time spent physically active given time slept
def predict_phys(sleep):
    x = np.array(totalData["Sleep"])
    y = np.array(totalData["Physical"])
        
    model = LinearRegression().fit(x.reshape(-1,1),y)
        
    p = float(model.predict([[sleep]]))
    if(p<0):
        p = 0
    return round(p,2)


while False:
    print("********************************************")
    print("**  Sleep Tracking Data Analysis          **")
    print("**                                        **")
    print("**  What do you want to know?             **")
    print("**  [Choose 1,2,3 or 4]                   **")
    print("**  (1) Graphs                            **")
    print("**  (2) Predict Sleep Time                **")
    print("**  (3) Predict Screen Time               **")
    print("**  (4) Predict Physical Activity         **")
    print("**  (5) Quit                              **")
    print("**                                        **")
    print("********************************************")
    
    choice = input()
    
    #Show graphs
    if(choice == "1"):
        print("**********************************************************")
        print("**  (1) Sleep in relation to screen time                **")
        print("**  (2) Graph of sleep in relation to physical activity **")
        print("**********************************************************")
        
        choice = input()
        if(choice == "1"):
            graph_screen()
        elif(choice == "2"):
            graph_phys()
        
    #Predict time slept given physical activity and screen time
    elif(choice == "2"):
        phys = float(input("Enter physical activity: "))
        
        screen = float(input("Enter Screen time: "))
        
        result = predict_sleep(phys,screen)
        print("Sleep time:",result,"hours")
        input()
    
    #Predict Screen time given time slept
    elif(choice=="3"):
        
        sleep = float(input("Enter time slept: "))
        result = predict_screen(sleep)
        
        print("Screen time:",result,"hours")
        input()
    #Predict physical activity given time slept
    elif(choice=="4"):
        sleep = float(input("Enter time slept: "))
        result = predict_phys(sleep)
        
        print("Physical activity:",result)
        
        input()
    #Exits the program
    elif(choice=="5"):
        break


