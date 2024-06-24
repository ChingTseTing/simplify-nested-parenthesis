import os
import re
def parenthetic_contents(string):
    """Generate parenthesized contents in string as pairs (level, contents)."""
    stack = []
    for i, c in enumerate(string):
        if c == '(':
            stack.append(i)
        elif c == ')' and stack:
            start = stack.pop()
            yield (len(stack), string[start + 1: i])
def unnest_single(str):
    if str[0]=="(" and str[-1]==")":
            tmp = list(parenthetic_contents(str)) #  "((((A NOT B) OR C)))"  # ((A NOT B) OR C) NOT ((((A NOT B) OR C)))    # 
            tmp.sort( )
            flag=0        
            for  i in range(len(tmp)-1,0,-1):
                if "("+tmp[i][1]+")"== tmp[i-1][1]:
                    flag=1
                    return ("("+tmp[i][1]+")")
            if flag==0:    
                obj= [ i for i in re.split(r'[(|)]', str) if i != '' and "AND" not in i and "NOT" not in i and "OR" not in i and "INTERACT" not in i and "NULL" not in i ]
                if len(obj)==1:
                    return obj[0]
                else:
                    return str
    else:
        return str

def UNNEST(str):
    before=str
    after=""
    flag=True
    while (flag):
        tmp = list(parenthetic_contents(before))
        rep=""
        for (l,c) in tmp:
            c = "("+c+")"
            if  c!=unnest_single(c) :
                rep = c   
                break
        if rep!="":
            after = before.replace(rep,unnest_single(rep))
        else:
            after=before
        if len(after)<len(before):
            before=after
        else:
            return after


def CHK_NULL(str):
    before=str
    after=""
    flag=True
    while (flag):
        tmp = list(parenthetic_contents(before))
        rep=""
        torep=""
        for (l,c) in tmp:
            a,b=chk_null(c) 
            if  a==True:
                rep=c
                torep=b
                break
        if rep!="":
            after = before.replace(rep,torep)
        else:
            after=before
        if len(after)<len(before):
            before=after
        else:
            return after

def chk_null(str):
    '''
    RULE : AND OR INTERACT NOT operation of NULL 
    ((A NOT B) OR C) NOT (NULL)      --> ((A NOT B) OR C)
    ((A NOT B) OR C) OR (NULL)       --> ((A NOT B) OR C)
    ((A NOT B) OR C) INTERACT (NULL) --> (NULL)
    (NULL) OR ((A NOT B) OR C)       --> ((A NOT B) OR C)
    (NULL) NOT ((A NOT B) OR C)      --> (NULL)
    (NULL) AND ((A NOT B) OR C)      --> (NULL)
    (NULL) INTERACT ((A NOT B) OR C) --> (NULL)
    ((A NOT B) OR C) AND (NULL)      --> (NULL)
    (NULL) AND (NULL)                --> (NULL)
    (NULL) OR (NULL)                 --> (NULL)
    (NULL) NOT (NULL)                --> (NULL)
    (NULL) INTERACT (NULL)           --> (NULL)
    '''
    if "(NULL)" in str:
        tmp= [ "("+v+")" for (i,v)  in list(parenthetic_contents(str)) if i==0]
        if len(  tmp)==2:
            if tmp[0]=="(NULL)" and tmp[1]!="(NULL)": #(NULL)在前
                if str ==" AND ".join(tmp):
                    return True,"(NULL)"
                elif str ==" OR ".join(tmp):
                    return True, tmp[1]
                elif str ==" NOT ".join(tmp):
                    return True, "(NULL)" 
                elif str ==" INTERACT ".join(tmp):
                    return True,"(NULL)"
                else:
                    return False, str
            elif tmp[0]!="(NULL)" and tmp[1]=="(NULL)":#(NULL)在後
                if str ==" AND ".join(tmp):
                    return True,"(NULL)"
                elif str ==" OR ".join(tmp):
                    return True, tmp[0]
                elif str ==" NOT ".join(tmp):
                    return True, tmp[0]
                elif str ==" INTERACT ".join(tmp):
                    return True, "(NULL)"
                else:
                    return False, str   
            elif tmp[0]=="(NULL)" and tmp[1]=="(NULL)":
                return True, "(NULL)"
            else:
                return False, str
        elif len(  tmp)==1 and tmp==['(NULL)']  and str!="(NULL)":     
            tmp2 = str.split(" ")
            if tmp2[0]=="(NULL)" and tmp2[2]!="(NULL)": #(NULL)在前
                if tmp2[1] =="AND":
                    return True,"(NULL)"
                elif tmp2[1] =="OR":
                    return True, tmp2[2]
                elif  tmp2[1] =="NOT":
                    return True, "(NULL)"
                elif  tmp2[1] =="INTERACT":
                    return True,"(NULL)"
                else:
                    return False, str
            elif tmp2[0]!="(NULL)" and tmp2[2]=="(NULL)":#(NULL)在後
                if  tmp2[1] =="AND":
                    return True,"(NULL)"
                elif  tmp2[1] =="OR":
                    return True, tmp2[0]
                elif  tmp2[1] =="NOT":
                    return True, tmp2[0]
                elif  tmp2[1] =="INTERACT":
                    return True, "(NULL)"
                else:
                    return False, str
            elif tmp2[0]=="(NULL)" and tmp2[1]=="(NULL)":
                return True, "(NULL)"
            else:
                return False, str
        else:
            return False, str
    else:
        return False, str



