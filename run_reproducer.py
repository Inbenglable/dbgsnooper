import runpy
import sys
from io import StringIO
import dbgsnooper
import traceback
import os

def execute_with_output(script_path, file_scope_dict, depth=None, loop= None):
    script_path = os.path.abspath(script_path) # 绝对化路径
    @dbgsnooper.snoop(file_scope_dict=file_scope_dict, depth=depth, loop = loop)
    def wrapped_execute():
        runpy.run_path(script_path, run_name="__main__")
    try:
        # 执行脚本
        wrapped_execute()
    except Exception as e:
        print(f"Error occurred during script execution:{e}")
        traceback.print_exc()


if __name__ == "__main__":
    script_path = '/data/swe-fl/TMP/testbed/astropy__astropy-12907/./reproducer.py'
    
    # Create a dictionary to store the observed file line scope(s)
    file_scope_dict = {}
    observed_file = '/data/swe-fl/TMP/testbed/astropy__astropy-12907/astropy/modeling/separable.py'
    start_line=290
    end_line=311
    
    file_scope_dict[observed_file] = (start_line, end_line)
    depth=1
    execute_with_output(script_path, file_scope_dict, depth)
