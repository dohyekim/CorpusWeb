import re

string = 'asejltase. faejta;et. faljet;akejtak.'
aaa = re.compile('\.\s')
bbb = re.sub(aaa, '\n', string)
print(string)

print(bbb)