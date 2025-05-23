def explain_steps(expr):
    steps = []
    if "+" in expr:
        a, b = expr.split("+")
        steps.append(f"Step 1: Add {a} and {b}")
        steps.append(f"Final Answer: {int(a) + int(b)}")
    elif "*" in expr:
        a, b = expr.split("*")
        steps.append(f"Step 1: Multiply {a} and {b}")
        steps.append(f"Final Answer: {int(a) * int(b)}")
    else:
        steps.append("Sorry, no explain mode for this expression.")
    return steps
