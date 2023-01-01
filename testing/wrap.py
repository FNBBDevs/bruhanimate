import time
import os


def print_buf(buff):
    print(f"+{'-'*(len(buff[0]) * 2 + 1)}+")
    for row in buff:
        print("| ", end="")
        print(" ".join(row), end=" ")
        print("|", end="")
        print()
    print(f"+{'-'*(len(buff[0]) * 2 + 1)}+")



output = [["-" for _ in range(10)] for __ in range(10)]
output[4][0] = ">"
output[4][1] = ">"
output[4][2] = ">"
output[5][1] = ">"
output[5][2] = ">"
output[5][3] = ">"
output[6][2] = ">"
output[6][3] = ">"
output[6][4] = ">"

buffer = [[" " for _ in range(10)] for __ in range(10)]

shift = -1

os.system("cls")
while True:
    time.sleep(0.05)
    os.system("cls")
    for _ in range(10):
        output[_] = output[_][shift:] + output[_][:shift]
    
    for row in output:
        print(f"| {''.join(row)} |")
    
