import mysql.connector
import random
from datetime import datetime, date
import getpass

names = [
    'John',
    'Andy',
    'Victor',
    'George',
    'Jessica',
    'James',
    'Amelia',
    'Emily',
    'Jacob',
    'Michael',
    'Thomas',
    'Barbara',
    'Susan',
    'Mia'
]

surnames = [
    'Smith',
    'Wilson',
    'Taylor',
    'Brown',
    'Rodriguez',
    'Larkin',
    'Williams',
    'Lee',
    'White',
    'Kovalsky'
]

def add_cinema(_cnx, _cursor, *, city, address):
    '''Adds cinema to database.'''
    query = ('INSERT INTO cinema(city, address) VALUES (%s, %s)')
    values = (city, address)
    _cursor.execute(query, values)
    _cnx.commit()

def add_room(_cnx, _cursor, *, id_cinema, place_amount, room_number):
    '''Adds room to database.'''
    query = ('INSERT INTO room(id_cinema, place_amount, room_number) VALUES (%s, %s, %s)')
    values = (id_cinema, place_amount, room_number)
    _cursor.execute(query, values)
    _cnx.commit()

def add_movie(_cnx, _cursor, *, title, technology):
    '''Adds movie to database.'''
    query = ('INSERT INTO movie(title, technology) VALUES (%s, %s)')
    values = (title, technology)
    _cursor.execute(query, values)
    _cnx.commit()

def add_projection(_cnx, _cursor, *, proj_date, id_movie, id_room):
    '''Adds movie projection to database.'''
    query = ('INSERT INTO projection(proj_date, id_movie, id_room) VALUES (%s, %s, %s)')
    values = (proj_date, id_movie, id_room)
    _cursor.execute(query, values)
    _cnx.commit()

def is_phone_unique(_cnx, _cursor, ph_number):
    '''Returns 1 if specified phone number is unique within customer table, otherwise returns 0.'''
    _cursor.execute(('SELECT phone FROM customer'))
    phone = _cursor.fetchall()
    for i in phone:
        if i[0] == int(ph_number): return 0
    return 1

def add_random_customer(_cnx, _cursor, amount = 1):
    '''Adds specified number of random customers.'''
    for i in range(amount):
        nm = random.randint(0, len(names) - 1)
        snm = random.randint(0, len(surnames) - 1)
        ph = random.randint(100000000, 999999999)
        if _cursor.execute('SELECT COUNT(*) from customer') == 0:
            while not is_phone_unique(_cnx, _cursor, ph):
                ph = random.randint(100000000, 999999999)
        else:
            ph = random.randint(100000000, 999999999)
        query = ('INSERT INTO customer(f_name, l_name, phone) VALUES (%s, %s, %s)')
        values = (names[nm], surnames[snm], ph)
        _cursor.execute(query, values)
        _cnx.commit()

def add_booking(_cnx, _cursor, *, f_name, l_name, phone, id_place, id_projection):
    '''Adds single booking to database (with customer creation).'''
    query = ('CALL add_booking(%s, %s, %s, %s, %s)')
    values = (f_name, l_name, phone, id_place, id_projection)
    _cursor.execute(query, values)
    _cnx.commit()

def add_booking_single_statement(_cnx, _cursor, *, id_place, id_customer, id_projection):
    '''Inserts one booking into database.'''
    query = ('INSERT INTO booking(id_place, id_customer, id_projection) VALUES (%s, %s, %s)')
    values = (id_place, id_customer, id_projection)
    _cursor.execute(query, values)
    _cnx.commit()

def select_city(_cnx, _cursor):
    '''Returns list of cities.'''
    _cursor.execute('SELECT DISTINCT city FROM cinema ORDER BY city, address DESC')
    records = _cursor.fetchall()
    data = []
    for i in records:
        data.append(i[0])
    return data

def select_cinema(_cnx, _cursor, *, city):
    '''Returns list of tuples: (cinema.id, cinema.address) in specified city.'''
    query = ('SELECT id, address FROM cinema WHERE city = %s ORDER BY address DESC')
    values = (city,)
    _cursor.execute(query, values)
    return _cursor.fetchall()

def select_movie(_cnx, _cursor):
    '''Returns list of tuples: (movie.id, movie.title, movie.technology).'''
    _cursor.execute('SELECT id, title, technology FROM movie')
    return _cursor.fetchall()

def count_seats(_cnx, _cursor, *, id_room):
    '''Returns number of seats in specified room ID.'''
    query = ('SELECT COUNT(*) FROM place WHERE id_room = %s')
    values = (id_room,)
    _cursor.execute(query, values)
    record = _cursor.fetchall()
    return record[0][0]

def select_day(_cnx, _cursor, *, id_cinema, id_movie, proj_date):
    '''Returns list of projection hours from database.'''
    query = ('SELECT DISTINCT proj_date FROM projection INNER JOIN room ON room.id=id_room AND room.id_cinema = %s AND projection.id_movie = %s AND proj_date LIKE %s')
    values = (id_cinema, id_movie, proj_date)
    _cursor.execute(query, values)
    data = _cursor.fetchall()
    conv_date = []
    for i in data:
        conv_date.append(i[0].strftime('%Y-%m-%d %H:%M:%S'))
    return conv_date

