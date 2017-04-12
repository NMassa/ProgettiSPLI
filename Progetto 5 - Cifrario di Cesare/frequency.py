import math
from difflib import SequenceMatcher


class Frequency(object):

    def __init__(self):
        self.file_decrypt = object
        self.dictionary_frequency = None
        self.dictionary_frequency = {}
        self.index = 0
        self.file_input = open('frequency_input.txt', 'r')
        self.list_file('u', ['books/(1) The Hunger Games.txt',
                             'books/(2) Catching Fire.txt',
                             'books/(3.1) Mockingjay.txt'])

    def letter_frequency(self):

        while True:
            line = self.file_input.readline()
            if line == "":
                print("finish")
                break
            else:
                letter, number = line.split()
                self.dictionary_frequency[letter] = int(number)
        self.file_input.close()

        file_output = open('frequency_output.txt', 'w')
        read_file = open(self.list_file[0], 'r')

        while True:
            letter2 = read_file.read(1)
            if letter2 == "":
                print("finish")
                break
            else:
                self.index + 1
                if 96 < ord(letter2) < 123:
                    self.dictionary_frequency[letter2] = self.dictionary_frequency[letter2] + 1
                elif 64 < ord(letter2) < 91:
                    key = ord(letter2) + 32
                    self.dictionary_frequency[chr(key)] = self.dictionary_frequency[chr(key)] + 1

        while True:
            file_output.writelines('{} {}\n'.format(k, float(v / self.index)) for k, v in self.dictionary_frequency.items())
            file_output.write('\n')
            file_output.close()
            break

        read_file.close()

    #restituisce percentuale
    def similar(a, b):
        return SequenceMatcher(None, a, b).ratio()

    '''ho considerato il file delle occorrenze strutturato così:
       abcdefghi.......
       80,32
       70,77
       66,55
       ...
       ...
       ...
    '''
    def frequency_compare(self, file):
            self.file = file
            self.freq_orig = []
            self.freq_crypt = []
            percent = []
            #alfabeto = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z']

            #chiamo regola che mi conta
            # le occorrenze nel file criptato
            f = open('..........txt', 'rb') #file con occorrenze da noi criptato
            o = open('..........txt', 'rb') #file con occorrenze della lingua

            for i in range(1, 26):
                self.freq_crypt = f.readlines(i)
                self.freq_orig = o.readlines(i)
                percent = [similar(self.freq_crypt, self.freq_orig)] #ritorna la percentuale di quanto sono simili
                print('percentuale corrispondeza di %s ', percent[i])

            print('Percentuale accettabile? digitare "ok" per conferma')
            ok = input()
            if ok =='ok':
                #prende le prime lettere dei file, le converte in numero e ne calcola la distanza
                #la distanza calcolata è la chiave di decifrazione
                #non so se abbiamo già implementata la funzione che converte lettere in numeri, nel caso si può usare la seguente
                n = bin(ord(self.freq_crypt[1]))
                m = bin(ord(self.freq_orig[1]))
                int(n, 2)
                int(m, 2)
                key = math.fabs(n-m)
                #ora abbiamo la chiave e possiamo decriptare
            else:
                print('Option not available')
