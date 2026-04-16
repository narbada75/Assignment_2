import os

# --- Tokenizer ---
def tokenize(expr):
    tokens = []
    i = 0
    n = len(expr)
    while i < n:
        if expr[i].isspace():
            i += 1
            continue
           
        if expr[i].isdigit() or expr[i] == '.':
            start = i
            while i < n and (expr[i].isdigit() or expr[i] == '.'):
                i += 1
            val_str = expr[start:i]
            if val_str == '.': return "ERROR"
           
            # Handle implicit multiplication when a number follows a closing parenthesis
            if tokens and tokens[-1]['type'] in ('RPAREN',):
                tokens.append({'type': 'OP', 'value': '*'})
               
            tokens.append({'type': 'NUM', 'value': val_str})
            continue
           
        if expr[i] in '+-*/':
            tokens.append({'type': 'OP', 'value': expr[i]})
            i += 1
            continue
           
        if expr[i] == '(':
            # Handle implicit multiplication when an opening parenthesis follows a number or closing parenthesis
            if tokens and tokens[-1]['type'] in ('RPAREN', 'NUM'):
                tokens.append({'type': 'OP', 'value': '*'})
               
            tokens.append({'type': 'LPAREN', 'value': '('})
            i += 1
            continue
           
        if expr[i] == ')':
            tokens.append({'type': 'RPAREN', 'value': ')'})
            i += 1
            continue
           
        return "ERROR"
       
    tokens.append({'type': 'END', 'value': ''})
    return tokens

# --- Recursive Descent Parser ---
def parse_factor(state):
    if state['error'] or state['pos'] >= len(state['tokens']):
        state['error'] = True
        return None
       
    tok = state['tokens'][state['pos']]

    if tok['type'] == 'OP' and tok['value'] == '-':
        state['pos'] += 1
        operand = parse_factor(state)
        if state['error']: return None
        return {'type': 'neg', 'operand': operand}
    elif tok['type'] == 'OP' and tok['value'] == '+':
        # Unary + is not supported and produces an error
        state['error'] = True
        return None
    elif tok['type'] == 'NUM':
        state['pos'] += 1
        return {'type': 'num', 'value': tok['value']}
    elif tok['type'] == 'LPAREN':
        state['pos'] += 1
        node = parse_expression(state)
        if state['error'] or state['pos'] >= len(state['tokens']) or state['tokens'][state['pos']]['type'] != 'RPAREN':
            state['error'] = True
            return None
        state['pos'] += 1
        return node
    else:
        state['error'] = True
        return None

def parse_term(state):
    left = parse_factor(state)
    if state['error']: return None
   
    while state['pos'] < len(state['tokens']) and state['tokens'][state['pos']]['type'] == 'OP' and state['tokens'][state['pos']]['value'] in ('*', '/'):
        op = state['tokens'][state['pos']]['value']
        state['pos'] += 1
        right = parse_factor(state)
        if state['error']: return None
        left = {'type': 'binop', 'op': op, 'left': left, 'right': right}
       
    return left

def parse_expression(state):
    left = parse_term(state)
    if state['error']: return None
   
    while state['pos'] < len(state['tokens']) and state['tokens'][state['pos']]['type'] == 'OP' and state['tokens'][state['pos']]['value'] in ('+', '-'):
        op = state['tokens'][state['pos']]['value']
        state['pos'] += 1
        right = parse_term(state)
        if state['error']: return None
        left = {'type': 'binop', 'op': op, 'left': left, 'right': right}
       
    return left

def parse(tokens):
    if tokens == "ERROR":
        return None
    state = {'tokens': tokens, 'pos': 0, 'error': False}
    tree = parse_expression(state)
   
    if state['error'] or state['pos'] >= len(tokens) or tokens[state['pos']]['type'] != 'END':
        return None
    return tree

# --- Evaluator ---
def evaluate_tree(node):
    if node is None: return "ERROR"
    if node['type'] == 'num':
        return float(node['value'])
    elif node['type'] == 'neg':
        val = evaluate_tree(node['operand'])
        if val == "ERROR": return "ERROR"
        return -val
    elif node['type'] == 'binop':
        left_val = evaluate_tree(node['left'])
        right_val = evaluate_tree(node['right'])
        if left_val == "ERROR" or right_val == "ERROR": return "ERROR"
       
        op = node['op']
        if op == '+': return left_val + right_val
        if op == '-': return left_val - right_val
        if op == '*': return left_val * right_val
        if op == '/':
            if right_val == 0:
                return "ERROR"
            return left_val / right_val

# --- Formatting Helpers ---
def format_tree(node):
    if node is None: return "ERROR"
    if node['type'] == 'num':
        val = float(node['value'])
        return str(int(val)) if val.is_integer() else str(val)
    elif node['type'] == 'neg':
        return f"(neg {format_tree(node['operand'])})"
    elif node['type'] == 'binop':
        return f"({node['op']} {format_tree(node['left'])} {format_tree(node['right'])})"

# --- Main API Function ---
def evaluate_file(input_path: str) -> list[dict]:
    results = []
    output_path = os.path.join(os.path.dirname(input_path) or ".", "output.txt")

    try:
        with open(input_path, 'r') as f:
            lines = f.read().splitlines()
    except FileNotFoundError:
        print(f"Error: '{input_path}' not found.")
        return []

    out_lines = []
    for line in lines:
        if not line.strip():
            continue
           
        tokens = tokenize(line)
        tree = parse(tokens)
        val = evaluate_tree(tree)

        tok_str = "ERROR" if tokens == "ERROR" else " ".join([("[END]" if t['type']=='END' else f"[{t['type']}:{t['value']}]") for t in tokens])
        tree_str = "ERROR" if tree is None else format_tree(tree)

        if val == "ERROR":
            res_str = "ERROR"
            res_val = "ERROR"
        else:
            res_val = val
            res_str = str(int(val)) if val.is_integer() else f"{round(val, 4)}"

        results.append({
            "input": line,
            "tree": tree_str,
            "tokens": tok_str,
            "result": res_val
        })

        out_lines.append(f"Input: {line}")
        out_lines.append(f"Tree: {tree_str}")
        out_lines.append(f"Tokens: {tok_str}")
        out_lines.append(f"Result: {res_str}")
        out_lines.append("")

    with open(output_path, 'w') as f:
        f.write("\n".join(out_lines).strip() + "\n")

    return results

# Optional Test Runner (Does not interfere with module importing)
if __name__ == "__main__":
    if os.path.exists("sample_input.txt"):
        res = evaluate_file("sample_input.txt")
        print("Successfully generated the output.txt based on sample_input.txt")