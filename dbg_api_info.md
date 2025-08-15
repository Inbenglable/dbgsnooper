# Dynamic Debugging APIs

We provides three runtime debugging APIs for inspecting methods, variables, and method call structures during test execution. We have deployed it as CLI for you to use.

## 1. `trace_method`

**Description**
Traces the execution of a specified method, showing its input arguments, internal state changes, and return value.

**Arguments**

| Name              | Required | Description                        |
| ----------------- | -------- | ---------------------------------- |
| `--observed_file` | Yes      | Path to the source file to observe |
| `--test_file`     | Yes      | Path to the test file to run       |
| `--method_name`   | Yes      | Target method name                 |

**Example**

```bash
trace_method --observed_file my_module.py --test_file test_my_module.py --method_name process_data
```

---

## 2. `trace_var`

**Description**
Traces the value changes of a specific global or local variable during execution.

**Arguments**

| Name              | Required | Description                                          |
| ----------------- | -------- | ---------------------------------------------------- |
| `--observed_file` | Yes      | Path to the source file to observe                   |
| `--test_file`     | Yes      | Path to the test file to run                         |
| `--var_name`      | Yes      | Variable name to trace                               |
| `--lineno`        | Yes      | Line number where the variable is defined or updated |

**Example**

```bash
trace_var --observed_file my_module.py --test_file test_my_module.py --var_name result --lineno 42
```

---

## 3. `call_graph`

**Description**
Generates a call graph of the target method and its next two levels of calls, including method names, input argument names/values, and return values.

**Arguments**

| Name              | Required | Description                        |
| ----------------- | -------- | ---------------------------------- |
| `--observed_file` | Yes      | Path to the source file to observe |
| `--test_file`     | Yes      | Path to the test file to run       |
| `--method_name`   | Yes      | Target method name                 |

**Example**

```bash
call_graph --observed_file my_module.py --test_file test_my_module.py --method_name process_data
```