def ranstr(strlen, usenum, uselet, usespec, usecaplet):
    import random
    try:
        if strlen == None:
            strlen = 10
        if usenum == None:
            usenum = True
        if uselet == None:
            uselet = True
        if usespec == None:
            usespec = True
        if usecaplet == None:
            usecaplet = True
        else:
            pass
        lset = []
        c = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z"]
        s = ["~", "`", "!", "@", "#", "$", "%", "^", "&", "*", "(", ")", "-", "_", "+", "=", "|", "\\", "{", "}", "[", "]", ":", ";", ",", "<", ">", ".", "?", "/", "'", '"']
        n = ["0","1","2","3","4","5","6","7","8","9"]
        l = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z"]
        if usenum == True:
            lset += n
        if uselet == True:
            lset += l
        if usespec == True:
            lset += s
        if usecaplet == True:
            lset += c
        ranmsg = ""
        for _ in range(strlen):
            ranmsg += random.choice(lset)
        return ranmsg
        
    except TypeError:
        pass