import re
word = "b>15551.5"

word = re.sub(r'\b[^\d\W]+\b>', '', word)

print(word)