def select_room(_cnx, _cursor, *, id_cinema, id_movie, proj_date):
    '''Returns list of tuples (room.id, room_number) from database.'''
    query = ('SELECT room.id, room_number FROM projection INNER JOIN room ON room.id=id_room AND room.id_cinema = %s AND projection.id_movie = %s AND proj_date = %s')
    values = (id_cinema, id_movie, proj_date)
    _cursor.execute(query, values)
    return _cursor.fetchall()

def select_projection(_cnx, _cursor, *, id_cinema, id_movie, proj_date, room_number):
    '''Returns list [room.id, projection.id] from database.'''
    query = ('SELECT room.id, projection.id FROM projection INNER JOIN room ON room.id=id_room AND room.id_cinema = %s AND projection.id_movie = %s AND proj_date = %s AND room.room_number = %s')
    values = (id_cinema, id_movie, proj_date, room_number)
    _cursor.execute(query, values)
    records = _cursor.fetchall()
    data = []
    data.append(records[0][0])
    data.append(records[0][1])
    return data

def select_reserved(_cnx, _cursor, *, id_cinema, id_projection):
    '''Returns list of reserved seats numbers from database.'''
    query = ('SELECT place.place_number FROM place INNER JOIN room ON room.id = place.id_room INNER JOIN cinema ON cinema.id = room.id_cinema and cinema.id = %s INNER JOIN projection ON room.id = projection.id_room and projection.id = %s RIGHT JOIN booking ON place.id=booking.id_place and projection.id=booking.id_projection')
    values = (id_cinema, id_projection)
    _cursor.execute(query, values)
    records = _cursor.fetchall()
    data = []
    for i in records:
        data.append(i[0])
    return data

def select_seat_id(_cnx, _cursor, *, id_room, place_number):
    '''Selects ID of seat from database indicated by id_room and place_number (returns single value)'''
    query = ('SELECT id FROM place WHERE id_room = %s AND place_number = %s')
    values = (id_room, place_number)
    _cursor.execute(query, values)
    record = _cursor.fetchall()
    return record[0][0]

if __name__ == "__main__":
    print('Before continuing make sure that cinema_db has no records - it can cause wrong input \n(please note that this project is in development)')
    input('Press any key to continue...')
    print('Type your MySQL root password (it is not shown in command prompt):')
    root_passwd = getpass.getpass()
    cnx = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd=root_passwd,
    database="cinema_db"
    )
    cursor = cnx.cursor(buffered = True)

    add_cinema(cnx, cursor, city = 'Warsaw', address = 'Random Street 42')
    add_cinema(cnx, cursor, city = 'Warsaw', address = 'Other Street 25')
    add_cinema(cnx, cursor, city = 'Cracow', address = 'Main Street 87')
    add_cinema(cnx, cursor, city = 'Cracow', address = 'Calm Street 123')

    cursor.execute('SELECT id from cinema')
    records = cursor.fetchall()
    cinemas = []
    for i in records:
        cinemas.append(i[0])

    for i in cinemas:
        for j in range(3):
            add_room(cnx, cursor, id_cinema = i, place_amount = 120, room_number = j + 1)
    
    add_movie(cnx, cursor, title = 'Pirates of the Baltic Sea', technology = '2D')
    add_movie(cnx, cursor, title = 'Lord of the Necklaces', technology = '2D')

    cursor.execute('SELECT title from movie')
    records = cursor.fetchall()
    movies = []
    for i in records:
        movies.append(i[0])

    cursor.execute('SELECT id from room')
    records = cursor.fetchall()
    rooms = []
    for i in records:
        rooms.append(i[0])

    today = str(date.today())
    for i in rooms:
        for j in range(2):
            hour = random.randint(8 + 6 * j, 12 + 6 * j)
            if hour >= 10:
                proj_hour = ''.join(today) + ' ' + str(hour) + ':00:00'
            else:
                proj_hour = ''.join(today) + ' 0' + str(hour) + ':00:00'
            add_projection(cnx, cursor, proj_date = proj_hour, id_movie = j + 1, id_room = i)
    add_random_customer(cnx, cursor, amount = 120)

    cursor.execute('SELECT id from customer')
    records = cursor.fetchall()
    customers = []
    for i in records:
        customers.append(i[0])
    customers.sort()

    cursor.execute('SELECT id from place')
    records = cursor.fetchall()
    seats = []
    for i in records:
        seats.append(i[0])
    seats.sort()

    cursor.execute('SELECT id from projection')
    records = cursor.fetchall()
    projections = []
    for i in records:
        projections.append(i[0])
    projections.sort()

    id_seat_low_limit = 0
    iteration = 0
    for i in projections:
        tmp_id_seat = []
        for j in range(5):
            id_seat = random.randint(id_seat_low_limit + 1, id_seat_low_limit + 120)
            while id_seat in tmp_id_seat:
                id_seat = random.randint(id_seat_low_limit + 1, id_seat_low_limit + 120)
            tmp_id_seat.append(id_seat)
            cursor.execute('INSERT INTO booking(id_place, id_customer, id_projection) VALUES (%s, %s, %s)', (tmp_id_seat[j], customers[iteration], i))
            iteration += 1       
        if iteration % 10 == 0:
            id_seat_low_limit += 120
    print('Data should be inserted. If it is not, type "DROP DATABASE cinema_db;" in MySQL, run cinema_database.sql script and try again to run queries.py')
    input('Press any key to continue...')
    cnx.commit()  
    cursor.close()
    cnx.close()