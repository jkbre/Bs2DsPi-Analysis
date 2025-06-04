# Version 0.1.8
"""
Printter class for Python scripts applications.
"""
from termcolor import colored
from pprint import pprint


class Printter:  # TODO: Add documenation for each class methods
    """
    Definig printing functions
    """

    def __init__(self, verbose: bool = False, devMode: bool = False) -> None:
        """
        Initialize the Printer class object.
        ---
        Parameters:
            verbose (bool): verbose flag
        Returns:
            None
        Raises:
            None
        """
        self.verbose = verbose
        self.devMode = devMode

    def _isiterable(self, obj) -> bool:
        """
        Check if an object is iterable.
        ---
        Parameters:
            obj (any): object to check
        Returns:
            bool: True if object is iterable, False otherwise
        Raises:
            None
        """
        if hasattr(obj, "__iter__"):
            return True
        else:
            return False

    def _totuple(self, obj) -> tuple:
        """
        Convert an object to tuple.
        ---
        Parameters:
            obj (any): object to convert
        Returns:
            tuple: converted object
        Raises:
            None
        """
        if isinstance(obj, str) or obj is None:
            return (obj,)
        elif isinstance(obj, dict):
            raise ValueError("Creation of tuple is not possible.")
        elif self._isiterable(obj):
            return tuple(obj)
        else:
            raise ValueError("Creation of tuple is not possible.")

    def iprint(self, *args, order: int = 0, colors=None, **kwargs) -> None:
        """
        Print function with indentation and color. Possible usage:
        iprint(0, "blue", "This is a normal text") -> This is a blue text
        iprint(1, "blue", "This is a blue text") -> | This is a normal text
        iprint(2, "blue", "This is a blue text") -> | | This is a normal text

        iprint(0, ("blue", "red"), "This is a normal text") -> This is a blue text
        ---
        Parameters:
            order (int): order of indentation
            colors (tuple): color of the text
            args (tuple): arguments to print
        Returns:
            None
        Raises:
            ValueError: Colors length must be equal to order or order + 1.
        """

        order = max(0, order)
        leadingSymbols = {"red": "!", "yellow": "?", "green": ">", "cyan": "<"}
        colors = self._totuple(colors)
        printType = None

        for icolor in colors:
            if icolor not in leadingSymbols:
                leadingSymbols[icolor] = "|"

        if order == 0 and len(colors) == 1:
            printType = "Default"
        elif len(colors) == 1:
            printType = "Simple Rows"
        elif order == len(colors) - 1:
            printType = "Rainbow"
        elif order > len(colors):
            printType = "Accents"
        elif order == len(colors):
            printType = "Colorful Rows"
        else:
            raise ValueError("Order number and colors length are not compatible.")

        if self.devMode is True:
            print(f"Print Type: {printType}")

        match printType:
            case "Default":
                # TODO: Try to rewrite this procedure [#1] below (of checking if in args is a not string variable) to be more readable
                stringLimit = next((i for i, arg in enumerate(args) if not isinstance(arg, str)), -1)
                if stringLimit == -1:
                    printout = " ".join(args)
                    print(colored(color=colors[0], text=printout), **kwargs)
                else:
                    header = " ".join(args[:stringLimit])
                    body = args[stringLimit:]
                    print(colored(header, colors[0]), *body, **kwargs)

            case "Colorful Rows":
                leadingSymbol = leadingSymbols[colors[0]]
                print(colored(leadingSymbol, colors[0]), end="")
                for icolor in colors[1:]:
                    isymbol = leadingSymbols[icolor]
                    print(colored(f" {isymbol}", icolor), end="")
                print("", *args, **kwargs)

            case "Simple Rows":
                leadingSymbol = leadingSymbols[colors[0]]
                indent = leadingSymbol + (f" {leadingSymbol}") * (order - 1)
                print(colored(indent, colors[0]), *args, **kwargs)

            case "Rainbow":
                leadingSymbol = leadingSymbols[colors[0]]
                # TODO: Try to avoid redundancy of this procedure [#1] below -> make a function for it
                stringLimit = next((i for i, arg in enumerate(args) if not isinstance(arg, str)), -1)

                printout = None
                if stringLimit == -1:
                    printout = " ".join(args)
                else:
                    header = " ".join(args[:stringLimit])
                    body = args[stringLimit:]

                print(colored(leadingSymbol, colors[0]), end="")
                for icolor in colors[1:-1]:
                    isymbol = leadingSymbols[icolor]
                    print(colored(f" {isymbol}", icolor), end="")
                if printout is not None:
                    print(colored(" " + printout, colors[-1]), **kwargs)
                else:
                    print(colored(" " + header, colors[-1]), *body, **kwargs)  # for case where a variable is also printed

            case _:
                if not self.devMode:
                    raise ValueError("Not yet implemented.")
                else:
                    print("TODO: Implement this case.")

    def vprint(self, *args, verbose=None, **kwargs) -> None:
        """
        Print function with verbose dependency.
        ---
        Parameters:
            args (tuple): arguments to print
            verbose (bool): verbose flag
        Returns:
            None
        Raises:
            None
        """
        verbose = self.verbose if verbose is None else verbose
        print(*args, **kwargs) if verbose else None

    def pprint(self, variable, **kwargs) -> None:
        """
        Print function for single variables.
        ---
        Parameters:
            variable (any): variable to print
        Returns:
            None
        Raises:
            None
        """
        print(variable, **kwargs)

    def vpprint(self, variable, verbose=None, **kwargs) -> None:
        """
        Print function for single variables with verbose dependency.
        ---
        Parameters:
            variable (any): variable to print
            verbose (bool): verbose flag
        Returns:
            None
        Raises:
            None
        """
        verbose = self.verbose if verbose is None else verbose
        pprint(variable, **kwargs) if verbose else None

    def viprint(self, *args, verbose=None, order: int, colors, **kwargs) -> None:
        """
        Print function with indentation and color option and verbose dependency.
        ---
        Parameters:
            order (int): order of indentation
            colors (str or tuple): color of the text
            args (tuple): arguments to print
            verbose (bool): verbose flag
        Returns:
            None
        Raises:
            None
        """
        verbose = self.verbose if verbose is None else verbose
        self.iprint(*args, order=order, colors=colors, **kwargs) if verbose else None

    def nvprint(self, *args, verbose=None, **kwargs) -> None:
        """
        Print function with anti-verbose dependency.
        ---
        Parameters:
            args (tuple): arguments to print
            verbose (bool): verbose flag
        Returns:
            None
        Raises:
            None
        """
        verbose = self.verbose if verbose is None else verbose
        print(*args, **kwargs) if not verbose else None
