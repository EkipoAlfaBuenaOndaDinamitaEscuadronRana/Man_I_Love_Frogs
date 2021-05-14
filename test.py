def is_operator(symbol):
    return symbol in [
        "+", "-", "*", "/", "%", "(", ")", ">", "<", "=", "|", "&", "!"
    ]

def divide_expression(expression):
    exp = []
    operand = ""
    i = 0

    while i < len(expression):
        symbol = expression[i]

        if is_operator(symbol):
            if len(operand):
                exp.append(operand)

            if symbol in ["<", ">", "=", "!"] and expression[i + 1] == "=":
                symbol += "="
                i += 1

            elif symbol in ["|", "&"] and expression[i + 1] == symbol:
                symbol += symbol
                i += 1

            exp.append(symbol)
            operand = ""

        else:
            operand += expression[i]

        i += 1

    if len(operand):
        exp.append(operand)

    return exp

print(divide_expression("A = B + C"))