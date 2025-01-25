import runpy
import sys
from io import StringIO
import dbgsnooper
import traceback

def execute_with_output(script_path, observed_file, start_line=None, end_line=None, depth=None, loop= None):
    @dbgsnooper.snoop(observed_file=observed_file, start_line=start_line, end_line=end_line, depth=depth, loop = loop)
    def wrapped_execute():
        runpy.run_path(script_path, run_name="__main__")
    try:
        # 执行脚本
        wrapped_execute()
    except Exception as e:
        print(f"Error occurred during script execution:{e}")
        traceback.print_exc()


if __name__ == "__main__":
    script_path = '/data/swe-fl/TMP/testbed/astropy__astropy-12907/reproducer.py'
    observed_file = '/data/swe-fl/TMP/testbed/astropy__astropy-12907/astropy/modeling/separable.py'
    start_line=290
    end_line=311
    depth=2
    execute_with_output(script_path, observed_file, start_line, end_line, depth)

