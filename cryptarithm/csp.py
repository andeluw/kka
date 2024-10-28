# Split equation menjadi tuple
def splitEquation(equation):
    return tuple(equation.upper().split())

# Mendapatkan huruf unik dari equation
def extractUniqueLetters(equation):
    return [i for i in set(''.join(splitEquation(equation))) if i.isalpha()]

# Mendapatkan huruf pertama dari setiap kata
def startingLetters(equation, letters):
    parts = splitEquation(equation)
    return [letters[i] for i in range(len(letters)) if letters[i] in [part[0] for part in parts if part.isalpha()]]

# Cek apakah assignment valid
def validateValues(assignment, equation):
    operand1, operator, operand2, equals, result = splitEquation(equation)
    
    # Jika semua huruf dalam operand1, operand2, dan result sudah di-assign
    if all(letter in assignment or not letter.isalpha() for letter in operand1 + operand2 + result):
        num1 = int("".join(str(assignment.get(letter)) for letter in operand1))
        num2 = int("".join(str(assignment.get(letter)) for letter in operand2))
        finalRes = int("".join(str(assignment.get(letter)) for letter in result))

        # print(f"Percobaan: {num1} {operator} {num2} = {finalRes}")

        if(operator == '+'):
            return num1 + num2 == finalRes
        elif(operator == '-'):
            return num1 - num2 == finalRes
        elif(operator == '*'):
            return num1 * num2 == finalRes
        elif(operator == '/'):
            return num1 / num2 == finalRes
    return False

# SELECT-UNASSIGNED-VARIABLE
def selectUnassignedVariable(assignment, letters, domains):
    unassigned = [v for v in letters if v not in assignment]
    if not unassigned:
        return None
    
    # Minimum Remaining Values
    unassigned.sort(key=lambda var: len(domains[var]))

    # Most Constraining Variable, jika ada 1 atau lebih variabel dengan nilai MRV yang sama
    least_mrv_vars = [
        var for var in unassigned
        if len(domains[var]) == len(domains[unassigned[0]])
    ]

    # Hitung degree dari setiap variabel di least_mrv_vars
    degrees = [
        len([v for v in unassigned if v != var])
        for var in least_mrv_vars
    ]
    maxDegree = max(degrees)
    
    for var in unassigned:
        connections = len([v for v in unassigned if v != var])
        if connections == maxDegree:
            selected_var = var
    
    return selected_var

# Backtracking search
def backtrack(assignment, variables, domains, equation):
    if len(assignment) == len(variables):
        if validateValues(assignment, equation):
            return assignment
        else:
            return None

    var = selectUnassignedVariable(assignment, variables, domains)
    for value in domains[var]:
        if value not in assignment.values():
            # CONSTRAINT: Angka pertama dari setiap kata tidak boleh bernilai 0
            if var in startingLetters(equation, variables) and value == '0':
                continue
            assignment[var] = value
            
            result = backtrack(assignment, variables, domains, equation)
            if result:
                return result
            del assignment[var]
    
    # Tidak ada solusi
    return None

def solve(equation):
    variables = extractUniqueLetters(equation)

    # CONSTRAINT: Jumlah huruf unik dalam problem tidak boleh lebih dari 10
    if len(variables) > 10:
        print("INVALID: Problem hanya boleh mengandung maksimal 10 huruf yang unik.\n")
        return
    operand1, operator, operand2, equal, result = splitEquation(equation)

    assignment = {}

    # Inisialisasi domain
    domains = {}
    for var in variables:
        domains[var] = list('0123456789')

    print("\nINFORMASI AWAL CSP")
    print(f"Variabel CSP: {variables}")
    print(f"Domain CSP:")
    for var in variables:
        print(f"{var}: {domains[var]}")

    print("\nProses pencarian solusi...\n")

    # Backtracking search
    assignment = backtrack(assignment, variables, domains, equation)

    print("HASIL SOLUSI")
    print("Persamaan yang diinputkan:", equation)

    # Jika ada complete assignment yang memenuhi semua constraint
    if assignment:
        print(f"Solusi ditemukan dengan assignment: {assignment}")
        print(f"Hasil akhir: {''.join(str(assignment.get(letter)) for letter in operand1)} {operator} {''.join(str(assignment.get(letter)) for letter in operand2)} = {''.join(str(assignment.get(letter)) for letter in result)}")
    
    # Tidak ada solusi valid yang ditemukan
    else:
        print("No valid solution found for the given equation.\n")

def input_from_user(input_user):
    while True:
        input_user = input(input_user)
        if input_user.isalpha():
            return input_user
        else:
            print("Silakan masukkan huruf saja.")

# Input User
op1 = input_from_user("Masukkan operan pertama: ")
op2 = input_from_user("Masukkan operan kedua: ")
while True:
    opt = input("Masukkan operator (+, -, *, /): ")
    if opt in ['+', '-', '*', '/']:
        break
    else:
        print("Operator yang dimasukkan tidak valid.")
res = input_from_user("Masukkan hasil: ")
problem = f"{op1} {opt} {op2} = {res}"

if problem:
    solve(problem)