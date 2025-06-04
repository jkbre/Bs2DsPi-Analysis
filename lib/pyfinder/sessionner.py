# Version 0.0.7
"""
Terminal UI for Python scripts applications. THE TRUE MAIN FILE!
"""
from .printter import Printter
import traceback
from pathlib import Path
from os.path import expanduser


class Sessionner(Printter):  # TODO: Add documenation for each class methods
    def __init__(self, API, verbose: bool = False) -> None:
        super().__init__(verbose=verbose)  # Inheriting from the Printter class
        self.API = API
        self.API.init_session("terminal")
        self.allowed_globals = {"__builtins__": None} | self.API.allowed_globals
        self.allowed_locals = {"help": self._help} | self.API.allowed_locals | {"exit": self._exit}
        self.allowed_locals_desc = self.API.allowed_locals_desc | {"exit": "exit the program"}
        self.welcome = self.API.welcome
        self.prompter = self.API.prompter
        self.leadingColor = "green"
        self.sideColor = "dark_grey"
        self.errorColor = "red"
        self.running = True
        self.session_type = self.API.session_type

    def _handler(self, message):
        try:
            method, *params = (
                message.split(" ")
                if " " in message
                else (message.split("(")[0], *message.split("(")[1].split(")")[0].split(", "))
            )
        except IndexError:
            method = message
            params = []

        joined_params = '", "'.join(params)
        command = f'{method}("{joined_params}")'
        command = command.replace('""', "")

        try:
            exec(command, self.allowed_globals, self.allowed_locals)
        except TypeError or SyntaxError:
            self.viprint(f"Error Message:\n {traceback.format_exc()}", order=1, colors=self.errorColor)

    def _ui_notebook(self):
        # TODO: Add a Jupiter notebook interface
        pass

    def _ui_terminal(self):
        self.iprint(self.welcome, order=0, colors=self.leadingColor)  # TODO: Add as a first run message
        self.iprint('Always can type "help" if needed', order=1, colors=self.leadingColor)  # TODO: Add as a first run message

        while self.running:
            try:
                print(self.prompter, end=" ")
                self._handler(input())
            except KeyboardInterrupt:  # TODO: Add a KeyboardInterrupt handler for any function in the API
                print("\nProgram interrupted. Exiting gracefully...")
                # Perform any cleanup here
                exit(0)
            except EOFError:
                print("\nEOF received. Exiting gracefully...")
                # Perform any cleanup here
                exit(0)
            except Exception as e:
                self.iprint(f"Error: {e}", order=0, colors=self.errorColor)
                self.viprint(f"Traceback: {traceback.format_exc()}", order=1, colors=self.errorColor)
                self._log_traceback(e)

    def _get_environment(self):
        try:
            shell = get_ipython().__class__.__name__  # type: ignore
            if shell == "ZMQInteractiveShell":
                return "notebook"  # Jupyter notebook or qtconsole
            elif shell == "TerminalInteractiveShell":
                return "ipython"  # Terminal running IPython
            else:
                return "other"  # Other type (?)
        except NameError:
            return "terminal"  # Probably standard Python interpreter

    def _log_traceback(self, e: Exception):
        # with open(Path(__file__).parent / "tracebacks.txt", "a") as file:
        #     file.write(f"Error: {e}\n")
        #     file.write(f"Traceback: {traceback.format_exc()}\n")
        pass

    def _exit(self):
        self.iprint("Exiting...", order=0, colors=self.sideColor)
        self.running = False

    def _help(self):
        self.iprint("Commands:", order=0, colors=self.leadingColor)
        for ikey, desc in self.allowed_locals_desc.items():
            self.iprint(f"{ikey} -> {desc}", order=1, colors=self.leadingColor)

    def run(self):
        try:
            environment = self._get_environment()
            match environment:
                # case "notebook":
                #     self._ui_notebook()
                # case "ipython":
                #     self._ui_ipython()
                case "terminal":
                    self._ui_terminal()
                case _:
                    self.iprint("Unknown environment", order=0, colors=self.errorColor)
        except Exception as e:
            self.iprint(f"Error: {e}", order=0, colors=self.errorColor)
            # self.iprint(f"Traceback: {traceback.format_exc()}", order=1, colors=self.errorColor)
            self._log_traceback(e)
            self._exit()
