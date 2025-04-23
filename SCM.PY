import re

def pass1(source_lines):
    symbol_table = {}
    literal_table = []
    pool_table = []
    location_counter = 4
    processed_lines = []
    
    for line in source_lines:
        tokens = re.split(r'\s+', line.strip())
        if not tokens:
            continue
        
        if tokens[0].endswith(":"):  # Label definition
            label = tokens[0][:-1]
            symbol_table[label] = location_counter
            tokens.pop(0)
        
        if tokens:  # Process instructions
            for i, token in enumerate(tokens):
                if token.startswith("="):  # Literal detected
                    if token not in literal_table:
                        literal_table.append(token)
            processed_lines.append(tokens)
            location_counter += 1
    
    # Populate pool table
    pool_table.append(0)
    return symbol_table, literal_table, pool_table, processed_lines

def pass2(processed_lines, symbol_table, literal_table):
    OPCODES = {
        "LOAD": "01", "STORE": "02", "ADD": "03", "SUB": "04", "JUMP": "05",
        "JZ": "06", "HALT": "FF"
    }
    machine_code = []
    optimization_table = []
    
    for tokens in processed_lines:
        opcode = OPCODES.get(tokens[0], "??")
        operand = "00"
        
        if len(tokens) > 1:
            if tokens[1] in symbol_table:
                operand = f"{symbol_table[tokens[1]]:02X}"
            elif tokens[1] in literal_table:
                operand = f"{literal_table.index(tokens[1]) + 1:02X}"
            else:
                operand = tokens[1]  # Direct numeric values
        
        machine_code.append(f"{opcode}{operand}")
        optimization_table.append((tokens[0], operand))
    
    return machine_code, optimization_table

def main():
    source_code = [
        "START:",
        "LOAD A",
        "ADD B",
        "STORE C",
        "JUMP START",
        "A: 10",
        "B: 20",
        "C:",
        "D: =5",
        "E: =10"
    ]
    
    symbol_table, literal_table, pool_table, processed_lines = pass1(source_code)
    machine_code, optimization_table = pass2(processed_lines, symbol_table, literal_table)
    
    print("Symbol Table:", symbol_table)
    print("Literal Table:", literal_table)
    print("Pool Table:", pool_table)
    print("Optimization Table:")
    for entry in optimization_table:
        print(entry)
    print("Machine Code:")
    for code in machine_code:
        print(code)

if __name__ == "__main__":
    main()