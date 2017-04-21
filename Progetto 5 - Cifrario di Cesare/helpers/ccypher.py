
def caesar(message, shift):
    translate = ''
    for carattere in message:
        ascii = ord(carattere)
        cif = ascii
        #if ascii == 65279:
         #   translate = ''
        if (ascii >= 97 and ascii <= 122):
            cif = ascii + shift
            if cif >122:
                diff = cif - 122
                cif = 96 + diff
            translate += chr(cif)
        elif (ascii >= 65 and ascii <= 90):
            cif = ascii + shift
            cif = cif+32
            if cif >122:
                diff = cif - 122
                cif = 96 + diff
            translate += chr(cif)
        elif ascii == 65279:
            translate += ''
        else:
            translate += carattere
    return translate


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
        if type(symbol) != int:
            num = ord(symbol)
        else:
            num = symbol
        if (97<=num<=122):
            num += key
            if num >= ord('z'):
                num -= 26
                translated += chr(num)
            elif num < ord('a'):
                num += 26
                translated += chr(num)
            else:
                translated += chr(num)
        else:
            translated += chr(symbol)
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