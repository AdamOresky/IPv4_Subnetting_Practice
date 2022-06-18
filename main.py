import random
import sys


def class_check(first_octet):
    if 0 <= first_octet < 128:
        right_answer = "A"
    elif 128 <= first_octet < 192:
        right_answer = "B"
    elif 192 <= first_octet < 224:
        right_answer = "C"
    elif 224 <= first_octet < 240:
        right_answer = "D"
    elif 240 <= first_octet < 256:
        right_answer = "E"
    else:
        input("FATAL ERROR: The program does not recognize the class for the given IP address...")
        sys.exit()

    entered_answer = input("Enter class: ").upper()
    while entered_answer not in ["A", "B", "C", "D", "E"]:
        entered_answer = input("Incorrect input. Enter class: ")
    if entered_answer != right_answer:
        input(f'Incorrect. The correct answer is {right_answer}.')


def private_check(first_octet, second_octet):
    if first_octet == 10 or first_octet == 172 and 16 <= second_octet < 32 or first_octet == 192 and second_octet == 168:
        right_answer = "pri"
    else:
        right_answer = "pub"

    entered_answer = input("Specify whether the address is private or public. [pri/pub]: ").lower()
    while len(entered_answer) != 3 and entered_answer not in ['pri', 'pub']:
        entered_answer = input("Incorrect input. Enter your answer again: ")
    if entered_answer != right_answer and right_answer == "pri":
        input("Incorrect. This address is private.")
    elif entered_answer != right_answer and right_answer == "pub":
        input("Incorrect. This address is public.")


def subnet_check(octets, mask, type_of_address, net_address, bro_address):
    if mask >= 24:
        address_base = str(octets[0]) + "." + str(octets[1]) + "." + str(octets[2]) + "."
    else:
        address_base = str(octets[0]) + "." + str(octets[1]) + "."
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
    if 24 <= mask <= 30:
        multiples = 2 ** (32 - mask)
        while actual < 256 and type_of_address == "":
            if octets[3] == actual:
                type_of_address = "N"
            elif octets[3] == actual + multiples - 1:
                type_of_address = "B"
            elif actual < octets[3] < actual + multiples - 1:
                type_of_address = "H"
            else:
                actual += multiples
        net_address = str(octets[0]) + "." + str(octets[1]) + "." + str(octets[2]) + "." + str(actual)
        bro_address = str(octets[0]) + "." + str(octets[1]) + "." + str(octets[2]) + "." + str(actual + multiples - 1)
    elif 16 <= mask <= 23:
        multiples = 2 ** (24 - mask)
        while actual < 256 and type_of_address == "":
            if actual <= octets[2] < actual + multiples:
                net_address = str(octets[0]) + "." + str(octets[1]) + "." + str(actual) + ".0"
                bro_address = str(octets[0]) + "." + str(octets[1]) + "." + str(actual + multiples - 1) + ".255"
                if str(octets[0]) + "." + str(octets[1]) + "." + str(octets[2]) + "." + str(octets[3]) == net_address:
                    type_of_address = "N"
                elif str(octets[0]) + "." + str(octets[1]) + "." + str(octets[2]) + "." + str(octets[3]) == bro_address:
                    type_of_address = "B"
                else:
                    type_of_address = "H"
            else:
                actual += multiples
    else:
        input("FATAL ERROR: The program can't handle generated mask...")
        sys.exit()

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
    octets = [random.randint(0, 255) for i in range(4)]
    mask = random.randint(20, 30)
    print(f'IP: {octets[0]}.{octets[1]}.{octets[2]}.{octets[3]} /{mask}')
    class_check(int(octets[0]))
    private_check(int(octets[0]), int(octets[1]))
    type_of_address_check(octets, mask)
    print()
    main()


main()
