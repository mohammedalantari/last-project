import hashlib
import sqlite3
import os
#this class is for database management
class Database:
    def __init__(self):
        self.conn = sqlite3.connect('airline_booking.db')
        self.cursor = self.conn.cursor()

    def create_table(self):
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS bookings (
                booking_ref TEXT PRIMARY KEY,
                passport TEXT,
                first_name TEXT,
                last_name TEXT,
                seat TEXT
            )
        ''')
        self.conn.commit()

    #storing booking data in db
    def insert_booking(self, booking_ref, passport, first_name, last_name, seat):
        self.cursor.execute('''
            INSERT INTO bookings (booking_ref, passport, first_name, last_name, seat)
            VALUES (?, ?, ?, ?, ?)
        ''', (booking_ref, passport, first_name, last_name, seat))
        self.conn.commit()

    #deleting a booking from db
    def delete_booking(self, booking_ref):
        self.cursor.execute('DELETE FROM bookings WHERE booking_ref = ?', (booking_ref,))
        self.conn.commit()

    #the additional feature that is added is search by booking ID and passport, if a passenger has booked a seat, he can search his
    #seat by his booking ID and passport, ths feature in available in practical airline booking systems
    def search_booking(self, search_term):
        self.cursor.execute('''
            SELECT first_name, last_name, seat FROM bookings WHERE booking_ref = ? OR passport = ?
        ''', (search_term, search_term))
        results = self.cursor.fetchall()
        if results:
            passenger_name = f"{results[0][0]} {results[0][1]}"
            seats = [f"{row[2]}" for row in results]
            return passenger_name, seats
        else:
            return None, None

    def close(self):
        self.conn.close()
        os.remove('airline_booking.db')


class AirlineBookingSystem:
    def __init__(self):
        self.seats = [] #initializing an empty list for the sitting plan
        self.status =[] #this list will store status of each seat (i.e. booked/free)
        self.db = Database()  # Initialize the database
        self.db.create_table()

        #this function will initialize the two lists one for sitting plan and other for the status of each seat
    def init(self):
        rows = ["A", "B", "C", "X","D", "E", "F"] # sets are categorized into these five sections
        # each section has 80 seats
        for row in rows:
            for num in range(1, 81):
                seat = f"{num}{row}"
                self.seats.append(seat)
                self.status.append("F")  # Initially as seats are free so status is "F"
        # Aisle seats (after C section)
        for i in range(240, 320):
            self.seats[i] = "X"  # Aisle seats marked as "X"
            self.status[i] = " "
        # Storage area is indicated as "S"
        storage_indexes = [396, 397, 476, 477,556,557]  # (77D,78D,77E,78E,77F,78F)
        for i in storage_indexes:
            self.seats[i] = "S"
            self.status[i] = " "

    #this function will be used to update the status list at the time of booking and freeing a seat
    def update (self,index,value):
        self.status[index] = value

    #the ID is generated by concatenating the passport and first and last name of the passenger
    #then it is encrypted using SHA-1 hash and lastly the value is trimmed to 8 figures, the fourth
    #parameter serves the purpose of generating unique ID for multiple booking of same user, the
    #default value of index is zero, it increments as bookings of same passenger increase, it works
    #by first getting details of all previous bookings and then counting the bookings this count will
    #server as a unique identifier for generating ids, thus each ID will be different.

    def generate_booking_ref(self, passport, first_name, last_name,index):
        passenger_info = passport + first_name + last_name + str(index)
        sha1_hash = hashlib.sha1(passenger_info.encode()).hexdigest()
        return sha1_hash[:8]

    # this function will print all the sitting plan
    def ShowBookingStatus(self):
        for i in range(len(self.seats)):
            if (i in range(240,320) or self.seats[i] == "S"): # for aisle and storage seats, there is no status to be printed
                print(f"[   {self.seats[i]}   ]", end="  ")
            else:
                print(f"[{self.seats[i]} : {self.status[i]}]", end="  ") #for passenger seats
            if (i + 1) % 80 == 0:
                print() # Newline after every 80 seats
                if (i+1)==240 or (i+1)==320: # extra newline before and after aisle
                    print()

    #this function will print all the seats available in a row
    def CheckAvailability(self):
        available_seats = [self.seats[i] for i in range(len(self.seats)) if self.status[i] == "F"]
        if available_seats:
            print("Available Seats: " + ", ".join(available_seats))
        else:
            print("No available seats left.")

    #this function will provide the functionality of booking a seat
    def BookSeats(self):
        self.CheckAvailability()
        while True:
            seat_name = input("Enter seat number or type '-1' to quit: ").strip()
            if seat_name.lower() == "-1":
                print("Exiting booking system...")
                break
            if seat_name not in self.seats: #invalid input
                print("Invalid seat name. Please enter a valid seat from the list.")
                continue
            index = self.seats.index(seat_name)
            if self.seats[index] == "X": #check fir isles area
                print(f" Seat {seat_name} is in the aisle area and cannot be booked.")
                continue
            elif self.seats[index] == "S": #check for storage area
                print(f"Seat {seat_name} is in the storage area and cannot be booked.")
                continue
            elif self.status[index] == "R": #check for already booked seats
                print(f"Seat {seat_name} is already booked. Please choose another seat.")
                continue

            # Get passenger details
            passport = input("Enter passport number: ").strip()
            first_name = input("Enter first name: ").strip()
            last_name = input("Enter last name: ").strip()
            existing_booking,seats = self.db.search_booking(passport)
            if existing_booking : #if same user has already booked a seat
                booking_index = len(seats) #then make new booking unique by first getting details of all previous bookings and then counting the bookings
                #this count will server as a unique identifier for generating ids, thus each ID will be different
                booking_ref = self.generate_booking_ref(passport, first_name, last_name, booking_index)
            else:
                booking_ref = self.generate_booking_ref(passport, first_name, last_name, 0) #deafult vaule of index is 0
            self.db.insert_booking(booking_ref, passport, first_name, last_name, seat_name) #updating db
            self.update(index, booking_ref) #updating status
            print(f"Seat {seat_name} booked successfully with reference {booking_ref}")

        self.CheckAvailability()

    #this function will provide functionality of freeing a seat
    def FreeSeat(self):
        seat_name = input("Enter seat number to free: ").strip()
        if seat_name not in self.seats: #inavlid input
            print("Invalid seat name. Please enter a valid seat.")
            return
        index = self.seats.index(seat_name)  # Find the seat index
        if self.status[index] == "R":
            booking_ref = self.status[index]
            self.db.delete_booking(booking_ref) #updating db
            self.update(index, "F")  # Mark the seat as free
            print(f"Seat {seat_name} is now free!")
        else: #if user selects a seat which is not booked
            print(f"Seat {seat_name} is not booked, so it cannot be freed.")

        self.ShowBookingStatus()  # Display the updated seat status

    #this function will provide the functionality to search booking by booking reference or passport
    def PassengerSearch(self):
        search_term = input("Enter booking reference or passport number: ").strip()
        passenger_name, seats = self.db.search_booking(search_term)
        if passenger_name:
            print(f"Passenger: {passenger_name}")
            print(f"Seats: {', '.join(seats)}")
        else:
            print("No booking found for the given reference/passport number.")

    # main entry of the program
    def menu(self):
        self.init()  # Initialize seats and status
        while True:
            # Display menu options
            print("\n--- Seat Booking System ---")
            print("1. Check availability of seat")
            print("2. Book a seat")
            print("3. Free a seat")
            print("4. Show booking status")
            print("5. Search Booking")
            print("6. Exit program")
            choice = input("Enter your choice (1-5): ").strip()
            if choice == "1":
                self.CheckAvailability()  #Check availability
            elif choice == "2":
                self.BookSeats()  #Book a seat
            elif choice == "3":
                self.FreeSeat()  #Free a seat
            elif choice == "4":
                self.ShowBookingStatus()  #Show booking status
            elif choice == "5":
                self.PassengerSearch() # Search Booking by booking ID or passport
            elif choice == "6":
                self.db.close()
                print("Exiting program... Goodbye!")  #Exit message
                break  
            else:
                print("Invalid choice. Please select a valid option (1-5).")

if __name__ == "__main__":
    obj = AirlineBookingSystem()
    obj.menu()





