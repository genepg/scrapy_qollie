# -*- encoding: utf-8 -*-
import re

print ("--------\n")

pattern = re.compile(r'\w+')
string = "台積電(台基)"
match = re.search(pattern, string )
print(match.group())
