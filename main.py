import tkinter as tk

# Define the instruction set
instructions = {
    "ADD": lambda reg1, reg2, dest: dest.set(reg1.get() + reg2.get()),
    "SUB": lambda reg1, reg2, dest: dest.set(reg1.get() - reg2.get()),
    "MUL": lambda reg1, reg2, dest: dest.set(reg1.get() * reg2.get()),
    "DIV": lambda reg1, reg2, dest: dest.set(reg1.get() / reg2.get() if reg2.get() != 0 else "Error: Division by zero"),
    "MOV": lambda value, dest: dest.set(value),
    "HALT": lambda: "Program terminated"
}

class ISASimulator(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("ISA Simulator")
        self.geometry("600x400")

        # Create a text area for input
        self.input_text = tk.Text(self, height=10, width=50)
        self.input_text.pack(pady=10)

        # Create a button to execute the instructions
        self.execute_button = tk.Button(self, text="Execute", command=self.execute_instructions)
        self.execute_button.pack(pady=5)

        # Create a text area for output
        self.output_text = tk.Text(self, height=10, width=50)
        self.output_text.pack(pady=10)

        # Initialize registers
        self.registers = {
            "R0": tk.IntVar(value=0),
            "R1": tk.IntVar(value=0),
            "R2": tk.IntVar(value=0),
            "R3": tk.IntVar(value=0)
        }

    def execute_instructions(self):
        # Get the input instructions
        instructions_str = self.input_text.get("1.0", "end-1c")
        instructions_list = instructions_str.split("\n")

        # Execute the instructions
        output = ""
        for instruction in instructions_list:
            parts = instruction.split()
            op = parts[0]
            
            if op in instructions:
                if op == "HALT":
                    output += instructions[op]() + "\n"
                    break
                elif op == "MOV":
                    if len(parts) == 3:
                        dest_reg = parts[1].rstrip(',')
                        value = int(parts[2])
                        dest = self.registers[dest_reg]
                        instructions[op](value, dest)
                        output += f"{op} {dest_reg}, {value} = {dest.get()}\n"
                elif len(parts) == 4:
                    dest_reg = parts[1].rstrip(',')
                    reg1_name = parts[2].rstrip(',')
                    reg2_name = parts[3].rstrip(',')
                    reg1 = self.registers[reg1_name]
                    reg2 = self.registers[reg2_name]
                    dest = self.registers[dest_reg]
                    instructions[op](reg1, reg2, dest)
                    output += f"{op} {dest_reg}, {reg1_name}, {reg2_name} = {dest.get()}\n"
            else:
                output += f"Invalid instruction: {instruction}\n"

        # Display the output
        self.output_text.delete("1.0", "end")
        self.output_text.insert("1.0", output)

if __name__ == "__main__":
    app = ISASimulator()
    app.mainloop()
    