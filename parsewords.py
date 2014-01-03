f = open('/usr/share/dict/words','r')
words = []
for line in f:
  word = line.rstrip().decode('utf-8')
  if (not "'" in word):
    words.append(word)

import codecs
f = codecs.open('words.txt','w','utf-8')
for word in words:
  f.write(word+'\n')
