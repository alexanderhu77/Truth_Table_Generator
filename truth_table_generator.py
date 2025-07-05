import argparse
import re
import itertools

def extract_variables(expr):
    # Extract all single-letter variable names, including from continuous strings like WXYZ
    tokens = re.findall(r'[A-Za-z]', expr)
    keywords = {'and', 'or', 'not'}
    return sorted(set(t for t in tokens if t not in keywords))

def preprocess(expr):
    
    # Step 1: Insert AND between adjacent variables (e.g., AB -> A and B)
    expr = re.sub(r'(?<=[A-Za-z])(?=[A-Za-z])', r' and ', expr)
    
    # Step 2: Insert AND after NOT (e.g., X'Y -> X' and Y)
    expr = re.sub(r"([A-Za-z])'(?=[A-Za-z])", r"\1' and ", expr)
    
    # Step 3: Replace A' with not A
    expr = re.sub(r"([A-Za-z])'", r"not \1", expr)
     
    # Step 4: Replace + with or
    expr = expr.replace('+', ' or ')
    
    # Step 5: Space out parentheses
    expr = expr.replace('(', ' ( ').replace(')', ' ) ')
    
    # Step 6: Handle negation of expressions in parentheses (e.g., (A+B)' -> not (A or B))
    expr = re.sub(r"\(\s*([^\(\)]+?)\s*\)\s*'", lambda m: f"not ( {m.group(1)} )", expr)

    # Step 7: Tokenize and insert 'and' where needed (e.g., var followed by 'not' or '(')
    tokens = expr.split()
    
    new_tokens = []
    i = 0
    while i < len(tokens):
        new_tokens.append(tokens[i])
        if i < len(tokens) - 1:
            curr = tokens[i]
            nxt = tokens[i + 1]
            curr_is_atom = re.fullmatch(r'[A-Za-z]', curr) or curr == ')'
            nxt_is_atom = re.fullmatch(r'[A-Za-z]', nxt) or nxt == '(' or nxt == 'not'
            if curr_is_atom and nxt_is_atom:
                new_tokens.append('and')
        i += 1
    
    final_expr = ' '.join(new_tokens)

    return final_expr

def generate_truth_table(raw_expr):
    variables = extract_variables(raw_expr)
    expr = preprocess(raw_expr)

    print("\nParsed expression:", expr)
    print()
    print(" | ".join(variables) + " | Output")
    print("-" * (5 * len(variables) + 5))

    # Ensure all combinations are generated
    all_combinations = list(itertools.product([0, 1], repeat=len(variables)))
    
    for values in all_combinations:
        context = {var: bool(val) for var, val in zip(variables, values)}
        
        try:
            result = eval(expr, {}, context)
        except Exception as e:
            result = f"ERR({e})"

        row = " | ".join(str(v) for v in values)
        print(f"{row} |   {int(bool(result)) if isinstance(result, (bool, int)) else result}")
        print("-" * (5 * len(variables) + 5))

def main():
    parser = argparse.ArgumentParser(description="Generate a truth table from a Boolean expression like A'B+C or WXYZ.")
    parser.add_argument("expr", help="Boolean expression using + (OR), ' (NOT), implicit AND")
    args = parser.parse_args()
    generate_truth_table(args.expr)

if __name__ == "__main__":
    main()
