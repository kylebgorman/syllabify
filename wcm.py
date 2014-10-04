#!/usr/bin/env python

from syllabify import syllabify

## constants
DORSALS = {'K', 'G', 'NG'}
LIQUIDS = {'L', 'R'}
VOICED_AF = {'V', 'DH', 'Z', 'ZH'}
AF = {'F', 'TH', 'S', 'SH', 'CH'} | VOICED_AF


def wcm(phonemes, *sylab):
    """
    The "Word Complexity Measure", as proposed in:

    C. Stoel-Gammon. 2010. The Word Complexity Measure: Description and 
    application to developmental phonology and disorders. Clinical
    Linguistics and Phonetics 24(4-5): 271-282.
    """
    syls = syllabify(phonemes) 
    # begin scoring
    score = 0
    ## Word patterns
    # (1) Productions with more than two syllables receive 1 point
    if len(syls) > 2:
        score += 1
    # FIXME <stupid_rule>
    # (2) Productions with stress on any syllable but the first receive 
    # 1 point [this rule is stupid --KG]
    if len(syls) > 1 and not syls[0][1][-1].endswith('1'):
        score += 1
    # FIXME </stupid_rule>
    ## Syllable structures
    # (1) Productions with a word-final consonant receive 1 point
    if syls[-1][2] != []:
        score += 1
    # (2) Productions with a syllable cluster (defined as a sequence of 
    # two or more consonants within a syllable) receive one point for 
    # each cluster:
    for syl in syls:
        if len(syl[0]) > 1:
            score += 1
        if len(syl[2]) > 1:
            score += 1
    ## Sound classes
    # (1) Productions with a velar consonant receive 1 point for each 
    # velar
    for syl in syls:
        score += sum(ph in DORSALS for ph in (syl[0] + syl[2]))
    # (2) Productions with a liquid, a syllabic liquid, or a rhotic vowel 
    # receive 1 point for each liquid, syllabic liquid, and rhotic vowel
    for syl in syls:
        score += sum(ph in LIQUIDS for ph in (syl[0] + syl[2]))
        score += sum(len(ph) > 1 and ph[1] == 'R' for ph in syl[1])
    # (3) Productions with a fricative or affricate receive 1 point for
    # each fricative and affricate
        score += sum(ph in AF for ph in (syl[0] + syl[2]))
    # (4) Productions with a voiced fricative or affricate receive 1 point
    # for each fricative and affricate (in addition to the point received
    # for #3)
    for syl in syls:
        score += sum(ph in VOICED_AF for ph in (syl[0] + syl[2]))
    # and we're done
    return score
