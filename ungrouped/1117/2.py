def encrypt(char:str, key1, key2:int) -> str:
    int_rep = {'A':0, 'B':1, 'C':2, 'D':3, 'E':4, 'F':5, 'G':6, 'H':7, 'I':8, 'J':9, 'K':10, 'L':11, 'M':12, 'N':13, 'O':14, 'P':15, 'Q':16, 'R':17, 'S':18, 'T':19, 'U':20, 'V':21, 'W':22, 'X':23, 'Y':24, 'Z':25}
    low_case = char.islower()
    char = char.upper()
    _char_int = (int_rep[char]*key1+key2)%26
    # find keys by values
    # if _char_int is 2, it will be ['A','B','C', ...][[0,1,2,...][2]]
    _char = list(int_rep.keys())[list(int_rep.values()).index(_char_int)]
    if low_case:
        _char = _char.lower()
    return _char

string, firstkey, secondkey = input(), int(input()), int(input())

for character in string:
    # is a character
    if character.isalpha():
        print(encrypt(character, firstkey, secondkey), end='')
    else:
        print(character, end='')

