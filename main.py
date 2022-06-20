import random
import sys


def class_check(first_octet):
    classes = ["A", "B", "C", "D", "E"]
    interfaces = [128, 192, 224, 240, 256]

    if 0 <= first_octet <= 255:
        for i in range(len(interfaces)):
            if first_octet < interfaces[i]:
                right_answer = classes[i]
                break
    else:
        input("FATAL ERROR: The generated IP is not valid...")
        sys.exit()

    entered_answer = input("Enter class: ").upper()
    while entered_answer not in classes:
        entered_answer = input("Incorrect input. Enter class: ").upper()
    if entered_answer != right_answer:
        input(f'Incorrect. The correct answer is {right_answer}.')


def private_check(first_octet, second_octet):
    if first_octet == 10 or \
            first_octet == 172 and 16 <= second_octet < 32 or \
            first_octet == 192 and second_octet == 168:
        right_answer = "pri"
    else:
        right_answer = "pub"

    entered_answer = input("Specify whether the address is private or public. [pri/pub]: ").lower()
    while len(entered_answer) != 3 and entered_answer not in ['pri', 'pub']:
        entered_answer = input("Incorrect input. Enter your answer again: ").lower()
    if entered_answer != right_answer and right_answer == "pri":
        input("Incorrect. This address is private.")
    elif entered_answer != right_answer and right_answer == "pub":
        input("Incorrect. This address is public.")


def subnet_check(octets, mask, type_of_address, net_address, bro_address):
    address_base = ""
    for i in range(0, mask // 8):
        address_base += str(octets[i]) + "."
    if type_of_address != "N":
        entered_answer = input(f'Enter network address: {address_base}')
        if address_base + entered_answer != net_address:
            input(f'Incorrect. Network address is {net_address}')
    if type_of_address != "B":
        entered_answer = input(f'Enter broadcast address: {address_base}')
        if address_base + entered_answer != bro_address:
            input(f'Incorrect. Broadcast address is {bro_address}')


def type_of_address_check(octets, mask):
    type_of_address, net_address, bro_address = "", "", ""
    actual = 0
    interfaces = [8, 16, 24, 32]

    if 0 <= mask <= 30:
        for a in range(len(interfaces)):
            if mask < interfaces[a]:
                multiples = 2 ** (interfaces[a] - mask)
                while actual < 256:
                    if actual <= octets[a] <= actual + multiples - 1:
                        break
                    else:
                        actual += multiples
                for b in range(a):
                    net_address += str(octets[b]) + "."
                    bro_address += str(octets[b]) + "."
                net_address += str(actual)
                bro_address += str(actual + multiples - 1)
                while net_address.count(".") < 3:
                    net_address += ".0"
                    bro_address += ".255"
                break
    else:
        input("FATAL ERROR: The program can't handle generated mask...")
        sys.exit()

    if octets == net_address.split('.'):
        type_of_address = "N"
    elif octets == bro_address.split('.'):
        type_of_address = "B"
    else:
        type_of_address = "H"

    entered_answer = input("Specify whether this is a network, host, or broadcast address. [N/H/B]: ").upper()
    while entered_answer not in ['N', 'H', 'B']:
        entered_answer = input("Incorrect input. Enter your input again: ")
    if entered_answer != type_of_address and type_of_address == "N":
        input("Incorrect. This IP is a network address.")
    elif entered_answer != type_of_address and type_of_address == "H":
        input("Incorrect. This IP is a host address")
    elif entered_answer != type_of_address:
        input("Incorrect. This IP is a broadcast address.")

    subnet_check(octets, mask, type_of_address, net_address, bro_address)


def main():
    while True:
        octets = [random.randint(0, 255) for _ in range(4)]
        mask = random.randint(1, 30)
        print(f'IP: {octets[0]}.{octets[1]}.{octets[2]}.{octets[3]} /{mask}')
        class_check(int(octets[0]))
        private_check(int(octets[0]), int(octets[1]))
        type_of_address_check(octets, mask)
        print()


main()
