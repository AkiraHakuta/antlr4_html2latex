# antlr4_html2latex  
Converter html into latex by using antlr4.  
Author:Akira Hakuta,  Date: 2018/07/28   

## Installation (windows)  
Python3: <https://www.python.org/downloads/windows/>   
ANTLR : <http://www.antlr.org>  (antlr4-python3-runtime 4.7)   
cx_Freeze: <https://anthony-tuininga.github.io/cx_Freeze/>    
```
python3 (python-3.6.2.exe)
pip install antlr4-python3-runtime 
pip install cx_Freeze
```


## Usage
```
> python.exe antlr4_html2latex.py sample1.html

This is antlr4_html2latex version 0.5.

antlr4_html2latex creates 'sample1.tex'.
```
```
> python.exe antlr4_html2latex.py sample2.html -m MOD
line 89:7 mismatched input '<EOF>' expecting '<'

This is antlr4_html2latex version 0.5.

modifying html file (insert 'optional tags' except p tag) ....

paired tag error. delete: line=67,column=1,</div>

paired tag error {'name':[opening tags number, closing tags number],...} ignore!
 {'span': [2, 1]}

insert tag:
line = 22,column = 6, </li>
line = 23,column = 3, </li>
line = 24,column = 6, </li>
line = 27,column = 6, </li>
line = 28,column = 3, </li>
line = 29,column = 5, </li>
line = 38,column = 3, </td></tr>
line = 40,column = 4, </th>
line = 45,column = 6, </td>
line = 46,column = 4, </td></tr>
line = 47,column = 9, </td>
line = 55,column = 3, </dd>
line = 56,column = 3, </dt>
line = 64,column = 30, </rt>
line = 65,column = 5, </rp>

modifying html file (insert  p tag) ....

insert p tag:
line = about 15,column = about 2,</p>
line = about 17,column = about 1,</p>

antlr4_html2latex creates 'sample2.tex'.
```

## Options 

```
> python.exe antlr4_html2latex.py -h
usage: antlr4_html2latex.py [-h] [-v] [-t NOTABLE] [-e ENCODE] [-m MOD]
                            [-a NOANCHOR] [-i NOIMG]
                            filename

positional arguments:
  filename     set filename, for example test.html

optional arguments:
  -h, --help   show this help message and exit
  -v           show program's version number and exit
  -t NOTABLE   converting table to tabular ,default = TABLE
  -e ENCODE    -e ascii or -e euc-jp or ... ,default = utf-8
  -m MOD       modifying html codes (optional tags, ..), default = NOMOD
  -a NOANCHOR  converting anchor to href, default = ANCHOR
  -i NOIMG     converting img to includegraphics, default = IMG
```
#### html2latex.csv  

Please add and change.  

```
paired tag --> latex 
[pair_tag], [p], [], [\\par\n]
[pair_tag], [li], [\\item ] , [\n]
[pair_tag], [ol], [\n\\begin{enumerate}\n] , [\n\\end{enumerate}]
[pair_tag], [ul], [\n\\begin{itemize}\n],[\n\\end{itemize}]
[pair_tag], [dt], [],[\\par\n]
[pair_tag], [dd], [~~~],[\\par\n]
......

entity code --> latex
[sp_text], [&alpha;], [$\\alpha$]
[sp_text], [&beta;], [$\\beta$]
[sp_text], [&gamma;], [$\\gamma$]
[sp_text], [&dagger;], [$\\dagger$]
.......

[sp_text], [&#176;], [$^\\circ$]
[sp_text], [&#8211;], [--]
[sp_text], [&#047;], [/]

[sp_text], [&], [\\verb|&|]
[sp_text], [$], [\\verb|$|]
```


## antlr4_tex2sym.exe

If you want to antlr4_tex2sym.py to .exe files,  
` python.exe setup.py `

#### Usage

```
> antlr4_tex2sym.exe sample1.html
> antlr4_tex2sym.exe sample2.html -m MOD
```



------



### in japanese

#### antlr4_html2latex は HTMLのコードを解析して、  LaTeXのコードに変換する Python のツールです。  
同様のツールは、既にあるのですが、  
The Definitive ANTLR 4 Reference (by Terence Parr)    12.4 Parsing and Lexing  XML  
を参考に、いちからプログラムを書いてみました。  
完成したプログラムを実行してみると、error となることがあります。  
原因と思われるのは、  

1. タグが省略 されている。特に終了タグ。 ( optional tags : li, dd, tr, p, .... ) 
2. 終了タグが多い 。  
3. 終了タグが少ない。例えば、`</div>`  

対応策  
1. コードを読んで、適当な場所に closing tag を挿入   ( html, body, head を除く )    
2. 分かった時点で、closing tag を単純に削除 
3. error message を表示するのみ   
```
> python.exe antlr4_html2latex.py sample2.html -m MOD
```
で確認してください。  
pdflatex.exe で pdf を作れないこともあります。 
その時は、  
option  ` -a NOANCHOR -i NOIMG　`を付けて実行。
`\href, \includegraphics` なしで、LaTeX のコードを生成します。  
不備なところが多々あります。  
このツールはまだ試作段階です。

####  実行ファイル 、ソースコード について   
releases の各 zip fileをクリックして解凍。  
