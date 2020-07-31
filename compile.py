from cx_Freeze import setup, Executable
import os.path

PYTHON_INSTALL_DIR = os.path.dirname(os.path.dirname(os.__file__))
os.environ['TCL_LIBRARY'] = os.path.join(PYTHON_INSTALL_DIR, 'tcl', 'tcl8.6')
os.environ['TK_LIBRARY'] = os.path.join(PYTHON_INSTALL_DIR, 'tcl', 'tk8.6')

include_files = [os.path.join(PYTHON_INSTALL_DIR, 'DLLs', 'tk86t.dll'),
		 os.path.join(PYTHON_INSTALL_DIR, 'DLLs', 'tcl86t.dll'),
		 'icon/']

setup(
    name='OWL Easy Commands',
    description='GUI Command Prompt',
    version='1.0',
    options={'build_exe': {'include_files': include_files}},
    executables=[Executable('project.py', 
			    targetName='OWL.exe',
			    copyright='Copyright (C) OWL 2018')]
)
