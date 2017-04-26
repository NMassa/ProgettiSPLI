import threading
import re
from helpers import ccypher
from helpers.utils import output


# class Bruteforce(threading.Thread):
#
#     def __init__(self, out_lck, cyphered, dict, shift, results):
#         threading.Thread.__init__(self)
#         self.out_lck = out_lck
#         self.cyphered = cyphered
#         self.dict = dict
#         self.shift = shift
#         self.results = results
#
#     def run(self):
#         text = ccypher.full_decaesar(self.cyphered, self.shift)
#         lst = re.findall(r"[\w']+", text)
#         for word in lst:
#             self.words.append(word)
#
#         output(self.out_lck, "Started bruteforce with shift %s..." % self.shift)
#         for word in self.words:
#             if word in self.dict:
#                 self.matches += 1
#             else:
#                 self.unmatches += 1
#
#         output(self.out_lck, "Terminated bruteforce with shift %s..." % self.shift)
#         accuracy = t.matches / (t.matches + t.unmatches)
#         res = {
#             "shift": t.shift,
#             "accuracy": accuracy
#         }
#         self.results.put(res)


def bruteforce(out_lck, cyphered, dict, shift, queue):
    words = []
    matches = 0
    unmatches = 0
    text = ccypher.full_decaesar(cyphered, shift)
    fout = open("bruteforce/___%s___.txt" % shift, "wt")
    fout.write(text)
    fout.close()

    lst = re.findall(r"[\w']+", text)
    for word in lst:
        words.append(word)

    output(out_lck, "Started bruteforce with shift %s..." % shift)
    for word in words:
        if word in dict:
            matches += 1
        else:
            unmatches += 1

    output(out_lck, "Terminated bruteforce with shift %s..." % shift)
    accuracy = matches / (matches + unmatches)
    #TODO: aggiungere al risultato matches e unmatches che fa figo
    res = {
        "shift": shift,
        "accuracy": accuracy
    }

    queue.put(res)
