import random
import sys


# region Global variables

classes = ['A', 'B', 'C', 'D', 'E']
octets = []
mask = 0

# endregion


# region Logic functions

# A function that generates needed variables for the program at the beginning of a new problem
def startup_config():
    global octets, mask
    octets = [random.randint(0, 255) for _ in range(4)]
    mask = random.randint(1, 30)


# A function that checks for any possible errors that may occur after running startup_config()
def check_possible_errors():
    for octet in octets:
        if 0 > octet > 255:
            input("FATAL ERROR: The generated IP is not valid...")
            sys.exit()
    if 1 > mask > 30:
        input("FATAL ERROR: The program can't handle generated mask...")
        sys.exit()


# A function that returns a class of an IP according to its first octet
def class_logic():
    interfaces = [128, 192, 224, 240, 256]

    for i in range(len(interfaces)):
        if octets[0] < interfaces[i]:
            return classes[i]


# A function that returns whether the IP address is private or public
def private_logic():
    option_1 = octets[0] == 10  # 10.X.X.X (class A)
    option_2 = octets[0] == 100  # 100.X.X.X (Carrier NAT)
    option_3 = octets[0] == 165 and octets[1] == 254  # 165.254.X.X (APIPA)
    option_4 = octets == [172, 0, 0, 1]  # 172.0.0.1 (localhost)
    option_5 = octets[0] == 172 and 16 <= octets[1] < 32  # range 172.16.0.0 - 172.31.255.255 (class B)
    option_6 = octets[0] == 192 and octets[1] == 168  # 192.168.X.X (class C)

    if sum([option_1, option_2, option_3, option_4, option_5, option_6]):
        return "pri"
    else:
        return "pub"


# A function that returns the type (Network / Host / Broadcast) of an IP address and its attributes
def type_logic():
    type_of_address, net_address, bro_address = '', '', ''
    actual = 0
    interfaces = [8, 16, 24, 32]

    for a in range(len(interfaces)):
        if mask < interfaces[a]:
            multiples = 2 ** (interfaces[a] - mask)
            while actual < 256:
                if actual <= octets[a] <= actual + multiples - 1:
                    for b in range(a):
                        net_address += str(octets[b]) + '.'
                    bro_address = net_address

                    net_address += str(actual)
                    bro_address += str(actual + multiples - 1)

                    while net_address.count('.') < 3:
                        net_address += ".0"
                        bro_address += ".255"

                    if octets == net_address.split('.'):
                        type_of_address = 'N'
                    elif octets == bro_address.split('.'):
                        type_of_address = 'B'
                    else:
                        type_of_address = 'H'

                    return type_of_address, net_address, bro_address
                else:
                    actual += multiples

# endregion


# region Input functions
# In this region, there are only functions that checks for user input and evaluate it

def class_input():
    right_answer = class_logic()

    entered_answer = input("Enter class: ").upper()
    while entered_answer not in classes:
        entered_answer = input("Incorrect input. Enter class: ").upper()
    if entered_answer != right_answer:
        input(f'Incorrect. The correct answer is {right_answer}.')


def private_input():
    right_answer = private_logic()

    entered_answer = input("Specify whether the address is private or public. [pri/pub]: ").lower()
    while entered_answer not in ['pri', 'pub']:
        entered_answer = input("Incorrect input. Enter your answer again: ").lower()
    if entered_answer != right_answer and right_answer == "pri":
        input("Incorrect. This address is private.")
    elif entered_answer != right_answer and right_answer == "pub":
        input("Incorrect. This address is public.")


def subnet_input(type_of_address, net_address, bro_address):
    address_base = ''
    for i in range(0, mask // 8):
        address_base += str(octets[i]) + '.'
    if type_of_address != 'N':
        entered_answer = input(f'Enter network address: {address_base}')
        if address_base + entered_answer != net_address:
            input(f'Incorrect. Network address is {net_address}')
    if type_of_address != "B":
        entered_answer = input(f'Enter broadcast address: {address_base}')
        if address_base + entered_answer != bro_address:
            input(f'Incorrect. Broadcast address is {bro_address}')


def type_input():
    type_of_address, net_address, bro_address = type_logic()

    entered_answer = input("Specify whether this is a network, host, or broadcast address. [N/H/B]: ").upper()
    while entered_answer not in ['N', 'H', 'B']:
        entered_answer = input("Incorrect input. Enter your input again: ")
    if entered_answer != type_of_address and type_of_address == 'N':
        input("Incorrect. This IP is a network address.")
    elif entered_answer != type_of_address and type_of_address == 'H':
        input("Incorrect. This IP is a host address.")
    elif entered_answer != type_of_address:
        input("Incorrect. This IP is a broadcast address.")

    subnet_input(type_of_address, net_address, bro_address)

# endregion


def main():
    startup_config()
    check_possible_errors()
    print(f'IP: {octets[0]}.{octets[1]}.{octets[2]}.{octets[3]} /{mask}')
    class_input()
    private_input()
    type_input()
    print()


while True:
    main()
