# Truth Table Generator

This Python script generates a truth table for any Boolean expression using **single-letter variables** (like `A`, `B`, `X`, `Y`, `Z`). It accepts input expressions with:

- `+` for **OR** (e.g., `A+B` means A OR B)
- `'` for **NOT** (e.g., `A'` means NOT A)
- Parentheses or no symbol for **AND** (e.g., `A(B)` as well as `AB` means A AND B)

## Features

- Supports any number of variables
- Outputs a full truth table with all combinations

---

## How to Use

1. Save the script as `truth_table_generator.py`.

2. Run it from the command line, passing in a Boolean expression. Exanples: `XY'Z`, `X+Y+Z`, and `a+XY'+Bh`. If spaces are included in the expression, quotes must be used. Syntax:

```bash
python truth_table_generator.py "{EXPRESSION}"
```
## Examples of Expressions

- AB      means A AND B
- A'B     means NOT A AND B
- A+B     means A OR B
- A(B+C)  means A AND (B OR C)
- (XY)'Z  means NOT (X AND Y) AND Z
- AB(C+D)' means A AND B AND NOT (C OR D)
- WXYZ    means W AND X AND Y AND Z
