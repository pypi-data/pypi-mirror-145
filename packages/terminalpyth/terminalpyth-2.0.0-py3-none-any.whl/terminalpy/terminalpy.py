#   MIT License
#
#   Copyright (c) 2022 Cargo
#
#   Permission is hereby granted, free of charge, to any person obtaining a copy
#   of this software and associated documentation files (the "Software"), to deal
#   in the Software without restriction, including without limitation the rights
#   to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
#   copies of the Software, and to permit persons to whom the Software is
#   furnished to do so, subject to the following conditions:
#
#   The above copyright notice and this permission notice shall be included in all
#   copies or substantial portions of the Software.
#
#   THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
#   IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#   FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
#   AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
#   LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
#   OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
#   SOFTWARE.

import subprocess, os

class Terminal:
    def __init__(self, output=False):
        self.__output__ = output # Determines if terminal return values must be returned
        self.__oldCds__ = [] # Directory changes memory

    # checks if the current command is a "cd". In that case, stores the directory change
    def __checkStore__(self, command: str):
        cmdList = self.__adjustCommand__(command)
        if cmdList[0] == 'cd':
            self.__oldCds__.append(command)
            return True
        return False

    # removes the unnecessary spaces in the command and splits it
    def __adjustCommand__(self, command: str):
        list = command.split(' ')
        i = 0
        while i < len(list):
            if list[i] == ' ' or list[i] == '':
                list.pop(i)
            i += 1
        return list

    # main command, which allows to type to the terminal
    def type(self, command: str):
        check = self.__checkStore__(command) # True or False, depending on the type of the current command
        if check: # only if current command is "cd"
            commands = '; '.join(self.__oldCds__) # adds "; " between each directory change, for multiline terminal command

            try: # send command(s) to he terminal, with error handler
                output = subprocess.check_output(commands, shell=True)
            except subprocess.CalledProcessError:
                self.__oldCds__.pop(-1)
                raise OSError('Command you entered not found or not valid in your environment')

            if isinstance(output, bytes): # if the return value is bytes, decodes it to string
                output = output.decode()

            if output[-1:len(output)] == '\n': # if the return value end with a new line, removes it
                output = output[0:-1]
        else: # if current command is not "cd"
            if len(self.__oldCds__) >= 1: # checks if there are command stored
                commands = '; '.join(self.__oldCds__) # adds "; " between each directory change, for multiline terminal command
                cmdList = self.__adjustCommand__(command) # splits current command

                if cmdList[0] == 'clear': # checks if current command is "clear", in that case, uses another type of process
                    os.system('clear')
                    output = ''
                else: # if current command is not "clear"
                    try: # sends the current command and the previous directory changes to the terminal, with error handler
                        output = subprocess.check_output(f'{commands}; {command}', shell=True)
                    except subprocess.CalledProcessError:
                        raise OSError('Command you entered not found or not valid in your environment')

                    if isinstance(output, bytes): # if the return value is bytes, decodes it to string
                        output = output.decode()

                    if output[-1:len(output)] == '\n': # if the return value end with a new line, removes it
                        output = output[0:-1]
            else: # if there is no command stored
                cmdList = self.__adjustCommand__(command) # splits the command

                if cmdList[0] == 'clear': # checks if current command is "clear", in that case, uses another type of process
                    os.system('clear')
                    output = ''
                else: # if the current command is not "clear"
                    try: # sends the commmand to the terminal, with error handler
                        output = subprocess.check_output(command, shell=True)
                    except subprocess.CalledProcessError:
                        raise OSError('Command you entered not found or not valid in your environment')

                    if isinstance(output, bytes): # if the return value is bytes, decodes it to string
                        output = output.decode()

                    if output[-1:len(output)] == '\n': # if the return value end with a new line, removes it
                        output = output[0:-1]
        if self.__output__ and output != b'' and output != '': # if the user wants the output, makes few more checks before returning
            return output

    # deletes from memory all the previous directory changes
    def clear(self):
        self.__oldCds__ = []

    # allows to change the output condition (return or do not return) during the session
    def setOutput(self, outputMode: bool):
        self.__output__ = outputMode