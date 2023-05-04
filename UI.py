str = "ROLL- 202132124 2009 Name - Samruddhi Q   5) =) 1 Natural language Q processing is subfield of. Q    2) => This create HTML, CSs."

questions = {}
index = 1

for i in range(len(str) - 1):
    if str[i] == 'Q':
        i+=1
        while(str[i] == ' '):
            i += 1
        if str[i].isdigit():
            index = str[i]
            i += 1
            j = i
            temp_str = ''
            while(str[j] != 'Q'):
                if j+1 == len(str):
                    break
                temp_str += str[j]
                j += 1
            questions[index] = temp_str

print(questions)

