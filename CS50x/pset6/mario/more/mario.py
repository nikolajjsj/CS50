from cs50 import get_int

# prompt the user for int, in while loop, only breaking the loop if the int is 1-8
while True:
    n = get_int("Number: ")
    if n < 9 and n > 0:
        break

original_n = n

while n:
    print(" " * (n - 1), end="")
    print("#" * (original_n - (n - 1)), end="")
    print("  ", end="")
    print("#" * (original_n - (n - 1)))
    n -= 1