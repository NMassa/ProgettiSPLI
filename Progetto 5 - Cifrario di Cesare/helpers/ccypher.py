def caesar(message, shift):
    key = shift
    translated = ''

    for symbol in message:
        if symbol.isalpha():
            num = ord(symbol)
            num += key

            if symbol.isupper():
                if num > ord('Z'):
                    num -= 26
                elif num < ord('A'):
                    num += 26
            elif symbol.islower():
                if num > ord('z'):
                    num -= 26
                elif num < ord('a'):
                    num += 26

            translated += chr(num)
        else:
           translated += symbol
    return translated


def full_caesar(message, shift):
    key = shift
    translated = ''

    for symbol in message:
        if type(symbol) != int:
            num = ord(symbol)
        else:
            num = symbol

        if num > 16 or num < 10:
            num += key
            if num < 32:
                num += 95
            elif num > 126:
                num -= 95

        translated += chr(num)

    return translated


def decaesar(message,shift):
    key = -shift
    translated = ''

    for symbol in message:
        if symbol.isalpha():
            num = ord(symbol)
            num += key

            if symbol.isupper():
                if num > ord('Z'):
                    num -= 26
                elif num < ord('A'):
                    num += 26
            elif symbol.islower():
                if num > ord('z'):
                    num -= 26
                elif num < ord('a'):
                    num += 26

            translated += chr(num)
        else:
           translated += symbol
    return translated


def full_decaesar(message,shift):
    key = -shift
    translated = ''

    for symbol in message:
        if type(symbol) != int:
            num = ord(symbol)
        else:
            num = symbol

        if num > 16 or num < 10:
            num += key
            if num < 32:
                num += 95
            elif num > 126:
                num -= 95

        translated += chr(num)

    return translated