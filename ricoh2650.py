import os
import subprocess
from pydub.generators import Sine
from tkinter import Tk, filedialog

class Ricoh2650:
    def __init__(self):
        self.pc = 0x1000  # Program counter (start at 0x1000 for loaded programs)
        self.acc = 0      # Accumulator
        self.memory = [0] * 0x10000  # 64KB memory space
        self.halted = False  # CPU state (halted or not)

    def load_program(self, program: list):
        """Load a list of bytes as a program into memory starting at 0x1000."""
        self.memory[0x1000: 0x1000 + len(program)] = program

    def load_program_from_file(self, filepath: str):
        """Load a program from a .r2650 file containing comma-separated values."""
        try:
            with open(filepath, "r") as file:
                content = file.read()
                # Parse CSV-like content (e.g., 0x00, 0x10, 0x13, 0x01)
                program = [int(byte.strip(), 16) for byte in content.split(",")]
                self.load_program(program)
                print(f"Program loaded from {filepath}")
        except Exception as e:
            print(f"Failed to load program: {e}")

    def step(self):
        """Execute one instruction (simplified)."""
        if self.halted:
            return
        opcode = self.memory[self.pc]
        if opcode == 0x01:  # Example: ADD instruction (pseudo-opcode)
            self.acc += self.memory[self.pc + 1]
            self.pc += 2
        elif opcode == 0x00:  # No-op (just for demo purposes)
            self.pc += 1
        else:
            self.pc += 1  # Skip unknown opcodes
        print(f"Executed opcode {hex(opcode)} at PC={hex(self.pc)}")

    def halt(self):
        """Halt the emulator."""
        self.halted = True
        print("Emulator halted.")

    def unhalt(self):
        """Unhalt the emulator."""
        self.halted = False
        print("Emulator running.")

    def dump(self):
        """Print current state."""
        print(f"PC: {hex(self.pc)}, Accumulator: {hex(self.acc)}, Halted: {self.halted}")

    def execute_asm(self, asm_code):
        """Execute an assembly-like instruction (simplified for demo purposes)."""
        instructions = asm_code.split()
        for instr in instructions:
            if instr == "NOP":  # No Operation
                self.memory[self.pc] = 0x00
                self.pc += 1
            elif instr == "ADD":
                self.memory[self.pc] = 0x01
                self.memory[self.pc + 1] = 0x10  # Example operand
                self.pc += 2
            else:
                print(f"Unknown instruction: {instr}")

# Emulator with console interaction
class EmulatorConsole:
    def __init__(self):
        self.cpu = Ricoh2650()
        self.running = True

    def playsound(self, frequency, duration=1):
        """Play a sound of the given frequency using ffplay."""
        print(f"Playing sound at {frequency} Hz for {duration} second(s).")
        try:
            sine_wave = Sine(frequency).to_audio_segment(duration=duration * 1000)
            
            # Define a custom temp directory
            temp_dir = r"C:\\Users\\Oem\\Desktop\\tmp"
            os.makedirs(temp_dir, exist_ok=True)  # Ensure the directory exists
            
            temp_file_path = os.path.join(temp_dir, "sine_wave.wav")
            sine_wave.export(temp_file_path, format="wav")
            
            # Use ffplay for playback and suppress output
            subprocess.run(["ffplay", "-autoexit", "-nodisp", temp_file_path], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

            # Clean up the temporary file
            os.remove(temp_file_path)

        except Exception as e:
            print(f"Error playing sound: {e}")

    def process_input(self, user_input):
        """Process user input and call corresponding function."""
        user_input = user_input.strip().lower()

        if user_input == "halt":
            self.cpu.halt()
        elif user_input == "unhalt":
            self.cpu.unhalt()
        elif user_input.startswith("asm"):
            # Execute ASM code from the input
            asm_code = user_input[4:].strip()
            self.cpu.execute_asm(asm_code)
        elif user_input == "step":
            # Execute a single step (instruction)
            self.cpu.step()
        elif user_input == "dump":
            self.cpu.dump()
        elif user_input.startswith("playsound"):
            try:
                # Parse the frequency from the input
                parts = user_input.split()
                frequency = int(parts[1])
                duration = float(parts[2]) if len(parts) > 2 else 1
                self.playsound(frequency, duration)
            except (IndexError, ValueError):
                print("Usage: playsound <frequency> [duration]")
        elif user_input == "load":
            # Open a file dialog to select a .r2650 file
            try:
                Tk().withdraw()  # Hide the main tkinter window
                filepath = filedialog.askopenfilename(filetypes=[("Ricoh 2650 Programs", "*.r2650")])
                if filepath:
                    self.cpu.load_program_from_file(filepath)
            except Exception as e:
                print(f"Error loading program: {e}")
        elif user_input == "exit":
            self.running = False
        else:
            print("Unknown command.")

    def run(self):
        """Run the emulator console and accept user commands."""
        while self.running:
            try:
                user_input = input(">>> ").strip()
                self.process_input(user_input)
            except KeyboardInterrupt:
                break
            except Exception as e:
                print(f"Error: {str(e)}")

        print("Exiting emulator.")

# Example program to load
program = [0x01, 0x10, 0x00, 0x00]  # Simple program for demo purposes

# Run the emulator with console interface
if __name__ == "__main__":
    emulator = EmulatorConsole()
    emulator.cpu.load_program(program)
    emulator.run()
