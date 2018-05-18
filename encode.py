#!/usr/bin/python
import urllib
import re

chara = 'A+%C3%A2%C2%80%C2%93+A'

encode = urllib.unquote_plus(chara)#.decode('utf8', 'ignore')
p = re.sub('<[^<]+?>', '', encode)
print p
