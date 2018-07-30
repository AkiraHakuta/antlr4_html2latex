# python.exe setup.py 
import cx_Freeze
import sys

sys.argv.append('build')
# python.exe setup.py build

base = None
includes = []
include_files = ['gen', 'mod_gen', 'html2latex.csv', 'sample1.html', 'sample2.html', 'cat.png', 'readme.txt']
excludes = []
packages = ['antlr4']
executables = [cx_Freeze.Executable(script="antlr4_html2latex.py",targetName="antlr4_html2latex.exe", base = base),]

cx_Freeze.setup(
    name = "antlr4_html2latex",
    options = {"build_exe": 
        {"build_exe":"antlr4_html2latex_binary/","includes":includes, "include_files": include_files, "excludes": excludes,"packages": packages}},
    version = "0.5",
    description = "Html to LaTeX Converter using antlr4",
    executables = executables)
