import tkinter as tk
from tkinter import ttk, messagebox
import mysql.connector
from mysql.connector import errorcode
from datetime import datetime
from math import ceil
from queries import select_city, select_cinema, select_movie, select_day, select_room, select_projection,\
                    select_reserved, add_booking, count_seats, select_seat_id

global cnx
global cursor
global choice_city
global choice_cinema_id
global choice_cinema
global choice_movie_id
global choice_movie
global choice_projection_id
global choice_day
global choice_room_id
global choice_projection_hour

global seats_in_row
seats_in_row = 15

class App(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self._frame = None
        self.switch_frame(LogWindow)   
        self.resizable(width = False, height = False)
        self.title('Cinema App')

    def switch_frame(self, frame_class):
        new_frame = frame_class(self)
        if self._frame is not None:
            self._frame.destroy()
        self._frame = new_frame
        self._frame.grid()

class LogWindow(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        def logging():
            try:   
                global cnx
                cnx = mysql.connector.connect(
                host = "localhost",
                user = username_str.get(),
                passwd = password_str.get(),
                database = "cinema_db",
                )
                global cursor
                cursor = cnx.cursor(buffered = True)
                master.switch_frame(ChooseCity)
            except mysql.connector.Error as err:
                if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                    tk.messagebox.showinfo('Wrong input', r'Wrong username and/or password')
                elif err.errno == errorcode.ER_BAD_DB_ERROR:
                    tk.messagebox.showinfo('Error', 'Database does not exist')
                else:
                    tk.messagebox.showinfo('Error', err)

        username_str = tk.StringVar()
        password_str = tk.StringVar()
        tk.Label(self, text = 'Username').grid(row = 1, column = 0, sticky = 'nsew', padx = 10)
        tk.Label(self, text = 'Password').grid(row = 2, column = 0, sticky = 'nsew', padx = 10)
        tk.Entry(self, width = 20, textvariable = username_str).grid(row = 1, column = 1, padx = 10, sticky = 'nsew')
        tk.Entry(self, show = '*', width = 5, textvariable = password_str).grid(row = 2, column = 1, padx = 10, sticky = 'nsew')
        tk.Button(self, text = 'Sign in', command = logging).grid(row = 3, column = 0, sticky = 'nsew', columnspan = 2)

class ChooseCity(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        def choose_city():
            selected = tree.focus()
            selected = tree.item(selected)
            global choice_city
            choice_city = selected['text']
            master.switch_frame(ChooseCinema)

        tk.Label(self, text = 'Choose city').grid(row = 0, column = 0)
        tree = tk.ttk.Treeview(self, show = 'tree') 
        tree.grid(row = 1, column = 0)
        tk.Button(self, text = 'Choose', command = choose_city).grid(row = 2, column = 0)
        cities = select_city(cnx, cursor)
        for i in cities:
            tree.insert('', 'end', text = i)      

class ChooseCinema(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        def choose_cinema():
            selected = tree.focus()
            selected = tree.item(selected)
            global choice_cinema
            global choice_cinema_id
            choice_cinema = selected['text']
            choice_cinema_id = id_key[cinemas.index(choice_cinema)]
            master.switch_frame(ChooseMovie)

        tk.Label(self, text = 'Choose cinema').grid(row = 0, column = 0, columnspan = 2)
        tree = tk.ttk.Treeview(self, show = "tree")
        tree.grid(row = 1, column = 0, columnspan = 2)
        records = select_cinema(cnx, cursor, city = choice_city)
        id_key = []
        cinemas = []
        for i in reversed(records):
            tree.insert('', 0, text = i[1])
            id_key.append(str(i[0]))
            cinemas.append(i[1])
        tk.Button(self, text = 'Back', command = lambda : master.switch_frame(ChooseCity)).grid(row = 2, column = 0, sticky = 'we')
        tk.Button(self, text = 'Choose', command = choose_cinema).grid(row = 2, column = 1, sticky = 'we')
        

class ChooseMovie(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        def choose_movie():
            selected = tree.focus()
            selected = tree.item(selected)
            global choice_movie
            global choice_movie_id
            choice_movie = selected['text']
            choice_movie_id = id_key[movies.index(choice_movie)]
            master.switch_frame(ChooseDay)

        tk.Label(self, text = 'Choose movie').grid(row = 0, column = 0, columnspan = 2)
        tree = tk.ttk.Treeview(self, show="tree")
        tree.grid(row = 1, column = 0, columnspan = 2)
        records = select_movie(cnx, cursor)
        id_key = []
        movies = []
        for i in reversed(records):
            tree.insert('', 'end', text = i[1])
            id_key.append(i[0])
            movies.append(i[1])
        tk.Button(self, text = 'Back', command = lambda : master.switch_frame(ChooseCinema)).grid(row = 2, column = 0, sticky = 'we')
        tk.Button(self, text = 'Choose', command = choose_movie).grid(row = 2, column = 1, sticky = 'we')

class ChooseDay(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        def choose_date():
            global choice_day
            choice_day = datetime(year_var.get(), month_var.get(), day_var.get())
            choice_day = str(choice_day)
            choice_day = choice_day[:10] + '%'
            master.switch_frame(ChooseProjection)

        tk.Label(self, text = 'Select date (dd-mm-yyyy):').grid(row = 0, column = 0, pady = 5, columnspan = 5, sticky = 'we')
        today = datetime.now()
        day_var = tk.IntVar(value = today.day)
        month_var = tk.IntVar(value = today.month)
        year_var = tk.IntVar(value = today.year)
        tk.Entry(self, width = 10, textvariable = day_var).grid(row = 1, column = 0, sticky = 'nsew')
        tk.Label(self, text = '-').grid(row = 1, column = 1)
        tk.Entry(self, width = 10, textvariable = month_var).grid(row = 1, column = 2, sticky = 'nsew')
        tk.Label(self, text = '-').grid(row = 1, column = 3)
        tk.Entry(self, width = 10, textvariable = year_var).grid(row = 1, column = 4, sticky = 'nsew')
        tk.Button(self, text = 'Back', command = lambda : master.switch_frame(ChooseMovie)).grid(row = 2, column = 0, columnspan = 2, sticky = 'we')
        tk.Button(self, text = 'Select', command = choose_date).grid(row = 2, column = 3, columnspan = 2, sticky = 'we')

class ChooseProjection(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        def choose_projection():
            selected = tree.focus()
            selected = tree.item(selected)
            global choice_projection_hour
            choice_projection_hour = selected['text']
            master.switch_frame(ChooseRoom)

        tk.Label(self, text = 'choose hour').grid(row = 0, column = 0, columnspan = 2)
        tree = tk.ttk.Treeview(self, show = "tree")
        tree.grid(row = 1, column = 0, columnspan = 2)
        hours = select_day(cnx, cursor, id_cinema = str(choice_cinema_id), id_movie = str(choice_movie_id), proj_date = str(choice_day))
        for i in hours:
            txt = ''.join(i)
            tree.insert('', 'end', text = txt)       
        tk.Button(self, text = 'Back', command = lambda : master.switch_frame(ChooseDay)).grid(row = 2, column = 0, sticky = 'nsew') 
        tk.Button(self, text = 'Select', command = choose_projection).grid(row = 2, column = 1, sticky = 'nsew')

class ChooseRoom(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        def choose_room():
            selected_room_id = tree.focus()
            selected_room_id = tree.item(selected_room_id)
            selected_room_id = selected_room_id['text']
            records = select_projection(cnx, cursor, id_cinema = choice_cinema_id, id_movie = choice_movie_id, proj_date = choice_projection_hour, room_number = selected_room_id)
            global choice_room_id
            choice_room_id = records[0]
            global choice_projection_id
            choice_projection_id = records[1]
            master.switch_frame(RoomWindow)
        tk.Label(self, text = 'Choose room').grid(row = 0, column = 0, columnspan = 2)
        tree = tk.ttk.Treeview(self, show = "tree")
        tree.grid(row = 1, column = 0, columnspan = 2)
        records = select_room(cnx, cursor, id_cinema = str(choice_cinema_id), id_movie = str(choice_movie_id), proj_date = str(choice_projection_hour))
        id_rooms = []
        room_numbers = []
        for i in records:
            id_rooms.append(i[0])
            room_numbers.append(i[1])
            txt = ''.join(str(i[1]))
            tree.insert('', 'end', text = txt)       
        tk.Button(self, text = 'Back', command = lambda : master.switch_frame(ChooseProjection)).grid(row = 2, column = 0, sticky = 'nsew') 
        tk.Button(self, text = 'Select', command = choose_room).grid(row = 2, column = 1, sticky = 'nsew')

class RoomWindow(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        def select_seat(x):
            if seat[x - 1]['bg'] == 'orange':
                seat[x - 1].config(bg = 'green')
                selected_seats.remove(int(seat[x - 1]['text']))
                return
            seat[x - 1].config(bg = 'orange')
            selected_seats.append(int(seat[x - 1]['text']))

        def book():
            for i in selected_seats:
                cur_place_id = select_seat_id(cnx, cursor, id_room = choice_room_id, place_number = i)
                add_booking(cnx, cursor, f_name = f_name_var.get(), l_name = l_name_var.get(), phone = str(phone_var.get()), id_place = cur_place_id, id_projection = choice_projection_id)
            master.switch_frame(RoomWindow)

        reserved = select_reserved(cnx, cursor, id_cinema = choice_cinema_id, id_projection = choice_projection_id)
        global seats_in_row 
        global choice_room_id
        left = count_seats(cnx, cursor, id_room = choice_room_id)
        rows = ceil(left/seats_in_row)
        tk.Label(self, bg = 'gray64', text = 'SCREEN').grid(row = 0, column = 1, columnspan = seats_in_row, ipady = 5, pady = 25, sticky = 'nsew')
        selected_seats = []
        seat = []
        for i in range(rows):
            for j in range(seats_in_row):
                curr_seat_number = i * seats_in_row + j + 1
                seat.append(tk.Button(self, bg = 'green', text = curr_seat_number))
                if curr_seat_number in reserved:
                    seat[-1].config(bg = 'orange red', disabledforeground = 'black', state = 'disabled')
                seat[-1].config(command = lambda x = int(seat[-1]['text']): select_seat(x))
                seat[-1].grid(row = 1 + i, column = 1 + j, padx = 1, pady = 3, sticky = 'nsew')
                self.grid_rowconfigure(1 + i, minsize = 40)
                self.grid_columnconfigure(1 + j, minsize = 40)
                left = left - 1
                if left == 0: break
        f_name_var = tk.StringVar()
        l_name_var = tk.StringVar(value = None)
        phone_var = tk.IntVar()
        tk.Button(self, text = 'Back', command = lambda : master.switch_frame(ChooseRoom)).grid(row = 0, column = 0, sticky = 'wn')
        tk.Label(self, text = 'Name', bg = 'powder blue').grid(row = 2, column = 0, ipady = 5, sticky = 's')
        tk.Entry(self, width = 20, textvariable = f_name_var).grid(row = 3, column = 0, ipady = 5, sticky = 'n')
        tk.Label(self, text = 'Surname', bg = 'powder blue').grid(row = 4, column = 0, ipady = 5, sticky = 's')
        tk.Entry(self, width = 20, textvariable = l_name_var).grid(row = 5, column = 0, ipady = 5, sticky = 'n')
        tk.Label(self, text = 'Phone', bg = 'powder blue').grid(row = 6, column = 0, ipady = 5, sticky = 's')
        tk.Entry(self, width = 20, textvariable = phone_var).grid(row = 7, column = 0, ipady = 5, sticky = 'n')     
        tk.Button(self, text = 'Add reservation', command = book).grid(row = 8, column = 0, ipady = 5, sticky = 'nsew')
        self.configure(bg = 'powder blue')

if __name__ == "__main__":
    app = App()
    app.mainloop()
