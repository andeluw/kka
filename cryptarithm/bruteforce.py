from itertools import permutations
import time
import tracemalloc

# Split equation menjadi tuple
def splitEquation(equation):
    return tuple(equation.upper().split())

# Mendapatkan huruf unik dari equation
def extractUniqueLetters(equation):
    return [i for i in set(''.join(splitEquation(equation))) if i.isalpha()]

# Mengubah kata menjadi angka berdasarkan assignment
def wordToNumber(word, assignment):
    return int(''.join(str(assignment[letter]) for letter in word))

# Function to validate if the current digit assignment is correct
def validateValues(assignment, equation):
    operand1, operator, operand2, equals, result = splitEquation(equation)
    
    if (assignment[operand1[0]] == 0 or 
        assignment[operand2[0]] == 0 or 
        assignment[result[0]] == 0):
        return False

    if all(letter in assignment or not letter.isalpha() for letter in operand1 + operand2 + result):
        num1 = wordToNumber(operand1, assignment)
        num2 = wordToNumber(operand2, assignment)
        finalRes = wordToNumber(result, assignment)

        # print(f"Percobaan: {num1} {operator} {num2} = {finalRes}")

        if operator == '+':
            return num1 + num2 == finalRes
        elif operator == '-':
            return num1 - num2 == finalRes
        elif operator == '*':
            return num1 * num2 == finalRes
        elif operator == '/':
            return num2 != 0 and num1 / num2 == finalRes  # Avoid division by zero
    return False

def recursiveAssignment(depth, max_depth, currentTuple, uniqueLetters):
    if depth == max_depth:
        assignment = dict(zip(uniqueLetters, currentTuple))
        if validateValues(assignment, problem):
            return assignment
        return None
    
    for i in range(10):
        if currentTuple.count(i) < 1:
            result = recursiveAssignment(depth + 1, max_depth, currentTuple + (i,), uniqueLetters)
            if result is not None:
                return result

def solveBruteForce(equation):
    uniqueLetters = extractUniqueLetters(equation)
    
    # CONSTRAINT: Jumlah huruf unik dalam problem tidak boleh lebih dari 10
    if len(uniqueLetters) > 10:
        print("INVALID: Problem hanya boleh mengandung maksimal 10 huruf yang unik.\n")
        return
    operand1, operator, operand2, equals, result = splitEquation(equation)
    
    print("\nProses pencarian solusi...\n")

    assignment = recursiveAssignment(0, len(uniqueLetters), (), uniqueLetters)
    if assignment:
        print(f"Solusi ditemukan: {assignment}")
        print(f"{wordToNumber(operand1, assignment)} {operator} {wordToNumber(operand2, assignment)} = {wordToNumber(result, assignment)}")
    else:
        print("Tidak ada solusi yang ditemukan.")

def inputFromUser(input_user):
    while True:
        user_input = input(input_user)
        if user_input.isalpha(): 
            return user_input
        else:
            print("Silakan masukkan huruf saja.")

# Input User
op1 = inputFromUser("Masukkan operan pertama: ")
op2 = inputFromUser("Masukkan operan kedua: ")
while True:
    opt = input("Masukkan operator (+, -, *, /): ")
    if opt in ['+', '-', '*', '/']:
        break
    else:
        print("Operator yang dimasukkan tidak valid.")
res = inputFromUser("Masukkan hasil: ")
problem = f"{op1} {opt} {op2} = {res}"

if problem:
    tracemalloc.start()
    start_time = time.time()
    solveBruteForce(problem)
    end_time = time.time()
    memory_usage, _ = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    print(f"Runtime : {end_time - start_time: .4f} seconds")
    print(f"Memory Usage : {memory_usage / 1024: .2f} KB")
