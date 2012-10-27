#!/usr/bin/env python
# 
# Copyright (c) 2012 Kyle Gorman
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

## constants
slax   = {'IH1', 'IH2', 'EH1', 'EH2', 'AE1', 'AE2', 'AH1', 'AH2', 
                                                    'UH1', 'UH2',}
vowels = {'IY1', 'IY2', 'IY0', 'EY1', 'EY2', 'EY0', 'AA1', 'AA2', 'AA0',
          'ER1', 'ER2', 'ER0', 'AW1', 'AW2', 'AW0', 'AO1', 'AO2', 'AO0',
          'AY1', 'AY2', 'AY0', 'OW1', 'OW2', 'OW0', 'OY1', 'OY2', 'OY0',
          'IH0', 'EH0', 'AE0', 'AH0', 'UH0', 'UW1', 'UW2', 'UW0', 'UW',
          'IY',  'EY',  'AA',  'ER',   'AW', 'AO',  'AY',  'OW',  'OY',  
          'UH',  'IH',  'EH',  'AE',  'AH',  'UH',} | slax

## medial onsets

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
# merely those that I believe need to be maximized in medial position.

def syllabify(pron, alaska_rule=True):
    """
    Syllabifies a CMU dictionary (ARPABET) word string

    1. Alaska rule must bleed onset maximization: a.las.ka
    2. Front onglides in 

    # Alaska rule:
    >>> print pretty(syllabify('AH0 L AE1 S K AH0'.split())), 'Alaska'
    -AH0-.L-AE1-S.K-AH0- Alaska
    >>> print pretty(syllabify('AH0 L AE1 S K AH0'.split(), 0)), 'Alaska'
    -AH0-.L-AE1-.S K-AH0- Alaska

    # huge medial onsets:
    >>> print pretty(syllabify('M IH1 N S T R AH0 L'.split())), 'minstrel'
    M-IH1-N.S T R-AH0-L minstrel
    >>> print pretty(syllabify('AA1  K T R W AA0 R'.split())), 'octroi'
    -AA1-K.T R W-AA0-R octroi

    # destressing
    >>> print pretty(destress(syllabify('M IH1 L AH0 T EH2 R IY0'.split()))), 'military'
    M-IH-.L-AH-.T-EH-.R-IY- military

    # normal treatment of 'j':
    >>> print pretty(syllabify('M EH1 N Y UW0'.split())), 'menu'
    M-EH1-N.Y-UW0- menu
    >>> print pretty(syllabify('S P AE1 N Y AH0 L'.split())), 'spaniel'
    S P-AE1-N.Y-AH0-L spaniel
    >>> print pretty(syllabify('K AE1 N Y AH0 N'.split())), 'canyon'
    K-AE1-N.Y-AH0-N canyon
    >>> print pretty(syllabify('M IH0 N Y UW2 EH1 T'.split())), 'minuet'
    M-IH0-N.Y-UW2-.-EH1-T minuet
    >>> print pretty(syllabify('JH UW1 N Y ER0'.split())), 'junior'
    JH-UW1-N.Y-ER0- junior
    >>> print pretty(syllabify('K L EH1 R IH0 HH Y UW0'.split())), 'clerihew'
    K L-EH1-.R-IH0-.HH Y-UW0- clerihew

    # nuclear treatment of 'j'
    >>> print pretty(syllabify('R EH1 S K Y UW0'.split())), 'rescue'
    R-EH1-S.K-Y UW0- rescue
    >>> print pretty(syllabify('T R IH1 B Y UW0 T'.split())), 'tribute'
    T R-IH1-B.Y-UW0-T tribute
    >>> print pretty(syllabify('N EH1 B Y AH0 L AH0'.split())), 'nebula'
    N-EH1-B.Y-AH0-.L-AH0- nebula
    >>> print pretty(syllabify('S P AE1 CH UH0 L AH0'.split())), 'spatula'
    S P-AE1-.CH-UH0-.L-AH0- spatula
    >>> print pretty(syllabify('AH0 K Y UW1 M AH0 N'.split())), 'acumen'
    -AH0-K.Y-UW1-.M-AH0-N acumen
    >>> print pretty(syllabify('S AH1 K Y AH0 L IH0 N T'.split())), 'succulent'
    S-AH1-K.Y-AH0-.L-IH0-N T succulent
    >>> print pretty(syllabify('F AO1 R M Y AH0 L AH0'.split())), 'formula'
    F-AO1 R-M.Y-AH0-.L-AH0- formula
    >>> print pretty(syllabify('V AE1 L Y UW0'.split())), 'value'
    V-AE1-L.Y-UW0- value

    # everything else
    >>> print pretty(syllabify('CH ER1 CH M AH0 N'.split())), 'churchmen'
    CH-ER1-CH.M-AH0-N churchmen
    >>> print pretty(syllabify('DH IY1'.split())), 'the' 
    DH-IY1- the
    >>> print pretty(syllabify('K AA1 M P AH0 N S EY2 T'.split())), 'compensate'
    K-AA1-M.P-AH0-N.S-EY2-T compensate
    >>> print pretty(syllabify('IH0 N S EH1 N S'.split())), 'inCENSE'
    -IH0-N.S-EH1-N S inCENSE
    >>> print pretty(syllabify('IH1 N S EH2 N S'.split())), 'INcense'
    -IH1-N.S-EH2-N S INcense
    >>> print pretty(syllabify('AH0 S EH1 N D'.split())), 'ascend'
    -AH0-.S-EH1-N D ascend
    >>> print pretty(syllabify('R OW1 T EY2 T'.split())), 'rotate'
    R-OW1-.T-EY2-T rotate
    >>> print pretty(syllabify('AA1 R T AH0 S T'.split())), 'artist'
    -AA1 R-.T-AH0-S T artist
    >>> print pretty(syllabify('AE1 K T ER0'.split())), 'actor'
    -AE1-K.T-ER0- actor
    >>> print pretty(syllabify('P L AE1 S T ER0'.split())), 'plaster'
    P L-AE1-S.T-ER0- plaster
    >>> print pretty(syllabify('B AH1 T ER0'.split())), 'butter'
    B-AH1-.T-ER0- butter
    >>> print pretty(syllabify('K AE1 M AH0 L'.split())), 'camel'
    K-AE1-.M-AH0-L camel
    >>> print pretty(syllabify('AH1 P ER0'.split())), 'upper'
    -AH1-.P-ER0- upper
    >>> print pretty(syllabify('B AH0 L UW1 N'.split())), 'balloon'
    B-AH0-.L-UW1-N balloon
    >>> print pretty(syllabify('P R OW0 K L EY1 M'.split())), 'proclaim'
    P R-OW0-.K L-EY1-M proclaim
    >>> print pretty(syllabify('IH0 N S EY1 N'.split())), 'insane'
    -IH0-N.S-EY1-N insane
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
        if len(onsets[i]) > 1 and alaska_rule and \
                                  nuclei[i-1][-1] in slax:
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

    return zip(onsets, nuclei, codas)


def pretty(syllab):
    return '.'.join('-'.join(' '.join(p) for p in syl) for syl in syllab)


def _destress(syllab):
    """
    Generate a syllabification with nuclear stress information removed
    """
    for (onset, nucleus, coda) in syllab:
        nuke = [p[:-1] if p[-1] in {'0', '1', '2'} else p for p in nucleus]
        yield (onset, nuke, coda)


def destress(syllab):
    return list(_destress(syllab))


if __name__ == '__main__':
    import doctest
    doctest.testmod()
