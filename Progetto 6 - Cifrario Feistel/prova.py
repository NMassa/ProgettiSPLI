import os
from files import *

if __name__ == "__main__":
    stringa = ['89504e47da1aa', 'ffd8ffe00104a46', '424df640000', ' ', '89504e47da1aa', '47496383961181']
            # [PNG,             JPG,                BMP,          RAW,  PNG, GIF]
    try:
        #file = open('/files/Periodic-Table.png', 'r')
        # file = open('files/frequency_cypher.txt', 'r')
        immagini = [file for file in os.listdir('files/')]
        file = open('files/' + immagini[3], 'rb')

    except OSError as e:
        print("errore apertura file")
        print(e)
    else:
        print("lettura file")
        f_byte = file.read(8)
        #compare_file(stringa , f_byte)
        print(''.join([r'{:x}'.format(c) for c in f_byte]))
        file.close()
        pippo = ''.join([r'{:x}'.format(c) for c in f_byte])
        for i in stringa:
            if i == pippo:
                print('ok')
                break
            else:
                print('non trovato')

