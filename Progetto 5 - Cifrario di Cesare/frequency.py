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

        for file_index in self.list_file:
            read_file = open('books/' + file_index, 'r')
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
            read_file.close()

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

        print("finish 1")

    #funzione che genera la frequenza delle lettere sul file ricevuto dalla socket
    def crypt_file_frequency(self, file_crypt):

        self.file_input = open('helpers/frequency_input.txt', 'r')
        dictionary_crypt = {}
        while True:
            line = self.file_input.readline()
            if line == "":
                break
            else:
                letter, number = line.split()
                dictionary_crypt[letter] = int(number)
        self.file_input.close()

        #file = open(file_crypt, 'r')
        file = open('received/cifrato.txt', 'r')

        while True:
            letter2 = file.read(1)
            if letter2 == "":
                break
            else:
                self.index = self.index + 1
                if 96 < ord(letter2) < 123:
                    dictionary_crypt[letter2] = dictionary_crypt[letter2] + 1
                elif 64 < ord(letter2) < 91:
                    key = ord(letter2) + 32
                    dictionary_crypt[chr(key)] = dictionary_crypt[chr(key)] + 1
        file.close()

        file_output = None
        file_output = open('helpers/frequency_cypher.txt', 'w')
        while True:
            #trasformo il contatore di ogni lettera in una percentuale
            for key, value in dictionary_crypt.items():
                dictionary_crypt[key] = dictionary_crypt[key]/self.index
            #ordino il dizionario trasformandolo in una lista di coppie
            dictionary_frequency_s = sorted(dictionary_crypt.items(), key=operator.itemgetter(1), reverse=True)
            #file_output.writelines('{} {}\n'.format(k, float(v / self.index) * 100) for k, v in dictionary_frequency_s.items())
            file_output.write('\n'.join('%s %s' % i for i in dictionary_frequency_s))
            file_output.write('\n')
            file_output.close()
            break

        print("finish 2")



    def decipher(self, file_receive):
        self.crypt_file_frequency(file_receive)
        self.frequency_compare(file_receive)

    #restituisce percentuale
    def similar(self, a, b):
        return SequenceMatcher(None, a, b).ratio()

    '''ho considerato il file delle occorrenze strutturato così:

       a 80,32
       b 70,77
       c 66,55
       ...
       ...
       ...
    '''
    def frequency_compare(self):
            #self.file = file
            self.freq_orig_value = []
            self.freq_crypt_value = []
            self.freq_crypt_char = []
            self.freq_orig_char = []
            percent = []
            i = 0

            with open('helpers/frequency_cypher.txt', 'r') as f:
                for line1 in f:
                    self.freq_crypt_char.append(line1.split(None, 1)[0]) #stampo la i-esima lettera
                    self.freq_crypt_value.append(line1.split(None, 1)[1])#stampo il i-esimo valore
                    i += 1
            with open('helpers/frequency_output.txt', 'r') as o:
                for line2 in o:
                    self.freq_orig_char.append(line2.split(None, 1)[0])
                    self.freq_orig_value.append(line2.split(None, 1)[1])
                    i += 1

            for i in range(0, 25):
                #se da errore commentare la riga sotto che non la si usa per trovare la chiave
                print(math.fabs(float(self.freq_crypt_value[i]) - float(self.freq_orig_value[i])) / float(self.freq_crypt_value[i]))
                value1 = str(self.freq_crypt_value[i])
                value2 = str(self.freq_orig_value[i])
                percent.append(self.similar(value1[:5], value2[:5])) #faccio compare solo sulle prime 4 cifre del numero, percentuale ottima ora!!!
                                                                # ovviamente più aumento il numero di cifre più la percentuale cala
                str1 = str(percent[i]) #così poi stampo solo le prime 2 cifre
                print('% correspondence of', self.freq_crypt_char[i], '--->', self.freq_orig_char[i], ' is', str1[:3])

            print(' Acceptable rate? Digit "ok" to confirm')
            ok = input()
            if ok == 'ok':
                n = bin(ord(self.freq_crypt_char[1]))
                m = bin(ord(self.freq_orig_char[1]))
                n =int(n,2)
                m =int(m,2)
                #print(n)#valore associato primo carattere
                #print(m)
                key = int(math.fabs(n - m))
                print('Search Key is :',key)
                return key
            else:
                print('Low rate \n')
                return None