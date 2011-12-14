fi = open("analysis.txt", "r")
fo = open("analysis_1.txt", "w")

for entry in fi.readlines():
    mark_paren = False
    for i in entry:
        if i=='(':
            if mark_paren:
                continue
            mark_paren = True
        elif i==')':
            if not mark_paren:
                continue
            mark_paren = False
        elif i==',' and not mark_paren:
            i= ' '
        elif i==' ' and mark_paren:
            continue
        fo.write(i)
