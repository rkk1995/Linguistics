# SIMPLY RUN THIS FILE AND CHECK TERMINAL OUTPUT
# USE IF SECRET KEY IS COMPROMISED
# ADJUST FUNCTION ON LINE 53 IF NEED DIFFERENT KEY PARAMETERS

"""
this includes some of Django's standard crypto functions and utilities.
"""
from __future__ import unicode_literals
from django.conf import settings

import hashlib
import time

# Use the system PRNG if possible
import random
try:
    random = random.SystemRandom()
    using_sysrandom = True
except NotImplementedError:
    import warnings
    warnings.warn('A secure pseudo-random number generator is not available '
                  'on your system. Falling back to Mersenne Twister.')
    using_sysrandom = False

def get_random_string(length=12,
                      allowed_chars='abcdefghijklmnopqrstuvwxyz'
                                    'ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'):
    """
    Returns a securely generated random string.

    The default length of 12 with the a-z, A-Z, 0-9 character set returns
    a 71-bit value. log_2((26+26+10)^12) =~ 71 bits
    """
    if not using_sysrandom:
        # This is ugly, and a hack, but it makes things better than
        # the alternative of predictability. This re-seeds the PRNG
        # using a value that is hard for an attacker to predict, every
        # time a random string is required. This may change the
        # properties of the chosen random sequence slightly, but this
        # is better than absolute predictability.
        random.seed(
            hashlib.sha256(
                ("%s%s%s" % (
                    random.getstate(),
                    time.time(),
                    settings.SECRET_KEY)).encode('utf-8')
                ).digest())
    return ''.join([random.choice(allowed_chars) for i in range(length)])

################################

print('\n')
print(get_random_string(50, 'abcdefghijklmnopqrstuvwxyz' 
                            'ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789' 
                            '*+%'))
print('\n')
