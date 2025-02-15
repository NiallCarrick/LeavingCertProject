import analysis
import customtkinter as ctk
from customtkinter import filedialog
import shutil
from importlib import reload

class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        #Sets scaling of the GUI
        ctk.set_widget_scaling(2)  # widget dimensions and text size
        ctk.set_window_scaling(2)  # window geometry dimensions
        
        #Sets the colour scheme and appearance of the interface
        ctk.set_appearance_mode("dark")  # Modes: system (default), light, dark
        ctk.set_default_color_theme("blue")  # Themes: blue (default), dark-blue, green
        
        #Sets the size of the window
        self.geometry("300x400")
        self.minsize(width=300,height=400)
        #Sets the title of the window
        self.title("Sleep Analysis")
        
        #Checks if data is already read in and if then the open csv window needs to be shown
        if(analysis.hasLoaded == False):
            self.header = ctk.CTkLabel(master=self, text="Sleep Analysis",fg_color="transparent")
            self.header.cget("font").configure(size=25)
            self.header.place(relx=0.5,rely=0.05,anchor=ctk.N)
            
            self.csvLabel = ctk.CTkLabel(master=self,text="Please open csv file",fg_color="transparent")
            self.csvLabel.place(relx=0.5,rely=0.4,anchor=ctk.N)
            
            self.csvButton = ctk.CTkButton(master=self,text="Open CSV",command=self.open_csv)
            self.csvButton.place(relx=0.5,rely=0.5,anchor=ctk.N)
        else:
            self.mainScreen()

    def open_csv(self):
        csv = filedialog.askopenfilename()
        shutil.copy(csv, 'microbit.csv')
        
        if(analysis.hasLoaded == False):
            self.csvLabel.place(relx=500,rely=500,anchor=ctk.N)
            self.csvLabel.configure(text="")
            self.csvButton.place(relx=100000,rely=0.5,anchor=ctk.N)
            self.mainScreen()
        reload(analysis)
         

    def prediction_option(self,choice):
        if(choice == "Sleep time"):
            self.inputlabel2.place(relx=0.5,rely=0.55,anchor=ctk.N)
            self.entry2.place(relx=0.5,rely=0.6,anchor=ctk.N)
            
            self.inputlabel.configure(text="Enter screen time(hours):")
        elif(choice == "Screen time"):
            self.entry2.place(relx=10,rely=0.65,anchor=ctk.N)
            self.inputlabel2.place(relx=1000,rely=10000,anchor=ctk.N)
            
            self.inputlabel.configure(text="Enter time slept(hours):")
        elif(choice == "Physical activity"):
            self.entry2.place(relx=10,rely=0.65,anchor=ctk.N)
            self.inputlabel2.place(relx=10000,rely=10000,anchor=ctk.N)
            
            self.inputlabel.configure(text="Enter time slept(hours):")

    def graphmenu_callback(self,choice):
        if(choice == "Sleep in relation to screen time"):
            #Outputs graph of sleep over screen time
            analysis.graph_screen()
        elif(choice == "Sleep in relation to physical activity"):
            #Outputs graph of sleep over time spent physically active
            analysis.graph_phys()
        elif(choice == "Sleep over time"):
            #Outputs graph of sleep over time
            analysis.graph_sleep()

    def predict(self):
        option = self.segButton.get()
        if(option == "Sleep time"):
            result=str(analysis.predict_sleep(float(self.entry1.get()),float(self.entry2.get())))
            output = "Predicted time slept: "+result+"(hours)"
            self.resultLabel.configure(text=output)
        elif(option == "Screen time"):
            result=str(analysis.predict_screen(float(self.entry1.get())))
            output = "Predicted screen time: "+result+"(hours)"
            self.resultLabel.configure(text=output)
        elif(option == "Physical activity"):
            result=str(analysis.predict_phys(float(self.entry1.get())))
            output = "Predicted physical activity: "+result+"(hours)"
            self.resultLabel.configure(text=output)

    def mainScreen(self):
        self.header = ctk.CTkLabel(master=self, text="Sleep Analysis",fg_color="transparent")
        self.header.cget("font").configure(size=25)
        self.header.place(relx=0.5,rely=0.05,anchor=ctk.N)
        
        self.graphlabel = ctk.CTkLabel(master=self, text="Graphs",fg_color="transparent")
        self.graphlabel.place(relx=0.5,rely=0.125,anchor=ctk.N)

        self.graphmenu_var = ctk.StringVar(value="Graphs")
        self.graphmenu = ctk.CTkOptionMenu(self,values=[
                                                   "Sleep in relation to screen time",
                                                   "Sleep in relation to physical activity",
                                                   "Sleep over time"],
                                                 command=self.graphmenu_callback,
                                                 variable=self.graphmenu_var)
        self.graphmenu.place(relx=0.5,rely=0.175,anchor=ctk.N)


        self.predictlabel = ctk.CTkLabel(master=self, text="Predictions",fg_color="transparent")
        self.predictlabel.place(relx=0.5,rely=0.25,anchor=ctk.N)

        self.segButton = ctk.CTkSegmentedButton(master=self,
                                        values=["Sleep time",
                                                "Screen time",
                                                "Physical activity"],
                                        command=self.prediction_option)
        self.segButton.set("Sleep time")
        self.segButton.place(relx=0.5, rely=0.30, anchor=ctk.N)


        self.inputlabel = ctk.CTkLabel(master=self, text="Enter screen time(hours):",fg_color="transparent")
        self.inputlabel.place(relx=0.5,rely=0.4,anchor=ctk.N)

        self.entry1 = ctk.CTkEntry(self)
        self.entry1.place(relx=0.5,rely=0.45,anchor=ctk.N)

        self.inputlabel2 = ctk.CTkLabel(master=self, text="Enter amount of physical activity(hours):",fg_color="transparent")
        self.inputlabel2.place(relx=0.5,rely=0.55,anchor=ctk.N)

        self.entry2 = ctk.CTkEntry(self)
        self.entry2.place(relx=0.5,rely=0.6,anchor=ctk.N)


        self.resultButton = ctk.CTkButton(self,text="Submit",command=self.predict)
        self.resultButton.place(relx=0.5,rely=0.7,anchor=ctk.N)

        self.resultLabel = ctk.CTkLabel(master=self, text="",fg_color="transparent")
        self.resultLabel.place(relx=0.5,rely=0.8,anchor=ctk.N)
        
        self.resultLabel.cget("font").configure(size=15)
        
        self.csvButton = ctk.CTkButton(master=self,text="Open CSV",command=self.open_csv)
        self.csvButton.place(relx=0.5,rely=0.9,anchor=ctk.N)


if __name__ == "__main__":
    app = App()
    app.mainloop()