__docformat__ = "google"

"""This module contains only one class - Calculator.

Please note that usual floats are used here, not decimal,
so this calculator is not suitable for ultra-precise calculations!

To perform arithmetic operations, just create an instance:
>>> calc_obj = Calculator()
>>> calc_obj
Calculator(value=0.0, show_value=False, show_operation=False, round_number=2)
"""


class Calculator:
    """This class is an implementation of calculator,
    which performs actions with a value inside its memory.

    To start:
    >>> calc_obj = Calculator(5)

    For arithmetic operations use methods:
    >>> calc_obj.add(3)
    8.0

    Such methods can get not only float, but also
    int or str, that can be converted into float.

    To check current status, use attributes:
    >>> calc_obj.value
    8.0

    To set up print messages and rounding, use attributes:
    >>> calc_obj.show_operation = True
    >>> calc_obj.round_number = 3

    >>> result = calc_obj.divide(3)
    Divided by 3.000!
    >>> result
    2.6666666666666665
    >>> print(calc_obj)
    Calculator object. Current value: 2.667

    Pay attention to the fact that you are passing
    the correct types as an attributes, otherwise you can get errors!

    Attributes:
        value, float: "memory" of the calculator
        show_value, bool: determines whether print messages about
            the current value in the calculator when performing
            arithmetic operations (default is False)
        show_operation, bool: determines whether print messages
            about the perfomed operation (default is False)
        round_number, int: the number of decimal places in numbers
            in the messages and in a string representation (default is 2)
    """

    def __init__(
            self, value = 0,
            show_value: bool = False,
            show_operation: bool = False,
            round_number: int = 2) -> None:
        # Initialize an object with default values
        self.value = float(value)
        self.show_value = show_value
        self.show_operation = show_operation
        self.round_number = round_number

    def __repr__(self) -> str:
        # Represent an object as a string, according to Python docs
        attrs_str = ', '.join(f'{key}={value}' for key, value in self.__dict__.items())
        return f'Calculator({attrs_str})'

    def __str__(self) -> str:
        # Represent an object as a string for print etc
        return f'Calculator object. Current value:{self.value: .{self.round_number}f}'

    def add(self, added_value) -> float:
        """Adds the passed number to the value of the calculator"""

        added_value = float(added_value)
        self.value += added_value

        if self.show_operation:
            print(f'Added{added_value: .{self.round_number}f}!')
        if self.show_value:
            print(self.__str__())

        return self.value

    def substract(self, substracted_value) -> float:
        """Subatracts the passed number from the value of the calculator"""

        substracted_value = float(substracted_value)
        self.value -= substracted_value

        if self.show_operation:
            print(f'Substracted{substracted_value: .{self.round_number}f}!')
        if self.show_value:
            print(self.__str__())

        return self.value

    def multiply(self, multiplier) -> float:
        """Multiplies the value of the calculator by the passed number"""

        multiplier = float(multiplier)
        self.value *= multiplier

        if self.show_operation:
            print(f'Multiplied by{multiplier: .{self.round_number}f}!')
        if self.show_value:
            print(self.__str__())

        return self.value

    def divide(self, divider) -> float:
        """Divides the value of the calculator by the passed number"""

        divider = float(divider)
        self.value /= divider

        if self.show_operation:
            print(f'Divided by{divider: .{self.round_number}f}!')
        if self.show_value:
            print(self.__str__())

        return self.value

    def root(self, n):
        """Takes (passed number) root of the value of the calculator"""

        n = float(n)
        if self.value > 0:
            self.value = self.value ** (1 / n)
        elif self.value < 0:
            self.value = -((-self.value) ** (1 / n))
        else:
            self.value = 0.0
        
        if self.show_operation:
            print(f'The root of the{n: .{self.round_number}f} degree has been taken!')
        if self.show_value:
            print(self.__str__())

        print(self.value)
        return self.value

    def reset(self) -> None:
        """Resets the memory in the calculator:
        >>> calc_obj = Calculator(5)
        >>> calc_obj.reset()
        >>> calc_obj.value
        0.0
        """
        self.value = 0.0
        if self.show_operation:
            print(f'The memory has been reset! Current value:{self.value: .{self.round_number}}')


if __name__ == '__main__':

    import doctest
    
    print(doctest.testmod())
