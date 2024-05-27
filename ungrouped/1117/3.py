train_type, train_num = input(), int(input())

"""empirical formula:
1. each train is 7 units long
2. n trains need n-1 connectors
3. first and last train both need one "[" "]" protective layer
"""
overall_length = train_num*7 + (train_num-1) + 2

first_line = ["-"]*overall_length    # list*int: repeat list int times

# replace "-" with "H" or "T" according to the train type
if train_type == "D":   # D stands for "Diesel"
    first_line[2] = "H"

elif train_type == "E": # E stands for "Electric"
    for i in range(1, train_num-1, 2):    # note that i starts from 1 as the second train is located at index 8*1
        # so as train_num need subtract by 1
        """
        each train 7 units long + one "[" or connector
        8*i+3: 8 units per train + "T" is located at the 3rd unit
        -1: list index starts from 0
        """
        first_line[(8*i+3) - 1] = "T"


second_line = ["#"]*overall_length

# replace "#" with "[", "]", or "-"
second_line[0] = "["
second_line[-1] = "]"
for i in range(1, train_num):
    second_line[8*i] = "-"

third_line = ["_"]*overall_length

"""
replace "_" with wheels "o"
if each train has 8 units, e.g. "[#######" as one train, then
wheels are located at each train's 2-3 and 7-8 unit
"""
for i in range(0, train_num):   # note that i starts from 0
    third_line[8*i+2 -1] = "o"
    third_line[8*i+3 -1] = "o"
    third_line[8*i+7 -1] = "o"
    third_line[8*i+8 -1] = "o"

print("".join(first_line))
print("".join(second_line))
print("".join(third_line))
