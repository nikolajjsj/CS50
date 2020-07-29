### print function for the famous Hello, world!
print("Hello, world!")


### input for name and then print it
name = input("Name: ")
print("Hello, " + name)
name = input("Name: ")
print(f"Hello, {name}")


### conditions
n = int(input("Number: "))

if n > 0:
    print("Number is positive")
elif n < 0:
    print("Number is negative")
else:
    print("Number is zero")


### sequences
name = "Harry"
print(name[0])

names = ["Harry", "Ron", "Hermione"]
print(names[0])

coordinateX = 10.0
coordinateY = 20.0
# or better yet a tuple:
coordinate = (10.0, 20.0)


### lists
# Define a list of names (example of a comment)
names = ["Harry", "Ron", "Hermione", "Ginny"]
# appends "Draco" to the end of the list
names.append("Draco")
# sorts the list in alphabetic order
names.sort()


### sets
# sets' values are uniques
s = set()
s.add(1)
s.add(2)
s.add(3)
s.remove(2)
# len gets the length of some type
print(f"The set has {len(s)} elements.")


### loops
for i in [0, 1, 2, 3, 4, 5]:
    print(i)
# or better use range() instead of list
for i in range(6):
    print(i)
# or loop over a name
names = ["Harry", "Ron", "Hermione", "Ginny"]
for i in names:
    print(i)
# or for characters in a name
name = "Harry"
for i in name:
    print(i)


### dictionaries
houses = {
    "Harry": "Gryffindor", 
    "Draco": "Slytherin",
}
houses["Hermione"] = "Gryffindor"
print(houses["Harry"])


### functions
def square(x):
    return x * x
# for loop giving the square of i in range(10)
for i in range(10):
    print(f"The square of {i} is {square(i)}")

# how to import:
# from functions import square: use square directly (square())
# or
# import functions: use square indirectly (functions.square())
# to import the whole file

