#!/usr/bin/env python
# Copyright (c) 2012-2013 Kyle Gorman <gormanky@ohsu.edu>
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
# syllabify.py: prosodic parsing of ARPABET entries

from itertools import chain

## constants
slax   = {'IH1', 'IH2', 'EH1', 'EH2', 'AE1', 'AE2', 'AH1', 'AH2', 
                                                    'UH1', 'UH2',}
vowels = {'IY1', 'IY2', 'IY0', 'EY1', 'EY2', 'EY0', 'AA1', 'AA2', 'AA0',
          'ER1', 'ER2', 'ER0', 'AW1', 'AW2', 'AW0', 'AO1', 'AO2', 'AO0',
          'AY1', 'AY2', 'AY0', 'OW1', 'OW2', 'OW0', 'OY1', 'OY2', 'OY0',
          'IH0', 'EH0', 'AE0', 'AH0', 'UH0', 'UW1', 'UW2', 'UW0', 'UW',
          'IY',  'EY',  'AA',  'ER',   'AW', 'AO',  'AY',  'OW',  'OY',  
          'UH',  'IH',  'EH',  'AE',  'AH',  'UH',} | slax

## licit medial onsets

o2 = {('P', 'R'), ('T', 'R'), ('K', 'R'), ('B', 'R'), ('D', 'R'),
      ('G', 'R'), ('F', 'R'), ('TH', 'R'), 
      ('P', 'L'), ('K', 'L'), ('B', 'L'), ('G', 'L'), 
      ('F', 'L'), ('S', 'L'),
      ('K', 'W'), ('G', 'W'), ('S', 'W'),
      ('S', 'P'), ('S', 'T'), ('S', 'K'),
      ('HH', 'Y'), # "clerihew"
      ('R', 'W'),} # "octroi"
o3 = {('S', 'T', 'R'), ('T', 'R', 'W'),}

# This does not represent anything like a complete list of onsets, but 
# merely those that need to be maximized in medial position.

