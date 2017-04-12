import math
from difflib import SequenceMatcher
import operator
import os


class Frequency(object):

    def __init__(self, text):
        self.file_decrypt = text
        self.dictionary_frequency = None
        self.dictionary_frequency = {}
        self.index = 0
        self.file_input = open('helpers/frequency_input.txt', 'r')
        #self.list_file = ['books/(1) The Hunger Games.txt', 'books/(2) Catching Fire.txt', 'books/(3.1) Mockingjay.txt']
        self.list_file = [file for file in os.listdir('books/') if file.endswith('.txt')]


    def letter_frequency(self):

        while True:
            line = self.file_input.readline()
            if line == "":
                break
            else:
                letter, number = line.split()
                self.dictionary_frequency[letter] = int(number)
        self.file_input.close()

        file_output = open('helpers/frequency_output.txt', 'w')
        read_file = open(self.list_file[0], 'r')

        while True:
            letter2 = read_file.read(1)
            if letter2 == "":
                break
            else:
                self.index = self.index + 1
                if 96 < ord(letter2) < 123:
                    self.dictionary_frequency[letter2] = self.dictionary_frequency[letter2] + 1
                elif 64 < ord(letter2) < 91:
                    key = ord(letter2) + 32
                    self.dictionary_frequency[chr(key)] = self.dictionary_frequency[chr(key)] + 1

        while True:

            #trasformo il contatore di ogni lettera in una percentuale
            for key, value in  self.dictionary_frequency.items():
                self.dictionary_frequency[key] = self.dictionary_frequency[key]/self.index
            #ordino il dizionario trasformandolo in una lista di coppie
            dictionary_frequency_s = sorted(self.dictionary_frequency.items(), key=operator.itemgetter(1), reverse=True)
            #file_output.writelines('{} {}\n'.format(k, float(v / self.index) * 100) for k, v in dictionary_frequency_s.items())
            file_output.write('\n'.join('%s %s' % i for i in dictionary_frequency_s))
            file_output.write('\n')
            file_output.close()
            break

        read_file.close()
        print("finish")

    def crypt_file_frequency(self, file_crypt):
        file = open(file_crypt, 'r')
        dictionary_crypt = {}
        while True:
            line = file.readline()
            if line == "":
                break
            else:
                letter, number = line.split()
                dictionary_crypt[letter] = int(number)
        file.close()



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
