import re

def diff(html):
    pattern = re.compile('\.\s')
    aa = re.sub(pattern, '.\n', html)
    xx = aa.split("\n")
    yy = []
    for h in xx:
        if len(h)>= 200 and len(h)<400:
            idx = h.find(',', 100)
            # print(idx)
            if idx != -1 and idx <200:
                idx = h.find(',',100)
                h_1 = h[0:idx+1]
                h_2 = h[idx+1:]

            else:
                idx = h.find(' ', 100)
                h_1 = h[0:idx+1]
                h_2 = h[idx+1:]
            # print(len(h_1))
            # print(len(h_2))
            yy.append(h_1)
            yy.append(h_2)
        else:
            yy.append(h)
    # print(yy)
    return yy