def syllabify(pron, alaska_rule=True):
    """
    Syllabifies a CMU dictionary (ARPABET) word string

    # Alaska rule:
    >>> pretty(syllabify('AH0 L AE1 S K AH0'.split())) # Alaska
    '-AH0-.L-AE1-S.K-AH0-'
    >>> pretty(syllabify('AH0 L AE1 S K AH0'.split(), 0)) # Alaska
    '-AH0-.L-AE1-.S K-AH0-'

    # huge medial onsets:
    >>> pretty(syllabify('M IH1 N S T R AH0 L'.split())) # minstrel
    'M-IH1-N.S T R-AH0-L'
    >>> pretty(syllabify('AA1  K T R W AA0 R'.split())) # octroi
    '-AA1-K.T R W-AA0-R'

    # destressing
    >>> pretty(destress(syllabify('M IH1 L AH0 T EH2 R IY0'.split())))
    'M-IH-.L-AH-.T-EH-.R-IY-'

    # normal treatment of 'j':
    >>> pretty(syllabify('M EH1 N Y UW0'.split())) # menu
    'M-EH1-N.Y-UW0-'
    >>> pretty(syllabify('S P AE1 N Y AH0 L'.split())) # spaniel
    'S P-AE1-N.Y-AH0-L'
    >>> pretty(syllabify('K AE1 N Y AH0 N'.split())) # canyon
    'K-AE1-N.Y-AH0-N'
    >>> pretty(syllabify('M IH0 N Y UW2 EH1 T'.split())) # minuet
    'M-IH0-N.Y-UW2-.-EH1-T'
    >>> pretty(syllabify('JH UW1 N Y ER0'.split())) # junior
    'JH-UW1-N.Y-ER0-'
    >>> pretty(syllabify('K L EH R IH HH Y UW'.split())) # clerihew
    'K L-EH-.R-IH-.HH Y-UW-'

    # nuclear treatment of 'j'
    >>> pretty(syllabify('R EH1 S K Y UW0'.split())) # rescue
    'R-EH1-S.K-Y UW0-'
    >>> pretty(syllabify('T R IH1 B Y UW0 T'.split())) # tribute
    'T R-IH1-B.Y-UW0-T'
    >>> pretty(syllabify('N EH1 B Y AH0 L AH0'.split())) # nebula
    'N-EH1-B.Y-AH0-.L-AH0-'
    >>> pretty(syllabify('S P AE1 CH UH0 L AH0'.split())) # spatula
    'S P-AE1-.CH-UH0-.L-AH0-'
    >>> pretty(syllabify('AH0 K Y UW1 M AH0 N'.split())) # acumen
    '-AH0-K.Y-UW1-.M-AH0-N'
    >>> pretty(syllabify('S AH1 K Y AH0 L IH0 N T'.split())) # succulent
    'S-AH1-K.Y-AH0-.L-IH0-N T'
    >>> pretty(syllabify('F AO1 R M Y AH0 L AH0'.split())) # formula
    'F-AO1 R-M.Y-AH0-.L-AH0-'
    >>> pretty(syllabify('V AE1 L Y UW0'.split())) # value
    'V-AE1-L.Y-UW0-'

    # everything else
    >>> pretty(syllabify('N AO0 S T AE1 L JH IH0 K'.split())) # nostalgic
    'N-AO0-.S T-AE1-L.JH-IH0-K'
    >>> pretty(syllabify('CH ER1 CH M AH0 N'.split())) # churchmen
    'CH-ER1-CH.M-AH0-N'
    >>> pretty(syllabify('K AA1 M P AH0 N S EY2 T'.split())) # compensate
    'K-AA1-M.P-AH0-N.S-EY2-T'
    >>> pretty(syllabify('IH0 N S EH1 N S'.split())) # inCENSE
    '-IH0-N.S-EH1-N S'
    >>> pretty(syllabify('IH1 N S EH2 N S'.split())) # INcense
    '-IH1-N.S-EH2-N S'
    >>> pretty(syllabify('AH0 S EH1 N D'.split())) # ascend
    '-AH0-.S-EH1-N D'
    >>> pretty(syllabify('R OW1 T EY2 T'.split())) # rotate
    'R-OW1-.T-EY2-T'
    >>> pretty(syllabify('AA1 R T AH0 S T'.split())) # artist
    '-AA1 R-.T-AH0-S T'
    >>> pretty(syllabify('AE1 K T ER0'.split())) # actor
    '-AE1-K.T-ER0-'
    >>> pretty(syllabify('P L AE1 S T ER0'.split())) # plaster
    'P L-AE1-S.T-ER0-'
    >>> pretty(syllabify('B AH1 T ER0'.split())) # butter
    'B-AH1-.T-ER0-'
    >>> pretty(syllabify('K AE1 M AH0 L'.split())) # camel
    'K-AE1-.M-AH0-L'
    >>> pretty(syllabify('AH1 P ER0'.split())) # upper
    '-AH1-.P-ER0-'
    >>> pretty(syllabify('B AH0 L UW1 N'.split())) # balloon
    'B-AH0-.L-UW1-N'
    >>> pretty(syllabify('P R OW0 K L EY1 M'.split())) # proclaim
    'P R-OW0-.K L-EY1-M'
    >>> pretty(syllabify('IH0 N S EY1 N'.split())) # insane
    '-IH0-N.S-EY1-N'
    """
    ## main pass
    mypron = list(pron)
    nuclei = []
    onsets = []
    i = -1
    for (j, seg) in enumerate(mypron):
        if seg in vowels:
            nuclei.append([seg])
            onsets.append(mypron[i + 1:j]) # actually interludes, r.n.
            i = j                        
    codas = [mypron[i + 1:]]
    ## resolve disputes and compute coda
    for i in xrange(1, len(onsets)):
        coda = []
        # boundary cases
        if len(onsets[i]) > 1 and onsets[i][0] == 'R':
            nuclei[i - 1].append(onsets[i].pop(0))
        if len(onsets[i]) > 2 and onsets[i][-1] == 'Y':
            nuclei[i].insert(0, onsets[i].pop())
        if len(onsets[i]) > 1 and alaska_rule and nuclei[i-1][-1] in slax:
            coda.append(onsets[i].pop(0))
        # onset maximization
        depth = 1
        if len(onsets[i]) > 1:
            if tuple(onsets[i][-2:]) in o2:
                depth = 3 if tuple(onsets[i][-3:]) in o3 else 2
        for j in xrange(len(onsets[i]) - depth):
            coda.append(onsets[i].pop(0))
        # store coda
        codas.insert(i - 1, coda)

    ## verify that all segments are included in the ouput
    output = zip(onsets, nuclei, codas)
    flat_output = list(chain.from_iterable(chain.from_iterable(output)))
    if flat_output != mypron:
        raise ValueError("could not syllabify {}, got {}".format(mypron, flat_output))

    return output


def pretty(syllab):
    return '.'.join('-'.join(' '.join(p) for p in syl) for syl in syllab)


def destress(syllab):
    """
    Generate a syllabification with nuclear stress information removed
    """
    syls = []
    for (onset, nucleus, coda) in syllab:
        nuke = [p[:-1] if p[-1] in {'0', '1', '2'} else p for p in nucleus]
        syls.append((onset, nuke, coda))
    return syls


if __name__ == '__main__':
    import doctest
    doctest.testmod()
