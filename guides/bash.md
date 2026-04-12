# Bash Reference

## Rules:

Use quotes to surround strings that contain value of variables or output of commands.

E.g.

```bash
"...$my_var..."
"...$(my_command)..."
```

## Variable Substitution

```bash
# Returns the expansion of WORD, if VAR is undefined or empty.
# Otherwise, returns VAR.
${VAR:-WORD}

# Returns the expansion of WORD and run VAR=WORD, if VAR is undefined or empty.
# Otherwise, returns VAR.
${VAR:=WORD}

# Skip the first N characters.
${VAR:N}
# Skip the first N characters, and keep the next M characters.
${VAR:N:M}
```
