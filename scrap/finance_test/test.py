#

def get_number():

    try:
        number = int(input("Enter a number: "))
        return number
    except:
        print("Please enter a number.")
        number = get_number()
        return number


def is_an_int(number):
    if (number % 2) == 0:
        return "Even"
    else:
        return "Odd"


answer = is_an_int(get_number())
print(answer)
