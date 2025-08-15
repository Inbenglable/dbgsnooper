import os
import runpy
import sys
import argparse
import traceback
from typing import List, Tuple
from .ast_env_boot import run_get_statement_range, run_get_belonging_method

def debugging_test_execution_wrapper(test_path, name, is_global = False, var_path=None, lineno = None):
    test_path = os.path.abspath(test_path)
    dir_path = os.path.dirname(test_path)
    if var_path:
        var_path = os.path.abspath(var_path)
        
    os.chdir(dir_path)
    if dir_path not in sys.path:
        sys.path.insert(0, dir_path)
    
    
    try:
        trace = VarTracer(name, test_path, is_global, var_path, lineno)
        sys.settrace(trace)
        runpy.run_path(test_path, run_name="__main__")
        print('\n\n'+'='*50+ '\n\n')
        print(f"Variable '{name}' history:")
        print(trace.construct_history_str())
    except Exception as e:
        print(f"Error occurred during script execution:\n{e}")
        # traceback.print_exc()

        
        

class VarTracer:
    def __init__(self, varname: str, test_path: str, is_global = False, var_path: str = None, lineno: int = None):
        self.trace_start = False
        self.test_path = os.path.abspath(test_path)
        self.varname = varname
        self.history: List[Tuple[str, int, object, str]] = []
        self.last_value = None
        self.frame_locs = dict()
        self.is_global = is_global
        
        self.var_path = os.path.abspath(var_path) if var_path else None
        self.lineno = lineno
        self.start_line = None
        self.end_line = None
        self.observed_code = None

        self.loop = 4
        self.frame_line_executed = {}
        
        if self.var_path and self.lineno and not self.is_global:
            assert os.path.exists(self.var_path), f"Variable path {self.var_path} does not exist"
            ## assert the varname in the file line
            with open(self.var_path, 'r') as f:
                lines = f.read().splitlines()
            assert self.lineno <= len(lines), f"Line number {self.lineno} exceeds the number of lines in {self.var_path}"
            assert self.varname in lines[self.lineno - 1], f"Variable '{self.varname}' not found in line {self.lineno} of {self.var_path}"
            self.start_line, self.end_line = run_get_belonging_method(self.var_path, self.lineno)
        

        
    def __call__(self, frame, event, arg):
        file = frame.f_code.co_filename
                
        if not self.trace_start:
            if file != self.test_path:
                return None
            else:
                self.trace_start = True
        
        if self.var_path:
            if not file.startswith(self.var_path):
                return None

        lineno = frame.f_lineno
        
        if not self.is_global:
            if not (self.start_line <= lineno <= self.end_line):
                return self
            
            if not self.observed_code and event != 'call':
                return self
            else:
                self.observed_code = frame.f_code
        
        self.record_frame_line_executed(frame)
        if self.is_global:
            g = frame.f_globals
            observed_vars = g
        else:
            l = frame.f_locals
            observed_vars = l
        
        
        if self.varname not in observed_vars:
            self.last_value = None
            self.frame_locs[frame] = (file, lineno)
            return self
        
            
            
        current_value = resolve_variable(observed_vars[self.varname])
        if current_value != self.last_value:
            source_file, source_lineno = self.frame_locs.get(frame)

            code, end_line = self._get_full_statement(source_file, source_lineno)
            if end_line != source_lineno:
                scope = f'{source_lineno}-{end_line}'
            else:
                scope = str(source_lineno)

            if self.is_skip_loop(frame, source_lineno):
                self.history.append((source_file, scope, current_value, code, 'loop'))
            else:
                self.history.append((source_file, scope, current_value, code))

        self.last_value = current_value
        self.frame_locs[frame] = (file, lineno)
        return self
        

    def _get_full_statement(self, filename: str, lineno: int):
        try:
            start, end = run_get_statement_range(filename, lineno)
            with open(filename, 'r', encoding='utf-8') as f:
                lines = f.read().splitlines()
            return '\n'.join(lines[start - 1:end]), end
        except Exception as e:
            return f"<error extracting statement: {e}>", None

    def construct_history_str(self):
        str_list = []
        for i in range(len(self.history)):
            curr_item = self.history[i]
            if len(curr_item) == 4:
                filename, scope, value, code = curr_item
                str_list.append(f"Location: {filename}: {scope}\nCode:\n```\n{code}\n```\nValue: {value}\n")
            elif len(curr_item) == 5:
                filename, scope, value, code, _ = curr_item
                next_item = self.history[i + 1] if i + 1 < len(self.history) else None
                if len(next_item) == 4:
                    str_list.append(f"Location: {filename}: {scope}\nCode:\n```\n{code}\n```\nValue: {value}\n")
                elif i-1 >= 0 and len(self.history[i-1]) == 4:
                        str_list.append(f"...Skipping repeated variable modification details in loop......\n")
        return '\n'.join(str_list)


    def is_skip_loop(self, frame, lineno, max_loop_times = None):
        looped_times = 0
        max_loop_times = max_loop_times if max_loop_times is not None else self.loop

        if frame in self.frame_line_executed and lineno in self.frame_line_executed[frame]:
            looped_times = self.frame_line_executed[frame][lineno]
        else:
            return False
        if looped_times >= max_loop_times:
            return True
        return False

        
    def record_frame_line_executed(self, frame, lineno = None):
        lineno = lineno if lineno is not None else frame.f_lineno
        if frame not in self.frame_line_executed:
            self.frame_line_executed[frame] = {}
        if lineno not in self.frame_line_executed[frame]:
            self.frame_line_executed[frame][lineno] = 0
        self.frame_line_executed[frame][lineno] += 1



