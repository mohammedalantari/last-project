
class AirlineBookingSystem:
    def __init__(self):
        self.seats = [] #initializing an empty list for the sitting plan
        self.status =[] #this list will store status of each seat (i.e. booked/free)

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
        self.CheckAvailability() #displaying the available seats
        while True:
            seat_name = input("Enter seat number or type '-1' to quit: ").strip() #user will press -1 to exit the booking function

            if seat_name.lower() == "-1":
                print("Exiting booking system...")
                break  # Exit the booking process

            if seat_name not in self.seats: #invalid input
                print("Invalid seat name. Please enter a valid seat from the list.")
                continue

            index = self.seats.index(seat_name)  # Find the index of the seat

            # Check if the seat is available
            if self.seats[index] == "X": #check for aisle
                print(f" Seat {seat_name} is in the aisle area and cannot be booked.")
                continue
            elif self.seats[index] == "S": #check for storage
                print(f"Seat {seat_name} is in the storage area and cannot be booked.")
                continue
            elif self.status[index] == "R": #check for already booked seat
                print(f"Seat {seat_name} is already booked. Please choose another seat.")
                continue

            # If seat is available, proceed with booking
            self.update(index, "R")
            print(f"Seat {seat_name} booked successfully!")

            self.CheckAvailability()

    #this function will provide functionality of freeing a seat
    def FreeSeat(self):
        seat_name = input("Enter seat number to free: ").strip()

        if seat_name not in self.seats: #inavlid input
            print("Invalid seat name. Please enter a valid seat.")
            return

        index = self.seats.index(seat_name)  # Find the seat index

        if self.status[index] == "R":
            self.update(index, "F")  # Mark the seat as free
            print(f"Seat {seat_name} is now free!")
        else: #if user selects a seat which is not booked
            print(f"Seat {seat_name} is not booked, so it cannot be freed.")

        self.ShowBookingStatus()  # Display the updated seat status

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
            print("5. Exit program")

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
                print("Exiting program... Goodbye!")  #Exit message
                break  
            else:
                print("Invalid choice. Please select a valid option (1-5).")

if __name__ == "__main__":
    obj = AirlineBookingSystem()
    obj.menu()





