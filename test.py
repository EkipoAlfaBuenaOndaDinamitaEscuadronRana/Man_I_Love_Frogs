def divide_expression(expression):
    exp = []
    operand = ""
    i = 0;

    while i < len(expression):
        if expression[i] in ["+", "-", "*", "/", "%", "(", ")", ">", "<", "=","|", "&", "!"]:
            if len(operand):
                exp.append(operand)

            symbol = expression[i]

            if symbol in ["<", ">", "=", "!"] and expression[i + 1] == "=":
                symbol += "="
                i += 1

            elif symbol == "|" and expression[i + 1] == "|":
                symbol += "|"
                i += 1

            elif symbol == "&" and expression[i + 1] == "&":
                symbol += "&"
                i += 1

            exp.append(symbol)
            operand = ""

        else:
            operand += expression[i]

        i += 1

    if len(operand):
        exp.append(operand)

    return exp


print(divide_expression("!A || B"))
