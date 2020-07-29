### point class for coordinates
class Point():
    def __init__(self, x, y): # self represent the object itself
        self.x = x
        self.y = y

# using the class to make the object p:
p = Point(2, 8)
# accesing the parameters of the object (Point / p)
print(p.x)
print(p.y)


### another class for airports named: Flight
class Flight():
    def __init__(self, capacity):
        self.capacity = capacity
        self.passengers = []
    
    def add_passenger(self, name):
        if not self.open_seats():
            return False
        else:
            self.passengers.append(name)
            return True         
    
    def open_seats(self):
        return self.capacity - len(self.passengers)

#using the Flight class to make a flight object with a capacity of 3
flight = Flight(3)

people = ["Harry", "Ron", "Hermione", "Ginny"]
for person in people:
    if flight.add_passenger(person):
        print(f"Added {person} to flight succesfully.")
    else:
        print(f"No available seats for {person}")