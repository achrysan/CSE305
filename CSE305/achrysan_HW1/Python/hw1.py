#!/usr/bin/env python
import re
def hw1(inString, outString):
        file_read = open(inString, 'r')
        text_in_f = file_read.readlines()
        print(text_in_f)
        alphabet = 'abcdefghijklmnopqrstuvwxyz'
        file_write = open(outString, 'w')
        for x in text_in_f:
            x = re.sub(r'[?|$|.|!|\"|\'|&|%|#|@|*|;|:|{|}|<|>|,|-]',r'',x)
            print(x)
            x = x.lower()
            x = "".join(set(x))
            x = x.replace('\n', '')
            x = x.replace('.', '')
            x = x.replace(' ', '')
            x = x.replace('(', '')
            x = x.replace(')', '')
            x = ''.join(sorted(x))
            print(x)
            if x == alphabet:
                file_write.write('true\n')
            else:
                file_write.write('false\n')
