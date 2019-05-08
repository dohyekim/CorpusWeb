    # def diff(html):
    #     pattern = re.compile('\.\s')
    #     aa = re.sub(pattern, '.\n', html)
    #     xx = aa.split("\n")
    #     yy = []
    #     for h in xx:
    #         if len(h)>= 200 and len(h)<400:
    #             idx = max((h.index(',')))
    #             if idx == None:
    #                 h_1 = h[0:199]
    #                 h_2 = h[199:]
    #             else:
    #                 h_1 = h[0:idx+1]
    #                 h_2 = h[idx+1:]
    #             yy.append(h_1)
    #             yy.append(h_2)
    #         else:
    #             yy.append(h)
    #     return yy