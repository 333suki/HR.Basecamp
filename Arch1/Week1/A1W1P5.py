numbers = input("")
sum = 0
#3141 = 9

for i in range(len(numbers)):
    #sum = sum + int(numbers[i])
    sum += int(numbers[i])

print(f"{numbers[0]}+{numbers[1]}+{numbers[2]}+{numbers[3]}={sum}")

#f(string) leest de accolade({}) in de string in plaats van het uit te printen als een string.
