import os
def simplify(str):
    try:
        before = str
        after = ""
        while (True):
            tmp = list(parenthetic_contents(before))
            rep=""
            for (l,c) in tmp:
                if chk_NOT(c):
                    rep = c         
                    break
            after = before.replace(rep,"")
            #after = after.replace("()","")
            if before!=after:
                return after
            if before == after:
                return before
    except:
        return "error"

def chk_NOT(str):
    arr = [ i.strip() for  i in str.split("NOT") ] 
    if len(arr)!=2:
        return False
    else:
        return all(elem == arr[0] for elem in arr)

def parenthetic_contents(string):
    """Generate parenthesized contents in string as pairs (level, contents)."""
    stack = []
    for i, c in enumerate(string):
        if c == '(':
            stack.append(i)
        elif c == ')' and stack:
            start = stack.pop()
            yield (len(stack), string[start + 1: i])

if __name__ == '__main__':

    str= input("pls input string: ") # "(((A or B) or ((A AND D) NOT (A AND D))) NOT C)"  #list(parenthetic_contents(str))
    print("Output:/n")
    print( simplify(str))
    print("")
    os.system("pause")
