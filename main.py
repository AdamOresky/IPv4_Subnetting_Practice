import random
import sys


# region Global variables

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


# A function that prints message
def incorrect_answer(message):
    print(message)


# A function that returns a class of an IP according to its first octet
def get_class():
    classes = ['A', 'B', 'C', 'D', 'E']
    interfaces = [128, 192, 224, 240, 256]
    return classes[interfaces.index(min(interfaces, key=lambda x: x < octets[0]))]


# A function that returns whether the IP address is private
def is_private():
    option_1 = octets[0] == 10  # 10.X.X.X (class A)
    option_2 = octets[0] == 100  # 100.X.X.X (Carrier NAT)
    option_3 = octets[0] == 165 and octets[1] == 254  # 165.254.X.X (APIPA)
    option_4 = octets == [172, 0, 0, 1]  # 172.0.0.1 (localhost)
    option_5 = octets[0] == 172 and 16 <= octets[1] < 32  # range 172.16.0.0 - 172.31.255.255 (class B)
    option_6 = octets[0] == 192 and octets[1] == 168  # 192.168.X.X (class C)

    if sum([option_1, option_2, option_3, option_4, option_5, option_6]):
        return True
    return False


# A function that returns the type (Network / Host / Broadcast) of an IP address and its network and broadcast address
def get_info():
    net_address = ''
    actual = 0
    interfaces = [8, 16, 24, 32]

    interface = min(interfaces, key=lambda x: x <= mask)
    multiples = 2 ** (interface - mask)
    while actual < 256:
        if actual <= octets[interfaces.index(interface)] <= actual + multiples - 1:
            for b in range(interfaces.index(interface)):
                net_address += str(octets[b]) + '.'
            bro_address = net_address

            net_address += str(actual)
            bro_address += str(actual + multiples - 1)

            while net_address.count('.') < 3:
                net_address += ".0"
                bro_address += ".255"

            if octets == net_address.split('.'):
                address_type = 'N'
            elif octets == bro_address.split('.'):
                address_type = 'B'
            else:
                address_type = 'H'

            return address_type, net_address, bro_address
        else:
            actual += multiples

# endregion


# region Input functions
# In this region, there are only functions that checks for user input and evaluate it

def class_input():
    right_answer = get_class()

    entered_answer = input("Enter class: ").upper()
    while entered_answer not in ['A', 'B', 'C', 'D', 'E']:
        entered_answer = input("Incorrect input. Enter class: ").upper()
    if entered_answer != right_answer:
        incorrect_answer(f'Incorrect. The correct answer is {right_answer}.')


def private_input():
    entered_answer = input("Specify whether the address is private or public. [pri/pub]: ").lower()
    while entered_answer not in ['pri', 'pub']:
        entered_answer = input("Incorrect input. Enter your answer again: ").lower()
    if entered_answer == "pub" and is_private():
        incorrect_answer("Incorrect. This address is private.")
    elif entered_answer == "pri" and not is_private():
        incorrect_answer("Incorrect. This address is public.")


def subnet_input(address_type, net_address, bro_address):
    address_base = ''
    for i in range(mask // 8):
        address_base += str(octets[i]) + '.'
    if address_type != 'N':
        entered_answer = input(f'Enter network address: {address_base}')
        if address_base + entered_answer != net_address:
            incorrect_answer(f'Incorrect. Network address is {net_address}')
    if address_type != "B":
        entered_answer = input(f'Enter broadcast address: {address_base}')
        if address_base + entered_answer != bro_address:
            incorrect_answer(f'Incorrect. Broadcast address is {bro_address}')


def type_input():
    address_type, net_address, bro_address = get_info()

    entered_answer = input("Specify whether this is a network, host, or broadcast address. [N/H/B]: ").upper()
    while entered_answer not in ['N', 'H', 'B']:
        entered_answer = input("Incorrect input. Enter your input again: ").upper()
    if entered_answer != address_type and address_type == 'N':
        incorrect_answer("Incorrect. This IP is a network address.")
    elif entered_answer != address_type and address_type == 'H':
        incorrect_answer("Incorrect. This IP is a host address.")
    elif entered_answer != address_type:
        incorrect_answer("Incorrect. This IP is a broadcast address.")

    subnet_input(address_type, net_address, bro_address)

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
