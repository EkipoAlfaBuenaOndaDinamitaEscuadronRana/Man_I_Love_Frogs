
from file_parser import parser_file

def test_file(file_name, answer):
    result = parser_file(file_name)
    if result == answer:
        return "."
    else:
        return "F"
        
test_answers =[
"NO EXISTE",
"01 | ENDOF - - -\n",
"01 | ENDOF - - -\n02 | EQ 1 - a\n03 | ENDOF - - -\n",
"NOT READY",
"01 | ENDOF - - -\n02 | EQ 1 - a\n03 | ENDOF - - -\n04 | EQ 10 - x\n05 | EQ 2 - y\n06 | MUL x y T6\n07 | EQ T6 - a\n08 | ADD x y T8\n09 | EQ T8 - b\n10 | DIV x y T10\n11 | EQ T10 - c\n12 | SUB x y T12\n13 | EQ T12 - d\n14 | ENDOF - - -\n",
"01 | ENDOF - - -\n02 | EQ 1 - a\n03 | ENDOF - - -\n04 | EQ 10 - x\n05 | EQ 2 - y\n06 | MUL x y T6\n07 | EQ T6 - a\n08 | ADD x y T8\n09 | EQ T8 - b\n10 | DIV x y T10\n11 | EQ T10 - c\n12 | SUB x y T12\n13 | EQ T12 - d\n14 | ENDOF - - -\n15 | EQ 1 - a\n16 | EQ 2 - b\n17 | EQ 0 - c\n18 | GT a b T18\n19 | GOTOF T18 - 23\n20 | ADD a 1 T20\n21 | EQ T20 - c\n22 | GOTO - - 30\n23 | BEQ b a T23\n24 | GOTOF T23 - 28\n25 | ADD b 1 T25\n26 | EQ T25 - c\n27 | GOTO - - 30\n28 | ADD 1 2 T28\n29 | EQ T28 - c\n30 | ENDOF - - -\n",
"01 | ENDOF - - -\n02 | EQ 1 - a\n03 | ENDOF - - -\n04 | EQ 10 - x\n05 | EQ 2 - y\n06 | MUL x y T6\n07 | EQ T6 - a\n08 | ADD x y T8\n09 | EQ T8 - b\n10 | DIV x y T10\n11 | EQ T10 - c\n12 | SUB x y T12\n13 | EQ T12 - d\n14 | ENDOF - - -\n15 | EQ 1 - a\n16 | EQ 2 - b\n17 | EQ 0 - c\n18 | GT a b T18\n19 | GOTOF T18 - 23\n20 | ADD a 1 T20\n21 | EQ T20 - c\n22 | GOTO - - 30\n23 | BEQ b a T23\n24 | GOTOF T23 - 28\n25 | ADD b 1 T25\n26 | EQ T25 - c\n27 | GOTO - - 30\n28 | ADD 1 2 T28\n29 | EQ T28 - c\n30 | ENDOF - - -\n31 | EQ 1 - a\n32 | EQ 2 - b\n33 | EQ 0 - c\n34 | GT a b T34\n35 | GOTOF T34 - 39\n36 | ADD a b T36\n37 | EQ T36 - c\n38 | GOTO - - 34\n39 | ENDOF - - -\n",
"01 | ENDOF - - -\n02 | EQ 1 - a\n03 | ENDOF - - -\n04 | EQ 10 - x\n05 | EQ 2 - y\n06 | MUL x y T6\n07 | EQ T6 - a\n08 | ADD x y T8\n09 | EQ T8 - b\n10 | DIV x y T10\n11 | EQ T10 - c\n12 | SUB x y T12\n13 | EQ T12 - d\n14 | ENDOF - - -\n15 | EQ 1 - a\n16 | EQ 2 - b\n17 | EQ 0 - c\n18 | GT a b T18\n19 | GOTOF T18 - 23\n20 | ADD a 1 T20\n21 | EQ T20 - c\n22 | GOTO - - 30\n23 | BEQ b a T23\n24 | GOTOF T23 - 28\n25 | ADD b 1 T25\n26 | EQ T25 - c\n27 | GOTO - - 30\n28 | ADD 1 2 T28\n29 | EQ T28 - c\n30 | ENDOF - - -\n31 | EQ 1 - a\n32 | EQ 2 - b\n33 | EQ 0 - c\n34 | GT a b T34\n35 | GOTOF T34 - 39\n36 | ADD a b T36\n37 | EQ T36 - c\n38 | GOTO - - 34\n39 | ENDOF - - -\n40 | EQ 10 - b\n41 | EQ 0 - c\n42 | EQ 0 - a\n43 | LT a b T43\n44 | GOTOF T43 - 50\n45 | ADD a 1 T45\n46 | EQ T45 - a\n47 | ADD c 1 T47\n48 | EQ T47 - c\n49 | GOTO - - 43\n50 | ADD b c T50\n51 | EQ T50 - b\n52 | ENDOF - - -\n"
]

test_results =[]

'''
Test 1 -> Correcto
Solo es header de programa
Yacc 0 probelmas 
'''
test_results.append(test_file("tests/test_1.txt", test_answers[1]))

'''
Test 2 -> Correcto
Header + una suma
Yacc 0 problems 
'''
test_results.append(test_file("tests/test_2.txt", test_answers[2]))

'''
Test 3 -> Correcto 
Variables Globales, Función, if
Yacc 0 problems 
Quads -> Pendiente
'''
# Pendiente
# test_results.append(test_file("tests/test_3.txt", test_answers[3]))

'''
Test 4 -> Correcto 
Variables y expresiones
Yacc 0 problems 
'''
test_results.append(test_file("tests/test_4.txt", test_answers[4]))


'''
Test 5 -> Correcto 
if else if else
Yacc 0 problems 
'''
test_results.append(test_file("tests/test_5.txt", test_answers[5]))


'''
Test 6 -> Correcto 
while
Yacc 0 problems 
'''
test_results.append(test_file("tests/test_6.txt", test_answers[6]))

'''
Test 7 -> Correcto 
for
Yacc 0 problems 
'''
test_results.append(test_file("tests/test_7.txt", test_answers[7]))

'''
Test 8 -> Todavía no funcionan los quads 
for simple 
Yacc 0 problems 
Quads -> nop 
'''
# Pendiente
# test_results.append(test_file("tests/test_8.txt", test_answers[8]))

print(test_results)