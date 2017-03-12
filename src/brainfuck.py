#!/usr/local/bin/python3

import sys


class BrainfuckInterpreter(object):
    __mem = bytearray(30000)
    __pointer = 0
    __program = ""
    __program_code = ""
    __program_counter = 0
    __verbose = False
    __loud = False
    __output_file = None
    __running = True

    def process_args(self, args):
        i = 0
        while i < len(args):
            if str.startswith(args[i], "-"):
                if args[i] == "-v":
                    self.__verbose = True
                elif args[i] == "-V":
                    self.__verbose = True
                    self.__loud = True
                elif args[i] == "-o":
                    i += 1
                    self.__output_file = open(args[i], "w")
            elif self.__program == "":
                self.__program = args[i]
            i += 1

    def run(self):
        print("-= {NAME} OUTPUT START =-\n".format(NAME=str.upper(self.__program)))
        try:
            while self.__running:
                self.process_instruction()
        except IndexError:
            print(self.__pointer)
            print(self.__program_counter)
            print(self.__mem)
            print(self.__program_code)
        except KeyboardInterrupt:
            pass
        print("\n-=: {NAME} OUTPUT END :=-".format(NAME=str.upper(self.__program)))

    def process_instruction(self):
        # End of program reached
        if self.__program_counter == len(self.__program_code):
            self.__running = False
            return
        instr = self.__program_code[self.__program_counter]
        if instr == '>':
            if self.__verbose:
                print("INCREMENT POINTER")
            self.__pointer += 1
            if self.__pointer == len(self.__mem):
                self.__mem.append(0)
        elif instr == '<':
            if self.__verbose:
                print("DECREMENT POINTER")
            self.__pointer -= 1
            if self.__pointer < 0:
                error_message = "MEMORY POINTER OUT OF RANGE: -1"
                self.__running = False
                print(error_message)
                if self.__output_file is not None:
                    self.__output_file.write(error_message)
        elif instr == '+':
            if self.__verbose:
                print("INCREMENT MEMORY AT LOCATION {pointer}".format(pointer=self.__pointer))
            if self.__mem[self.__pointer] == 255:
                self.__mem[self.__pointer] = 0
            else:
                self.__mem[self.__pointer] += 1
        elif instr == '-':
            if self.__verbose:
                print("DECREMENT MEMORY AT LOCATION {pointer}".format(pointer=self.__pointer))
            if self.__mem[self.__pointer] == 0:
                self.__mem[self.__pointer] = 255
            else:
                self.__mem[self.__pointer] -= 1
        elif instr == ',':
            if self.__verbose:
                print("GET INPUT FOR MEMORY AT LOCATION {pointer}".format(pointer=self.__pointer))
            self.__mem[self.__pointer] = ord(sys.stdin.read(1))
        elif instr == '.':
            if self.__verbose:
                print("OUTPUT MEMORY AT LOCATION {pointer}".format(pointer=self.__pointer))
            print(chr(self.__mem[self.__pointer]), end="")
        elif instr == '[':
            if self.__mem[self.__pointer] == 0:
                self.__program_counter += 1
                if self.__verbose:
                    print("START CONDITIONAL LOOP")
                depth = 0
                while depth > 0 or self.__program_code[self.__program_counter] != ']':
                    instr = self.__program_code[self.__program_counter]
                    if instr == '[':
                        depth += 1
                    elif instr == ']':
                        if depth == 0:
                            break
                        depth -= 1
                    self.__program_counter += 1
                if self.__verbose:
                    print("END LOOP")
        elif instr == ']':
            if self.__mem[self.__pointer] != 0:
                self.__program_counter -= 1
                if self.__verbose:
                    print("TRAVERSE BACK TO START OF LOOP")
                    if self.__loud:
                        print("RUNNING LOOP BECAUSE MEMORY AT {pointer} IS {data}".format(
                            pointer=self.__pointer,
                            data=self.__mem[self.__pointer]
                        ))
                depth = 0
                while depth > 0 or self.__program_code[self.__program_counter]:
                    instr = self.__program_code[self.__program_counter]
                    if self.__loud:
                        print("--------------------------------")
                        print("INSTR            ->   {instr}".format(instr=instr))
                        print("PROGRAM COUNTER  ->   {pc}".format(pc=self.__program_counter))
                        print("DEPTH            ->   {d}".format(d=depth))
                    if instr == ']':
                        depth += 1
                    elif instr == '[':
                        if depth == 0:
                            break
                        depth -= 1
                    self.__program_counter -= 1
                if self.__verbose:
                    print("START OF LOOP REACHED")
                self.__program_counter -= 1
            pass
        self.__program_counter += 1

    def read_program(self):
        if self.__program == "":
            print("Usage: brainfuck.py [-v] [-V] [-o <output file>] <input file>")
            print("Options:")
            print("  -v           Verbose program execution")
            print("  -V           Loud verbose program execution(Not Recommended for normal use)")
            print("  -o <file>    Write program output to the specified file")
            sys.exit(0)
        self.__program_code = open(str(self.__program), "r").read()


if __name__ == '__main__':
    interpreter = BrainfuckInterpreter()
    interpreter.process_args(sys.argv[1:])
    interpreter.read_program()
    interpreter.run()
