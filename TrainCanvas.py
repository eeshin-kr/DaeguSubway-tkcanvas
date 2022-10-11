import tkinter as tk
import CSVManager
import time

class TrainCanvasClass(tk.Canvas):

    def __init__(self, master, target_line, target_station, target_direction ,target_daytype):
        super().__init__(master)
        self.tkmaster = master
        self.width = master.winfo_screenwidth()
        self.height = 250
        self.line = target_line
        self.station = target_station
        self.direction = target_direction
        self.daytype = target_daytype
        self.init_var()
        self.draw_window()
        self.draw_dots()
        self.draw_line()
        self.update_trains()
        self.draw_train_body()

    def init_var(self):
        self.csv_class = CSVManager.CSVClass(self.line)
        self.station_list = self.csv_class.get_station_list()
        self.csv_train_class_1 = self.CSVWorkingTrainClass(daytype=self.daytype, direction=self.direction, line=self.line)
        #self.csv_train_class_2 = self.CSVWorkingTrainClass(daytype=self.daytype, direction="하", line=self.line)
        self.train_body_dict={}
        
    def draw_line(self):
        fig_line = self.create_line(0, self.height/2, self.width, self.height/2)

    def draw_window(self):
        self.pack(fill=tk.X)

    def draw_dots(self):
        pos_y_line = self.height / 2
        margin_left_px = 60 #맨 왼쪽 점의 왼쪽 여백 설정
        margin_right_px = 60 #맨 오른쪽 점의 오른쪽 여백 설정
        diameter_px_dot = 10 #점의 지름 설정
        number_of_dots = len(self.station_list)
        margin_distance_dots = (self.width - (margin_left_px + margin_right_px)) // (number_of_dots - 1) #원 지름은 고려하지 않음

        #margin_right_dots_px = 70 #각 점의 오른쪽 간격 설정
        #number_of_dots = ( self.width - (margin_left_px + margin_right_px) ) // (margin_right_dots_px + diameter_px_dot)
        #number_of_dots = int(number_of_dots)
        #if number_of_dots > len(self.station_list) - self.station_list.index(self.station):
        #    number_of_dots = len(self.station_list) - self.station_list.index(self.station)

        #dot_pos_x_list = [margin_left_px + diameter_px_dot / 2]
        #for tmp in range(1, number_of_dots):
        #    pos_x = dot_pos_x_list[-1] + (diameter_px_dot / 2 + margin_right_dots_px + diameter_px_dot / 2)
        #    dot_pos_x_list.append(pos_x)
        #dot_pos_x_list = [margin_left_px + diameter_px_dot / 2]
        dot_pos_x_list = [margin_left_px]
        for tmp in range(1, number_of_dots):
            pos_x = dot_pos_x_list[-1] + margin_distance_dots
            dot_pos_x_list.append(pos_x)

        self.dots_list = []
        for pos_x_dots in dot_pos_x_list:
            self.dots_list.append( self.StationDotClass(self, pos_x_dots, pos_y_line, diameter_px_dot) )

        self.highlight_dot = self.StationDotClass(self, dot_pos_x_list[self.station_list.index(self.station)], self.height/2, diameter_px_dot*1.5, "Green")

        self.dot_pos_x_list = dot_pos_x_list
        self.draw_dots_captions()

    def draw_dots_captions(self):
        self.station_current_list=[]
        for tmp in range(len(self.dots_list)):
            #self.station_current_list.append(self.station_list[self.station_list.index(self.station) + tmp])
            self.station_current_list.append(self.station_list[tmp])
            self.dots_list[tmp].set_caption(self.station_current_list[tmp])

    def update_trains(self):
        self.csv_train_class_1.refresh()
        next_time_launch_str = self.csv_train_class_1.get_next_train_update_time()
        next_time_launch_sec = get_time_diff_from_now(next_time_launch_str)
        #print(next_time_launch_sec)
        self.after(next_time_launch_sec * 1000, self.update_trains)
        
        
    def draw_train_body(self):
        # 차량 도형 생성 또는 이동
        testvar = self.csv_train_class_1.get_working_train_info_dict()
        #testvar2 = []
        
        for (key, val) in testvar.items():
            #if val["destination"] in self.station_current_list:
            #testvar2.append(key)
            tmpindex = self.station_current_list.index(val["destination"])
            tmp_pos_x_distance = self.dot_pos_x_list[1] - self.dot_pos_x_list[0]
            if self.direction == "상":
                tmplocation = self.dot_pos_x_list[tmpindex] + (tmp_pos_x_distance) * (1 - val["percentage"])
            elif self.direction == "하":
                tmplocation = self.dot_pos_x_list[tmpindex] - (tmp_pos_x_distance) * (1 - val["percentage"])
            if key not in self.train_body_dict.keys():
                self.train_body_dict[key] = self.TrainBodyClass(self, key, self.direction)
            self.train_body_dict[key].moveto_coords(tmplocation)


        for key in list(self.train_body_dict.keys()):
            if key not in testvar.keys() :
                self.train_body_dict[key].remove_body()
                del self.train_body_dict[key]
        
        self.after(2000, self.draw_train_body)

    def get_station_dot_xpos(self):
        station_xpos = self.dot_pos_x_list[self.station_list.index(self.station)]
        return station_xpos

    def get_station_dot_distance(self):
        return self.dot_pos_x_list[1] - self.dot_pos_x_list[0]


    class StationDotClass:
        def __init__(self, master, pos_x, pos_y ,diameter_px, color = "white"):
            self.tkmaster = master
            self.caption = None
            self.pos_x = pos_x
            self.pos_y = pos_y

            pos_x1 = pos_x - diameter_px / 2
            pos_x2 = pos_x + diameter_px / 2
            pos_y1 = pos_y - diameter_px / 2
            pos_y2 = pos_y + diameter_px / 2
            self.dot = master.create_oval(pos_x1, pos_y1, pos_x2, pos_y2, fill=color)

        def set_color(self, color):
            self.tkmaster.itemconfig(self.dot, fill=color)

        def set_caption(self, txt):
            if self.caption != None :
                self.tkmaster.delete(self.caption)
            pos_caption = self.pos_y + 20
            self.caption = self.tkmaster.create_text(self.pos_x, pos_caption, text = txt)

    class TrainBodyClass:
        def __init__(self, master, train_number, direction):
            self.tkmaster = master
            self.train_number = train_number
            self.train_direction = direction
            self.draw_body()


        def calculate_coords(self, pos_x):
            body_width = 40
            body_height = 20

            x_center = pos_x
            y_center = self.tkmaster.height/2 - body_height/2
            if self.train_direction == "상":                    
                x1 = x_center - body_width/2
                x2 = x_center + body_width/2
                x3 = x2
                x4 = x_center - body_width/4
                

            elif self.train_direction == "하":
                x1 = x_center - body_width/2
                x2 = x_center + body_width/2
                x3 = x_center + body_width/4
                x4 = x1

            y1 = y_center + body_height/2
            y2 = y1
            y3 = y_center - body_height/2
            y4 = y3

            tmpdict = {}
            tmpdict["coords_train"] = [x1, y1, x2, y2, x3, y3, x4, y4]
            tmpdict["coords_train_number"] = [x_center, y_center]

            return tmpdict


        def draw_body(self):
            default_pos_x = 20
            tmpdict = self.calculate_coords(default_pos_x)
            coords_train = tmpdict["coords_train"]
            coords_train_number = tmpdict["coords_train_number"]

            self.train = self.tkmaster.create_polygon(coords_train, fill="white", outline="black")
            self.train_number_text = self.tkmaster.create_text(coords_train_number, text = self.train_number)

        def moveto_coords(self, pos_x):
            tmpdict = self.calculate_coords(pos_x)
            coords_train = tmpdict["coords_train"]
            coords_train_number_text = tmpdict["coords_train_number"]
            
            self.tkmaster.coords(self.train, coords_train)
            self.tkmaster.coords(self.train_number_text, coords_train_number_text)

        def remove_body(self):
            self.tkmaster.delete(self.train)
            self.tkmaster.delete(self.train_number_text)
            

    class CSVWorkingTrainClass:

        def __init__(self, daytype, direction, line):
            self.daytype = daytype
            self.direction = direction
            self.line = line
            self.set_line(daytype, direction, line)
            
        def set_line(self, daytype, direction, line):
            self.csv_class = CSVManager.CSVClass(line)
            self.station_list = self.csv_class.get_station_list()
            self.traindict_arrive = self.csv_class.get_train_dict(daytype, direction, AdType="도착")
            self.traindict_departure = self.csv_class.get_train_dict(daytype, direction, AdType="출발")

        def refresh(self): #운행중인 열차 파악
            self.current_working_train_dict = self.filter_working_train_dict(self.traindict_arrive, self.direction)

        def get_next_train_update_time(self): #다음 열차의 첫 출발 시각 계산
            train_number_list = [train_number for train_number in self.traindict_arrive.keys()]
            if not list(self.current_working_train_dict.keys()) : #이번 열차가 없는 경우
                current_max_train_number = 0
            else:                
                current_max_train_number = max(list(self.current_working_train_dict.keys()))
                
            fillterd_train_number_list = [train_number for train_number in train_number_list if train_number >  current_max_train_number]
            if not fillterd_train_number_list : #다음 열차가 없을 경우
                fillterd_train_number_list = train_number_list
                
            next_train_number = min(fillterd_train_number_list)

            new_list = [time for time in self.traindict_departure[next_train_number] if time != None]
            new_list2 = list(map(timestr_to_sec, new_list))
            
            if self.direction == "상":
                first_time = new_list[-1]

            elif self.direction == "하":
                first_time = new_list[0]
            
            return first_time
            

        def filter_working_train_dict(self, traindict, direction):
            working_train = {}
            now_time_int = timestr_to_sec(time.strftime("%H:%M:%S"))
            for (key, val) in traindict.items(): #운행중인 열차 번호 파악

                new_list = [time for time in val if time != None]
                new_list2 = list(map(timestr_to_sec, new_list))

                if direction == "상":
                    first_time_int = new_list2[-1]
                    last_time_int = new_list2[0]

                elif direction =="하":
                    first_time_int = new_list2[0]
                    last_time_int = new_list2[-1]

                if last_time_int < first_time_int : #마지막 차가 24:00:00을 넘어갈 경우를 고려
                    if now_time_int < last_time_int : #현재 시각이 24:00:00을 넘어갈 경우 24:00:00만큼 막차 전 시간 까지 더해 줌
                        now_time_int = now_time_int + timestr_to_sec("24:00:00")
                    last_time_int = last_time_int + timestr_to_sec("24:00:00")
                
                if first_time_int > now_time_int : #출발을 안 한 차량
                    continue
                if last_time_int < now_time_int : #이미 종점을 지난 차량
                    continue

                tmpdict={"station_time_arrive_list": val,
                         "station_time_arrive_int_list": new_list2,
                         "station_time_departure_list": self.traindict_departure[key],
                         "first_time_int": first_time_int,
                         "last_time_int": last_time_int,
                         "is_last_time_over_24h": last_time_int > timestr_to_sec("24:00:00")}
                
                working_train[key] = tmpdict #dict 형태에 대입
            return working_train


        def get_working_train_info_dict(self):
            now_time_int = timestr_to_sec(time.strftime("%H:%M:%S"))
            working_train_destination_dict={}
            for (key, val) in self.current_working_train_dict.items(): #운행중인 열차의 위치 파악, 어느 역, 몇 분 남았는지 확인
                #마지막 차가 24:00:00을 넘어갈 경우를 고려
                if val["is_last_time_over_24h"] == True:
                    if now_time_int + timestr_to_sec("24:00:00") <= val["last_time_int"] :
                        now_time_int = now_time_int + timestr_to_sec("24:00:00")
                
                if self.direction == "상":
                    station_time_list = val["station_time_arrive_list"][::-1]
                    station_time_list2 = val["station_time_departure_list"][::-1]
                elif self.direction == "하":
                    station_time_list = val["station_time_arrive_list"]
                    station_time_list2 = val["station_time_departure_list"]
                    
                station_time_list3 = list(zip(station_time_list, station_time_list2))

                for arrive_time, departure_time in station_time_list3 :
                    if arrive_time == None:
                        continue
                    arrive_time_int = timestr_to_sec(arrive_time)
                    departure_time_int = timestr_to_sec(departure_time)
                    
                    if arrive_time_int < val["first_time_int"]:
                        arrive_time_int = arrive_time_int + timestr_to_sec("24:00:00")

                    if departure_time_int < val["first_time_int"]:
                        departure_time_int = departure_time_int + timestr_to_sec("24:00:00")

                    if departure_time_int < now_time_int :
                        previous_station_destination_departure_time_int = timestr_to_sec(departure_time)
                        continue

                    if departure_time_int >= now_time_int and arrive_time_int <= now_time_int :
                        previous_station_destination_departure_time_int = timestr_to_sec(departure_time)
                        next_station_destination_departure_time_int = arrive_time_int
                        percentage = 1
                        working_train_destination_dict[key]= {"destination": self.station_list[val["station_time_departure_list"].index(departure_time)],
                                                              "destination_time": departure_time,
                                                              "percentage": percentage,
                                                              "status": "대기"}
                        break
                    
                    if arrive_time_int > now_time_int:
                        next_station_destination_arrive_time_int = arrive_time_int
                        time_left = next_station_destination_arrive_time_int - now_time_int
                        time_duration = next_station_destination_arrive_time_int - previous_station_destination_departure_time_int
                        percentage = 1 - (time_left / time_duration)
                        working_train_destination_dict[key]= {"destination": self.station_list[val["station_time_arrive_list"].index(arrive_time)],
                                                              "destination_time": arrive_time,
                                                              "percentage": percentage,
                                                              "status": "출발"}
                        break

            return working_train_destination_dict    

def timestr_to_sec(TStr):
    tmp_array = TStr.split(':')
    tmp_list = list(map(int,tmp_array))
    tmp_int = tmp_list[0] * 3600 + tmp_list[1] * 60 + tmp_list[2]
    return tmp_int

def get_time_diff_from_now(TimeStr):
    time_now_int = timestr_to_sec(time.strftime("%H:%M:%S"))
    time_destination_int = timestr_to_sec(TimeStr)
    if time_now_int > time_destination_int:
        return 24*3600 - time_now_int + time_destination_int
    else:
        return time_destination_int - time_now_int


##master = tk.Tk()
##
##a = MyCanvas(master, 2, "대실", "하" ,"휴일")
##
##master.mainloop()
##