def chk_NOT(str):
    '''
    Rule
    (A) NOT (A) -->NULL
    A NOT A --> NULL
    (A AND (B NOT C)) NOT (A AND (B NOT C)) --NULL
    NOT (A AND (B OR C))--> NULL
    NOT A --> NULL
    NOT (A) --> NULL
    (A AND (B OR C)) NOT --> (A AND (B OR C))
    A NOT --> A
    (A) NOT --> (A)
    (A AND (B NOT C)) NOT (A AND (B NOT D)) --> (A AND (B NOT C)) NOT (A AND (B NOT D))
    A NOT B --> A NOT B
    A --> A 
    NULL--> NULL
    NOT-->NOT
    (NULL)--> (NULL)
    (NOT)-->(NOT)
    '''
    if str=="NOT" or str=="NULL"  or str=="(NOT)"  or str=="(NULL)":
        return  str
    elif list(parenthetic_contents(str)) !=[]:
        tmp = [ "("+v+")" for (i,v)  in list(parenthetic_contents(str)) if i==0]
        if all(elem == tmp[0] for elem in tmp) and  str.split(tmp[0])==['', ' NOT ', '']:
            return  "(NULL)"
        elif len(tmp)==1 and  str.split(tmp[0])==['NOT ', '']:
            return  "(NULL)"
        elif len(tmp)==1 and  str.split(tmp[0])==['', ' NOT']:
            return  tmp[0]
        else:
            return  str
    else:
        arr = [ i.strip()  for  i in str.split("NOT") ]  
        if len(arr)!=2:
            return  str
        elif len(arr)==2 and arr[0]=="":
            return  "(NULL)"
        elif len(arr)==2 and arr[1]=="":
            return  arr[0]
        elif len(arr)==2 and len(set( arr ))==1: 
            return "(NULL)"
        elif len(arr)==2 and arr[0]!="" and arr[0]!="" :
            return str
        else:
            return str
            
def CHK_NOT(str):
    before=str
    after=""
    flag=True
    while (flag):
        tmp = list(parenthetic_contents(before))
        rep=""
        dorep=""
        for (l,c) in tmp:
          #  c = "("+c+")"
            if  chk_NOT(c)!=c:
                #rep = c   
                rep = "("+ c +")"
                dorep=chk_NOT(c)
                break
        if rep!="":
            after = before.replace(rep,dorep)
        else:
            after=before
        if len(after)<len(before):
            before=after
        else:
            return after

def bracket_nospa(str):
    before=str
    after=""
    while (True):
        for i in range(10):
            before = before.replace("( (","((")
            before = before.replace(") )","))")
        before = before.replace("(  (","((")        
        after = before.replace(")  )","))")
    if len(after)<len(before):
        before=after
    else:
        return after

def main(str):
    before=str
    before = before.replace("SIZING 0","")
    before = bracket_nospa(before)
    before = UNNEST(before)
    before = bracket_nospa(before)        
    while(True):
        tmp = len(before)
        before = CHK_NOT(before)
        before = bracket_nospa(before)
        before = UNNEST(before)
        before = bracket_nospa(before)
        before = UNNEST(before)

        before = CHK_NULL(before)
        before = bracket_nospa(before)
        before = UNNEST(before)
        before = bracket_nospa(before)
        after = UNNEST(before)

        if len(after)<tmp:
            before=after
        else:
            return after



if __name__ == '__main__':

    str2 ="Y"

    while str2=="Y":
        print("PLS input LOP for simplify")
        print( " ")
        str = input(">> ")
        print( " ")
        print( "Output:")
        print( " ")
        print( main(str) )
        print( " ")
        print("Simplify another LOP ? (Y/N)")
        print( " ")
        str2 = input(">> ")





