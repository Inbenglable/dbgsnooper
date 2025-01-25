# dbgsnooper (based on Pysnooper)

## Installation

```bash
git clone https://github.com/Inbenglable/dbgsnooper.git
cd dbgsnooper
python -m pip install -e .
```

This will install the package locally, and any changes you make to the code will take effect immediately without needing a reinstall.


## About dbgsnooper

`dbgsnooper` is a simple yet powerful debugger for Python. It is based on `PySnooper`, a lightweight debugging tool that provides a "set -x" style trace of your Python code. With `dbgsnooper`, you can quickly debug your code by automatically logging function calls and their return values, as well as the lines of code being executed—without needing to set breakpoints.

This project is a modified version of the original `PySnooper` with added features. While it inherits all the functionality and usage patterns of `PySnooper`, it introduces the ability to specify and limit the scope of observation.

### New Features Added to dbgsnooper

1. **Observe a Specific Range of Code**  
   You can now limit the trace to a specific range of lines in your code by using the `observed_file`, `start_line`, and `end_line` parameters. This is useful when you only want to focus on a particular part of your code:

   ```python
   @dbgsnooper.snoop(observed_file='/path/to/your/file.py', start_line=8, end_line=13, depth=2)
   def my_function():
       # function code
   ```

   In this example, the debugger will only trace the code between lines 8 and 13 of `file.py`, with a `depth` of 2.

2. **Limit obsservation on Loop Iterations**  
   When debugging loops, it’s often helpful to limit the number of iterations logged. The `loop` parameter lets you restrict the trace to a specified number of iterations:

   ```python
   @dbgsnooper.snoop(loop=1)
   def my_function():
       for i in range(10):
           # some code
   ```

   In this case, the debugger will trace only the first loop iteration, making it easier to debug without excessive output.


### 3. **Trace an Entire Python Script Without Modifying Its Code**  

The `run_reproducer.py` script allows you to trace the execution of an entire Python program **without needing to manually add decorators**. This is especially useful when debugging a script from start to finish without worrying about which specific functions should be instrumented.  

#### **How It Works**  

You provide the script to be executed along with the specific file and code sections you want to trace. The following parameters are available:

- **`script_path`** – The path to the Python script you want to debug.  
- **`observed_file`** – The file containing the code to be traced.  
- **`start_line` & `end_line`** – The range of lines to observe.  
- **`depth`** – The level of call stack depth to include in the trace.  
- **`loop`** – Limits trace output for loop iterations.  

#### **Why Use This Approach?**  
- No need to modify the original script.  
- Ideal for debugging **third-party code** or **large projects** where adding decorators to individual functions is impractical.   


---

The following is the introduciton of PySnooper.

## PySnooper
**PySnooper** is a poor man's debugger. If you've used Bash, it's like `set -x` for Python, except it's fancier.

Your story: You're trying to figure out why your Python code isn't doing what you think it should be doing. You'd love to use a full-fledged debugger with breakpoints and watches, but you can't be bothered to set one up right now.

You want to know which lines are running and which aren't, and what the values of the local variables are.

Most people would use `print` lines, in strategic locations, some of them showing the values of variables.

**PySnooper** lets you do the same, except instead of carefully crafting the right `print` lines, you just add one decorator line to the function you're interested in. You'll get a play-by-play log of your function, including which lines ran and   when, and exactly when local variables were changed.

What makes **PySnooper** stand out from all other code intelligence tools? You can use it in your shitty, sprawling enterprise codebase without having to do any setup. Just slap the decorator on, as shown below, and redirect the output to a dedicated log file by specifying its path as the first argument.

## Example

We're writing a function that converts a number to binary, by returning a list of bits. Let's snoop on it by adding the `@pysnooper.snoop()` decorator:

```python
import pysnooper

@pysnooper.snoop()
def number_to_bits(number):
    if number:
        bits = []
        while number:
            number, remainder = divmod(number, 2)
            bits.insert(0, remainder)
        return bits
    else:
        return [0]

number_to_bits(6)
```
The output to stderr is:

![](https://i.imgur.com/TrF3VVj.jpg)

Or if you don't want to trace an entire function, you can wrap the relevant part in a `with` block:

```python
import pysnooper
import random

def foo():
    lst = []
    for i in range(10):
        lst.append(random.randrange(1, 1000))

    with pysnooper.snoop():
        lower = min(lst)
        upper = max(lst)
        mid = (lower + upper) / 2
        print(lower, mid, upper)

foo()
```

which outputs something like:

```
New var:....... i = 9
New var:....... lst = [681, 267, 74, 832, 284, 678, ...]
09:37:35.881721 line        10         lower = min(lst)
New var:....... lower = 74
09:37:35.882137 line        11         upper = max(lst)
New var:....... upper = 832
09:37:35.882304 line        12         mid = (lower + upper) / 2
74 453.0 832
New var:....... mid = 453.0
09:37:35.882486 line        13         print(lower, mid, upper)
Elapsed time: 00:00:00.000344
```

## Features

If stderr is not easily accessible for you, you can redirect the output to a file:

```python
@pysnooper.snoop('/my/log/file.log')
```

You can also pass a stream or a callable instead, and they'll be used.

See values of some expressions that aren't local variables:

```python
@pysnooper.snoop(watch=('foo.bar', 'self.x["whatever"]'))
```

Show snoop lines for functions that your function calls:

```python
@pysnooper.snoop(depth=2)
```

**See [Advanced Usage](https://github.com/cool-RR/PySnooper/blob/master/ADVANCED_USAGE.md) for more options.** <------


## Installation with Pip

The best way to install **PySnooper** is with Pip:

```console
$ pip install pysnooper
```

## Other installation options

Conda with conda-forge channel:

```console
$ conda install -c conda-forge pysnooper
```

Arch Linux:

```console
$ yay -S python-pysnooper
```

Fedora Linux:

```console
$ dnf install python3-pysnooper
```


## Citing PySnooper

If you use PySnooper in academic work, please use this citation format:

```bibtex
@software{rachum2019pysnooper,
    title={PySnooper: Never use print for debugging again},
    author={Rachum, Ram and Hall, Alex and Yanokura, Iori and others},
    year={2019},
    month={jun},
    publisher={PyCon Israel},
    doi={10.5281/zenodo.10462459},
    url={https://github.com/cool-RR/PySnooper}
}
```


## License

Copyright (c) 2019 Ram Rachum and collaborators, released under the MIT license.


## Media Coverage

[Hacker News thread](https://news.ycombinator.com/item?id=19717786)
and [/r/Python Reddit thread](https://www.reddit.com/r/Python/comments/bg0ida/pysnooper_never_use_print_for_debugging_again/) (22 April 2019)
