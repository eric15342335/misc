file = open("pi_million_digits.txt", "r").read()

Q3_out = {}
sequence = ""

for char in file:
    if char in sequence:
        sequence += char
    else:  # put the sequence into the dict
        # workaround for initially sequence being empty
        if sequence:
            Q3_out[sequence] = Q3_out.setdefault(sequence, 0) + 1
        sequence = char

print(Q3_out)
