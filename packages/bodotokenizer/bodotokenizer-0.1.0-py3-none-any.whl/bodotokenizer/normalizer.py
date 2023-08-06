# from . import helpers
"""
Normalize characters 
"""
import re
from . import helpers

def normalize(sentence):
    sentence = sentence.strip()
    # Normalize sentence

    # Turn single quotes variation to sqv1|sqv2|sqv3..|sqvn
    single_quotes_regex = re.compile('|'.join(helpers.SINGLE_QUOTE))
    # Substitute variation with '
    sentence = re.sub(single_quotes_regex, "'", sentence)
    # Turn double quotes variation to dqv1|dgv2..|dgvn
    double_quotes_regex = re.compile('|'.join(helpers.DOUBLE_QUOTE))
    # Substitute variation with "
    sentence = re.sub(double_quotes_regex, '"', sentence)

    dari_quotes_regex = re.compile('|'.join(helpers.DARI_VARIATIONS))

    # print(dari_quotes_regex)
    # unicode value of । = \u0964
    # source https://www.fileformat.info/info/unicode/char/0964/index.htm
    sentence = re.sub(dari_quotes_regex, "\u0964", sentence)
    return sentence
    print(sentence)