import tkinter as tk
from tkinter import ttk
import TrainCanvas
import CSVManager

class MainWin(tk.Tk):
    
    def __init__(self, line, station, daytype = "평일"):
        super().__init__()
        self.resizable(True, False)
        self.title(f'{line}호선 {daytype} - 대구 도시철도 열차 표시 프로그램')
        self.main_frame1 = tk.Frame(self, padx=2)
        self.main_frame2 = tk.Frame(self, padx=2)
        
        
        self.canvas1 = TrainCanvas.TrainCanvasClass(self.main_frame1, line, station, "상", daytype)
        self.canvas2 = TrainCanvas.TrainCanvasClass(self.main_frame2, line, station, "하", daytype)

        scrollbar1 = tk.Scrollbar(self.main_frame1, orient='horizontal')
        scrollbar2 = tk.Scrollbar(self.main_frame2, orient='horizontal')
        
        title_label = tk.Label(self, text=f'{line}호선 {daytype} 열차')
        label1 = tk.Label(self.main_frame1, text="상선")
        label2 = tk.Label(self.main_frame2, text="하선")

        sizegrip = ttk.Sizegrip(self.main_frame2)
        
        x1 = self.canvas1.bbox("all")[2] - self.canvas1.bbox("all")[0]
        y1 = self.canvas1.bbox("all")[3] - self.canvas1.bbox("all")[1]
        x2 = self.canvas2.bbox("all")[2] - self.canvas2.bbox("all")[0]
        y2 = self.canvas2.bbox("all")[3] - self.canvas2.bbox("all")[1]
        
        self.canvas1.config(scrollregion=self.canvas1.bbox("all"), xscrollcommand= scrollbar1.set)
        self.canvas2.config(scrollregion=self.canvas2.bbox("all"), xscrollcommand= scrollbar2.set)
        self.canvas1.config(height=y1)
        self.canvas2.config(height=y2)

        scrollbar1.config(command=self.canvas1.xview)
        scrollbar2.config(command=self.canvas2.xview)

        #self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)
        self.rowconfigure(2, weight=1)
        
        self.columnconfigure(0, weight=1)
        self.main_frame1.rowconfigure(0, weight=1)
        self.main_frame1.rowconfigure(1, weight=1)
        self.main_frame2.rowconfigure(0, weight=1)        
        self.main_frame2.rowconfigure(1, weight=1)
        self.main_frame1.columnconfigure(1, weight=1)
        self.main_frame2.columnconfigure(1, weight=1)

        self.main_frame1.grid(row=1, column=0, sticky="nswe")
        self.main_frame2.grid(row=2, column=0, sticky="nswe")

        self.canvas1.grid(row=1, column=1, sticky="nswe")
        self.canvas2.grid(row=1, column=1, sticky="nswe")

        scrollbar1.grid(row=2, column=1, sticky="we")
        scrollbar2.grid(row=2, column=1, sticky="we")

        title_label.grid(row=0, column=0)
        label1.grid(row=1, column=0, rowspan=1, sticky="we")
        label2.grid(row=1, column=2, rowspan=1, sticky="we")
        
        sizegrip.grid(row=2, column=2, sticky="se")

        self.update()
        
        canvas2_row, canvas2_col = self.canvas2.grid_info()['row'], self.canvas2.grid_info()['column']
        canvas2_length = self.main_frame2.grid_bbox(canvas2_row, canvas2_col)[2] - self.main_frame2.grid_bbox(canvas2_row, canvas2_col)[0]
        
        scrollval1 = (self.canvas1.get_station_dot_xpos() - self.canvas1.get_station_dot_distance())/x1
        scrollval2 = (self.canvas2.get_station_dot_xpos() - canvas2_length + self.canvas2.get_station_dot_distance() )/x2
        self.canvas1.xview_moveto(scrollval1)
        self.canvas2.xview_moveto(scrollval2)

class InputWindow(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("시작")
        self.draw_UI()
        

    def draw_UI(self):
        frame1 = tk.Frame(self, padx = 5, pady=5)

        label_title = tk.Label(frame1, text="대구 도시철도 열차 표시 프로그램\n\n\n설정", pady = 5)
        label1 = tk.Label(frame1, text="호선 선택:", padx = 5, pady=5)
        label2 = tk.Label(frame1, text="역 선택: ", padx = 5, pady=5)
        label3 = tk.Label(frame1, text="요일 선택: ", padx = 5, pady=5)

        self.var1=tk.IntVar()
        self.var2=tk.StringVar()
        self.var3=tk.StringVar()

        self.combobox1 = ttk.Combobox(frame1, state="readonly", textvariable = self.var1)
        self.combobox2 = ttk.Combobox(frame1, state="readonly", textvariable = self.var2)
        self.combobox3 = ttk.Combobox(frame1, state="readonly", textvariable = self.var3)

        button1 = tk.Button(frame1, text="실행", padx = 5, pady=5, command = lambda: launch_mainwin(self.var1.get(), self.var2.get(), self.var3.get()))
        button2 = tk.Button(frame1, text="닫기", padx = 5, pady=5, command= self.destroy)

        self.combobox1['values'] = [1, 2, 3]
        self.combobox1.set('호선을 선택하세요')
        self.combobox3['values'] = ["평일", "토요일", "휴일"]

        label_title.grid(row=0, column=0, columnspan=2, sticky= "nwse")
        label1.grid(row=1, column=0, sticky="w")
        label2.grid(row=2, column=0, sticky="w")
        label3.grid(row=3, column=0, sticky="w")

        self.combobox1.grid(row=1, column=1)
        self.combobox2.grid(row=2, column=1)
        self.combobox3.grid(row=3, column=1)
        button1.grid(row=4, column=0, columnspan=2 ,sticky="nwse")
        button2.grid(row=5, column=0, columnspan=2 ,sticky="nwse")

        self.combobox1.bind('<<ComboboxSelected>>', self.get_stations)
        
        
        frame1.pack()
        
    def get_stations(self, value):
        stationlist = CSVManager.CSVClass(self.var1.get()).get_station_list()
        
        self.combobox2['values'] = stationlist
        self.combobox2.set('')

def launch_mainwin(line, station, daytype):
    a = MainWin(line, station, daytype)
    a.mainloop()
    
    
test = InputWindow()
test.mainloop()
