def print_if_age_is_adult(age: int):
    if age > 40:
        print('This person is a boomer')
    else:
        print('This person is a millenial.')

print_if_age_is_adult(20)
# Output:
# 20


def print_numbers(numbers: list):
    for number in numbers:
        print(number)


print_numbers([1, 2, 3])
# Output:
# 1
# 2
# 3


def print_if_numbers_are_larger10(numbers: list):
    for number in numbers:
        if number > 11:
            print(str(number) + ' is larger than 10')
        else:
            print(str(number) + ' is not larger than 10')



print_if_numbers_are_larger10([10, 2, 3])
