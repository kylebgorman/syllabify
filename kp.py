# Copyright (c) 201X Kyle Gorman
# 
# Permission is hereby granted, free of charge, to any person obtaining a 
# copy of this software and associated documentation files (the 
# "Software"), to deal in the Software without restriction, including 
# without limitation the rights to use, copy, modify, merge, publish, 
# distribute, sublicense, and/or sell copies of the Software, and to 
# permit persons to whom the Software is furnished to do so, subject to 
# the following conditions:
# 
# The above copyright notice and this permission notice shall be included 
# in all copies or substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS 
# OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF 
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. 
# IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY 
# CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, 
# TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE 
# SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
# 
# kp.py: prints dorsal-labial medial clusters from the CMU dictionary
# Kyle Gorman <kgorman@ling.upenn.edu>

from syllabify import syllabify

if __name__ == '__main__':
    source = open('cmudict.0.7a', 'r')
    for line in source:
        if line[0] == ';':                   # header, comments
            continue                         # starts next iter of loop
        (word, pron) = line.rstrip().split('  ', 1)
        syllables = syllabify(pron.split())  # syllabify pronunciation
        for i in xrange(len(syllables) - 1):
            coda  = syllables[i][2]
            onset = syllables[i + 1][0]
            if coda and coda[-1] in {'K', 'G',}:           
                if onset and onset[0] in {'P', 'B', 'F', 'V',}:
                    print word
                    break                    # don't print a word twice  
