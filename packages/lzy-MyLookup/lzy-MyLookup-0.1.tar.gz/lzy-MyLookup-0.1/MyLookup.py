def MyLookup(*args):
    l = []
    for k in args[0]:
        if k:
            for v in args[1]:
                if k in v:
                    l.append(v)
        else:
            l.append([])
    for n in range(len(args[0])):
        if args[0][n] and args[0][n] not in l[n]:
            l.insert(n,[])
    return l