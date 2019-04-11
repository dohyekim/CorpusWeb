import difflib


text1 = """Lorem ipsum dolor sit amet, consectetuer adipiscing elit. Integer
eu lacus accumsan arcu fermentum euismod. Donec pulvinar porttitor
tellus. Aliquam venenatis. Donec facilisis pharetra tortor.  In nec
mauris eget magna consequat convallis. Nam sed sem vitae odio
pellentesque interdum. Sed consequat viverra nisl. Suspendisse arcu
metus, blandit quis, rhoncus ac, pharetra eget, velit. Mauris
urna. Morbi nonummy molestie orci. Praesent nisi elit, fringilla ac,
suscipit non, tristique vel, mauris. Curabitur vel lorem id nisl porta
adipiscing. Suspendisse eu lectus. In nunc. Duis vulputate tristique
enim. Donec quis lectus a justo imperdiet tempus."""

text1_lines = text1.splitlines()
# print(text1_lines) #list

text2 = """Lorem ipsum dolor sit amet, consectetuer adipiscing elit. Integer
eu lacus accumsan arcu fermentum euismod. Donec pulvinar, porttitor
tellus. Aliquam venenatis. Donec facilisis pharetra tortor. In nec
mauris eget magna consequat convallis. Nam cras vitae mi vitae odio
pellentesque interdum. Sed consequat viverra nisl. Suspendisse arcu
metus, blandit quis, rhoncus ac, pharetra eget, velit. Mauris
urna. Morbi nonummy molestie orci. Praesent nisi elit, fringilla ac,
suscipit non, tristique vel, mauris. Curabitur vel lorem id nisl porta
adipiscing. Duis vulputate tristique enim. Donec quis lectus a justo
imperdiet tempus. Suspendisse eu lectus. In nunc. """
text2_lines = text2.splitlines()

d = difflib.Differ()
diff = d.compare(text1_lines, text2_lines)

# print("diff>>>>>>", diff) # 주소값
# print("\n\n\n\n\n")
# print ('diff 1>>>>>>>>>\n'.join(diff))

# diff2 = difflib.ndiff(text1_lines, text2_lines)
# print ('\ndiff2>>>>>>>>>>>>>>>>>>\n'.join(diff2), "\n")
# print("\n\n\n\n\n")
    
# print ('type of diff2>>>>>>>>>>>>>>>>>>>>>>>>\n'.join(list(diff2)))


# # 빠진 것과 더해진 것들을 한 번에
# diff3 = difflib.unified_diff(text1_lines, text2_lines, lineterm='')
# print ('\n diff3>>>>>>>>\n'.join(list(diff3)))

# # 빠진 것과 더해진 것들을 두 개로 나눠서
# diff4 = difflib.unified_diff(text1_lines, text2_lines, lineterm='')
# print('\n'.join(list(diff4)))

# # HTML Table로
# d = difflib.HtmlDiff()
# print("\n html >>>>> \n",d.make_table(text1_lines, text2_lines))


d2 = difflib.HtmlDiff()
print("\n html >>>>> \n",d2.make_file(text1_lines, text2_lines))
    

