import re

# Check if input is a simple interest question
def is_interest_query(text):
    return "interest" in text.lower() and "on" in text.lower() and "%" in text.lower()

# Extract numbers and calculate simple interest with steps
def parse_interest_query(query):
    try:
        query = query.lower()
        principal = float(re.search(r'on\s+(\d+)', query).group(1))
        rate = float(re.search(r'at\s+(\d+)%', query).group(1))
        time = float(re.search(r'for\s+(\d+)', query).group(1))

        si = (principal * rate * time) / 100

        answer = f"The simple interest is {si} rupees."
        steps = f"Steps:\n1. Principal (P) = {principal}\n2. Rate (R) = {rate}%\n3. Time (T) = {time} years\n4. Formula: SI = (P × R × T) / 100\n5. Calculation: ({principal} × {rate} × {time}) / 100 = {si}"
        return answer, steps
    except Exception:
        return "Sorry, I couldn't understand the interest calculation.", ""

# Convert voice commands to math expression
def voice_to_expression(text):
    text = text.lower()
    text = text.replace("plus", "+")
    text = text.replace("minus", "-")
    text = text.replace("into", "*")
    text = text.replace("times", "*")
    text = text.replace("multiplied by", "*")
    text = text.replace("x", "*")
    text = text.replace("divided by", "/")
    text = text.replace("by", "/")
    text = text.replace("mod", "%")
    # Keep digits and operators only
    text = re.sub(r"[^0-9+\-*/().%]", "", text)
    return text

# Calculate math expression with steps (simple version)
def calculate_expression(expr):
    try:
        result = eval(expr)
        answer = f"The answer is {result}"
        steps = f"Evaluated the expression: {expr} = {result}"
        return answer, steps
    except Exception:
        return "Sorry, I couldn't calculate that expression.", ""

# Main parser function returning answer and steps
def get_response(text):
    if is_interest_query(text):
        return parse_interest_query(text)
    else:
        expr = voice_to_expression(text)
        return calculate_expression(expr)

# Alias for compatibility
def parse_command(text):
    return get_response(text)
