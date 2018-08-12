# python.exe setup.py 
import cx_Freeze
import sys

sys.argv.append('build')
# python.exe setup.py build

base = None
includes = []
include_files = ['gen', 'mod_gen', 'example', 'html2latex.csv', 'readme.txt']
excludes = []
packages = ['antlr4']
executables = [cx_Freeze.Executable(script="antlr4_html2latex.py",targetName="antlr4_html2latex.exe", base = base),]

cx_Freeze.setup(
    name = "antlr4_html2latex",
    options = {"build_exe": 
        {"build_exe":"antlr4_html2latex_binary-0.6/","includes":includes, "include_files": include_files, "excludes": excludes,"packages": packages}},
    version = "0.6",
    description = "HTML to LaTeX Converter using antlr4",
    executables = executables)