import inspect
import types

def resolve_variable(val):
    value = []
    if isinstance(val, list):
        for item in val:
            value.append(parse_refer_value(item))
    elif isinstance(val, dict):
        for key, item in val.items():
            value.append(f"{key}: {parse_refer_value(item)}")
    elif isinstance(val, tuple):
        value = [parse_refer_value(item) for item in val]
    
    elif isinstance(val, set):
        value = [parse_refer_value(item) for item in val]
        
    else:
        value = [parse_refer_value(val)]
    return '\n'.join(value)
   



def parse_refer_value(val):
    if isinstance(val, (int, float, str, bool, type(None))):
        return f"[Value] {repr(val)}"

    elif isinstance(val, types.FunctionType):
        try:
            file = inspect.getsourcefile(val)
            lines, start_line = inspect.getsourcelines(val)
            def_line = lines[0].strip()
            return f"[Function] {file}:{start_line} -> {def_line}"
        except Exception as e:
            return f"[Function] <uninspectable> ({type(val).__name__}): {e}"

    elif isinstance(val, object):
        cls_name = val.__class__.__name__
        attrs = {k: getattr(val, k) for k in dir(val)
                 if not k.startswith("__") and not inspect.ismethod(getattr(val, k, None))}
        attr_lines = [f"  - {k}: {repr(v)}" for k, v in attrs.items()]
        attr_display = "\n".join(attr_lines) if attr_lines else "  (no public attributes)"
        return f"[Object] Instance of '{cls_name}':\n{attr_display}"

    else:
        return f"[Other] {type(val).__name__}: {repr(val)}"
    


def judge_global(var_name: str, test_path: str, file_path: str = None, lineno: str = None):
    class Tracer:
        def __init__(self, varname: str, test_path: str, var_path: str = None, start_line: int = None, end_line: int = None):
            self.trace_start = False
            self.test_path = os.path.abspath(test_path)
            self.varname = varname
            self.var_path = os.path.abspath(var_path) if var_path else None
            self.start_line = start_line
            self.end_line = end_line
            self.observed_code = None
            
            self.is_global_scope = True
            
        def __call__(self, frame, event, arg):
            file = frame.f_code.co_filename
            if not self.trace_start:
                if file != self.test_path:
                    return None
                else:
                    self.trace_start = True
            

            if not file.startswith(self.var_path):
                return None

            lineno = frame.f_lineno

            if not (self.start_line <= lineno <= self.end_line):
                return self
            
            if not self.observed_code and event != 'call':
                return self
            else:
                self.observed_code = frame.f_code
                
            local_vars = frame.f_locals
            if self.varname not in local_vars:
                return self
            else:
                self.is_global_scope = False
        
    def execution_and_trace(test_path, name, var_path = None, start_line = None, end_line = None):
        test_path = os.path.abspath(test_path)
        dir_path = os.path.dirname(test_path)
        if var_path:
            var_path = os.path.abspath(var_path)
            
        os.chdir(dir_path)
        if dir_path not in sys.path:
            sys.path.insert(0, dir_path)
        
        
        try:
            trace = Tracer(name, test_path, var_path, start_line, end_line)
            sys.settrace(trace)
            runpy.run_path(test_path, run_name="__main__")
            sys.settrace(None)
            return trace.is_global_scope
            
        except Exception as e:
            traceback.print_exc()
        

    file_path = os.path.abspath(file_path) if file_path else None
    test_path = os.path.abspath(test_path)
    
    if file_path and lineno:
        if os.path.exists(file_path):
            with open(file_path, 'r') as f:
                lines = f.read().splitlines()
            if lineno <= len(lines) and var_name in lines[lineno - 1]:                
                start_line, end_line = run_get_belonging_method(file_path, lineno)
                if start_line and end_line:
                    return execution_and_trace(test_path=test_path, name=var_name, var_path=file_path, start_line=start_line, end_line=end_line)
                else:
                    return True
    return False 


def trace_var(test_path, var_path, name, lineno):
    
    # is_global = judge_global(args.name, args.test_path, args.var_path, args.lineno)
    is_global = judge_global(name, test_path, var_path, lineno)
    # debugging_test_execution_wrapper(args.test_path, args.name, is_global, args.var_path, args.lineno)
    debugging_test_execution_wrapper(test_path, name, is_global, var_path, lineno)
