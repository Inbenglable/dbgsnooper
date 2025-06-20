import os
import runpy
import sys
import argparse
import traceback
import dbgsnooper  

def debugging_test_execution_wrapper(test_path, observed_file,start_Line, end_line, depth=1, loop=None, depth_expanded=True):
    test_path = os.path.abspath(test_path)
    dir_path = os.path.dirname(test_path)
    os.chdir(dir_path)
    if dir_path not in sys.path:
        sys.path.insert(0, dir_path)
    
    @dbgsnooper.snoop(observed_file=observed_file,start_line=start_Line,end_line=end_line, depth=depth, loop=loop, depth_expanded=depth_expanded)
    def wrapped_execute():
        runpy.run_path(test_path, run_name="__main__")
    try:
        wrapped_execute()
    except Exception as e:
        print(f"Error occurred during script execution:{e}")
        traceback.print_exc()

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--test_path", type = str, required=True)
    # parser.add_argument("--file-scope-dict", required=True)
    parser.add_argument("--observed_file", type = str, required=True)
    parser.add_argument("--start_line", type = int, required=True)
    parser.add_argument("--end_line", type = int, required=True)
    parser.add_argument("--depth", type=int, default=1)
    parser.add_argument("--loop", type=int, default=None)
    parser.add_argument("--no_depth_expanded", action="store_false", help="Disable depth expansion")
    args = parser.parse_args()
    

    # file_scope_dict = json.loads(args.file_scope_dict)
    # new_file_scope_dict = {}
    # for file_path in file_scope_dict:
    #     new_file_path = os.path.abspath(file_path)
    #     new_file_scope_dict[new_file_path] = file_scope_dict[file_path]
    observed_file = os.path.abspath(args.observed_file)
        
    debugging_test_execution_wrapper(args.test_path, args.observed_file, args.start_line, args.end_line, args.depth, args.loop, args.no_depth_expanded)

    # debugging_test_execution_wrapper('/data/SWE/SRC/approach/tmp/testbed/astropy__astropy-12907/astropy__astropy__4.3/debugging_test.py'\
    # , {'/data/SWE/SRC/approach/tmp/testbed/astropy__astropy-12907/astropy__astropy__4.3/astropy/modeling/core.py': (57, 57)}, 1, 0)