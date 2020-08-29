# Clyde "Thluffy" Sinclair
# Aug 2020

def factorial(n):
    if n == 0:
        return 1
    
    return n * factorial(n-1)

def fib(n):
    if n == 1:
        return 0
    if n == 2 or n == 3:
        return 1
    
    return fib(n-1) + fib(n-2)

print("Good News Everyone!")
print(f"4! = {factorial(4)}" )
print(f"fib(8) = {fib(8)}" )

