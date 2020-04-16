## Cinema booking database with GUI

This project consists of database (using MySQL) that stores information about bookings in cinemas and GUI (made with Python) that allows to manage reservations.

![booking_printscreen](/images/8_booking_window.PNG)

__Please note that this project is still in development and that is why it is not fully wrong-user-input-prone and code needs to be refactorized.__

Database EER diagram:

![EER diagram](/images/EER_diagram.PNG)

### Table of contents

1. Requirements.
2. Installation guide.
3. Sample usage.

### Requirements

- Python3
- MySQL Server 8.0
- MySQL Connector/Python 8.0
- MySQL Workbench and MySQL Notifier (not necessary but recommended)

### Installation guide

1. Make sure that MySQL80 service is on (you can check this easily via MySQL Notifier or find it in Services)
2. Open MySQL Workbench and click file --> Open SQL Script --> browse cinema_database.sql and execute it - now database is created (if you do not have Workbench you can do this in command prompt too).
3. Run queries.py as script (it fills database with some random data).
4. Run CinemaBookingApp.pyw.

### Sample Usage

Firstly you need to log in MySQL as user (default username is 'root'):

![Log window](/images/1_log_window.PNG)

Then choose city:

![Choose city window](/images/2_choose_city.PNG)

Now choose cinema:

![Choose cinema window](/images/3_choose_cinema.PNG)

Choose movie:

![Choose movie window](/images/4_choose_movie.PNG)

Select day (query.py inserts projections in today's date, so choose current date - otherwise you will see no positions in next window):

![Choose day window](/images/5_choose_day.PNG)

Select projection hour:

![Choose hour window](/images/6_choose_hour.PNG)

Choose room:

![Choose room window](/images/7_choose_room.PNG)

And finally you can add booking (red seats - reserved, green - free, orange - selected):

![Booking window](/images/8_booking_window.PNG)
