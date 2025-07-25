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
    expr = re.sub(r'(?<=[A-Za-z])(?=[A-Za-z\(])', r' and ', expr)
    
    # Step 2: Insert AND after NOT (e.g., X'Y -> X' and Y)
    expr = re.sub(r"([A-Za-z])'(?=[A-Za-z])", r"\1' and ", expr)
    
    # Step 3: Replace A' with not A
    expr = re.sub(r"([A-Za-z])'", r"not \1", expr)
     
    # Step 4: Replace + with or
    expr = expr.replace('+', ' or ')
    
    # Step 5: Replace ^ with != for XOR operation
    expr = expr.replace('^', ' != ')

    # Step 6: Space out parentheses
    expr = expr.replace('(', ' ( ').replace(')', ' ) ')
    
    # Step 7: Handle negation of expressions in parentheses (e.g., (A or B)' -> not (A or B))
    expr = re.sub(r"\(\s*([^\(\)]+?)\s*\)\s*'", lambda m: f"not ( {m.group(1)} ) ", expr)

    # Step 8: Tokenize and insert 'and' where needed (e.g., var followed by 'not' or '(')
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

def generate_truth_table(raw_expr, show_kmap=False):
    variables = extract_variables(raw_expr)
    expr = preprocess(raw_expr)

    print("\nParsed expression:", expr.replace("!=", "XOR"))
    print()
    print(" | ".join(variables) + " | Output | Minterm | Maxterm")
    print("-" * (6 * len(variables) + 24))

    # Ensure all combinations are generated
    all_combinations = list(itertools.product([0, 1], repeat=len(variables)))
    
    kmap_data = {}
    for idx, values in enumerate(all_combinations):
        context = {var: bool(val) for var, val in zip(variables, values)}

        try:
            result = eval(expr, {}, context)
        except Exception as e:
            result = f"ERR({e})"

        row = " | ".join(str(v) for v in values)
        output = int(bool(result)) if isinstance(result, (bool, int)) else result
        minterm = str(idx) if output == 1 else ""
        maxterm = str(idx) if output == 0 else ""

        row = " | ".join(str(v) for v in values)
        print(f"{row} |   {output}    | {minterm:^8} | {maxterm:^8}")
        print("-" * (6 * len(variables) + 24))
        if isinstance(output, int):
            kmap_data[tuple(values)] = output

    if show_kmap:
        display_kmap(variables, kmap_data)

def display_kmap(variables, kmap_data):
    print("\nKarnaugh Map:\n")

    def cell(val):
        return f"{str(val) if val in [0, 1] else ' ':^7}"

    def print_row(label, values):
        label_str = label.ljust(8)
        row = " | ".join(cell(kmap_data.get(key, 0)) for key in values)
        print(f"{label_str}| {row} |")

    def print_border(num_cols):
        border = "+".join(["-" * 9] * (num_cols))
        print(f"        +{border}+")

    if len(variables) == 2:
        label0 = f"{variables[1]}=0"
        label1 = f"{variables[1]}=1"
        print(f"          {label0:^7} | {label1:^7}")


        print_border(2)
        for a in [0, 1]:
            keys = [(a, 0), (a, 1)]
            print_row(f"{variables[0]}={a}", keys)
            print_border(2)

    elif len(variables) == 3:
        print(f"        {variables[1]}{variables[2]}")
        print(f"          {'00':^7} | {'01':^7} | {'11':^7} | {'10':^7}")
        print_border(4)
        for a in [0, 1]:
            keys = [(a, 0, 0), (a, 0, 1), (a, 1, 1), (a, 1, 0)]
            print_row(f"{variables[0]}={a}", keys)
            print_border(4)

    elif len(variables) == 4:
        print(f"        {variables[2]}{variables[3]}")
        print(f"          {'00':^7} | {'01':^7} | {'11':^7} | {'10':^7}")
        print_border(4)
        for ab in [(0, 0), (0, 1), (1, 1), (1, 0)]:
            keys = [(*ab, 0, 0), (*ab, 0, 1), (*ab, 1, 1), (*ab, 1, 0)]
            print_row(f"{variables[0]}{variables[1]}={ab[0]}{ab[1]}", keys)
            print_border(4)

    else:
        print("K-map display is only supported for 2, 3, or 4 variables.")

def main():
    parser = argparse.ArgumentParser(description="Generate a truth table from a Boolean expression like A'B+C or WXYZ.")
    parser.add_argument("-k", "--karnaugh", action="store_true", help="Enable Karnaugh Map display for up to 4 variables")
    parser.add_argument("expr", help="Boolean expression using + (OR), ' (NOT), implicit AND")    
    args = parser.parse_args()
    generate_truth_table(args.expr, show_kmap=args.karnaugh)

if __name__ == "__main__":
    main()
