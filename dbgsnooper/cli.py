import os
import runpy
import sys
import argparse
import traceback
import dbgsnooper 

def dbgsnooper_execution_wrapper(test_path, observed_file,start_Line, end_line, call_graph_mode = False):
    test_path = os.path.abspath(test_path)
    dir_path = os.path.dirname(test_path)
    os.chdir(dir_path)
    if dir_path not in sys.path:
        sys.path.insert(0, dir_path)

    @dbgsnooper.snoop(observed_file=observed_file,start_line=start_Line,end_line=end_line, call_graph_mode = call_graph_mode)
    def wrapped_execute():
        runpy.run_path(test_path, run_name="__main__")
    try:
        wrapped_execute()

        if call_graph_mode:
            call_graph_data_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'call_graph_data.json')
            print(render_call_tree(call_graph_data_path))
            os.remove(call_graph_data_path)
    except Exception as e:
        print(f"Error occurred during script execution:{e}")
        traceback.print_exc()

    

def build_trace_method_parser(parser):
    parser.add_argument('--observed_file', required=True)
    parser.add_argument('--test_file', required=True)
    parser.add_argument('--method_name', required=True)
    return parser


def build_trace_var_parser(parser):
    parser.add_argument('--observed_file', required=True)
    parser.add_argument('--test_file', required=True)
    parser.add_argument('--var_name', required=True)
    parser.add_argument('--lineno', type=int, required=True)
    return parser


def build_call_graph_parser(parser):
    parser.add_argument('--observed_file', required=True)
    parser.add_argument('--test_file', required=True)
    parser.add_argument('--method_name', required=True)
    return parser

from .trace_var import trace_var
from .render_call_tree import render_call_tree
from .ast_env_boot import run_get_method_range

def main():
    prog = sys.argv[0].split('/')[-1]

    # === 单命令模式 ===
    if prog in ('trace_method', 'trace_var', 'call_graph'):
        args = sys.argv[1:]
        if prog == 'trace_method':
            parser = build_trace_method_parser(argparse.ArgumentParser(prog='trace_method'))
            parsed = parser.parse_args(args)
            method_start_line, method_end_line = run_get_method_range(parsed.observed_file, parsed.method_name)
            dbgsnooper_execution_wrapper(parsed.test_file, parsed.observed_file, method_start_line, method_end_line)

        elif prog == 'trace_var':
            parser = build_trace_var_parser(argparse.ArgumentParser(prog='trace_var'))
            parsed = parser.parse_args(args)
            trace_var(parsed.test_file, parsed.observed_file, parsed.var_name, parsed.lineno)

        elif prog == 'call_graph':
            parser = build_call_graph_parser(argparse.ArgumentParser(prog='call_graph'))
            parsed = parser.parse_args(args)
            method_start_line, method_end_line = run_get_method_range(parsed.observed_file, parsed.method_name)
            dbgsnooper_execution_wrapper(parsed.test_file, parsed.observed_file, method_start_line, method_end_line, call_graph_mode = True)

        return



if __name__ == "__main__":
    main()
    
