#!/usr/bin/env python

import sys
from email.Header import decode_header

s = decode_header(str(sys.argv[1]))
print( s[0][0].decode('iso-8859-1').encode('utf-8'))
