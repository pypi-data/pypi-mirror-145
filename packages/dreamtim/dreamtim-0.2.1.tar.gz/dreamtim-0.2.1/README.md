This is a collection of useful tools for analytics, statistics and data science. At the moment, only test modules are available:
- calculator
- statistical_tools

# Installation

```
pip install dreamtim
```

# Usage

```python
from dreamtim.calculator import Calculator

calc_obj = Calculator(5)
calc_obj.add(3)
# returns 8.0
```

### Module calculator

This module contains just one class - **Calculator**. Its attributes:
- value, float: "memory" of the calculator
- show_value, bool: determines whether print messages about the current value in the calculator when performing arithmetic operations (default is False)
- show_operation, bool: determines whether print messages about the perfomed operation (default is False)
- round_number, int: the number of decimal places in numbers in the messages and in a string representation (default is 2)

For complete documentation, please, check this page:
https://ryko.tk/dreamtim/
