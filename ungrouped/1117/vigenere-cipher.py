encode, decode = "encode", "decode"

def charOffset(char:str, begin:str="A")->int:
    return ord(char) - ord(begin)

def keySelected(pos:int, key:str)->str:
    return key[pos % len(key)]

def pickCharAtABC(pos:int)->str:
    # input: 27 (27th character)
    # returns: 1 (1st character, "B")
    return chr(pos % 26 + ord("A"))

def vigenereCipher(mode:str, text:str, key:str)->str:
    result = ""
    if mode == encode:
        for index in range(0, len(text)):
            result += pickCharAtABC(charOffset(text[index])+charOffset(keySelected(index,key)))
    elif mode == decode:
        for index in range(0, len(text)):
            result += pickCharAtABC(charOffset(text[index])-charOffset(keySelected(index,key)))
    return result

assert(vigenereCipher(encode,"ATTACKATDAWN","LEMON")=="LXFOPVEFRNHR")
assert(vigenereCipher(decode,"LXFOPVEFRNHR","LEMON")=="ATTACKATDAWN")
assert(vigenereCipher(encode,"PYTHONPROGRAMMING","PINEAPPLE")=="EGGLOCECSVZNQMXCR")
assert(vigenereCipher(decode,"EGGLOCECSVZNQMXCR","PINEAPPLE")=="PYTHONPROGRAMMING")

mode = {1:encode, 2:decode}[int(input())]
text = input()
key = input()

print(vigenereCipher(mode,text,key))
