people = [
    {"name": "Harry", "house": "Gryffindor"},
    {"name": "Cho", "house": "Ravenclaw"},
    {"name": "Draco", "house": "Slytherin"}
]

# one way of using function sort
def f(person):
    return person["name"]
people.sort(key=f)

# another way using lamda keyword:
people.sort(key=lambda person: person["name"])


print(people)