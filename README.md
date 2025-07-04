# Truth Table Generator

This Python script generates a truth table for any Boolean expression using **single-letter variables** (like `A`, `B`, `X`, `Y`, `Z`). It accepts input expressions with:

- `+` for **OR**
- `'` for **NOT** (e.g., `A'` means NOT A)
- No symbol for **AND** (e.g., `AB` means A AND B)
- Spaces ignored (e.g., `A B` means A AND B)

## Features

- Supports any number of variables
- Outputs a full truth table with all combinations

---

## How to Use

1. Save the script as `truth_table_generator.py`.

2. Run it from the command line, passing in a Boolean expression. Exanples: `XY'Z`, `X+Y+Z`, and `a+XY'+Bh`. If spaces are included in the expression, quotes must be used. Syntax:

```bash
python truth_table_generator.py "{EXPRESSION}"
