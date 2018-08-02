# antlr4_html2latex  
HTML to LaTeX converter using antlr4.  
Author: Akira Hakuta,  Date: 2018/08/01       

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
> python.exe antlr4_html2latex.py example\sample1.html

This is antlr4_html2latex version 0.5.

antlr4_html2latex creates 'sample1.tex'.
```
```
> python.exe antlr4_html2latex.py example\sample2.html -m MOD

This is antlr4_html2latex version 0.5.

modifying html file (insert 'optional tags' except p tag) ....

paired tag error. delete: line = 67, column = 1, </div>

paired tag error {'name':[number of opening tags, number of closing tags],...}
 {'span': [2, 1]}

insert tags:
line = 22, column = 6, </li>
line = 23, column = 3, </li>
line = 24, column = 6, </li>
line = 27, column = 6, </li>
line = 28, column = 3, </li>
line = 29, column = 5, </li>
line = 38, column = 3, </td></tr>
line = 40, column = 4, </th>
line = 45, column = 6, </td>
line = 46, column = 4, </td></tr>
line = 47, column = 9, </td>
line = 55, column = 3, </dd>
line = 56, column = 3, </dt>
line = 64, column = 30, </rt>
line = 65, column = 5, </rp>

modifying html file (insert  p tag) ....

insert p tag:
line = 15, column = 2, </p>
line = 17, column = 1, </p>

delete paired tags:  ['span']

antlr4_html2latex creates 'sample2.tex'.
```

## Options 

```
> python.exe antlr4_html2latex.py -h
usage: antlr4_html2latex.py [-h] [-v] [-e ENCODING] [-m MOD] [-a NOA]
                            [-i NOIMG] [-t NOTBL]
                            filename

positional arguments:
  filename     set filename, for example test.html

optional arguments:
  -h, --help   show this help message and exit
  -v           show program's version number and exit
  -e ENCODING  -e ascii or -e euc-jp or ... ,default = utf-8
  -m MOD       modifying html file (optional tags, ..), default = NOMOD
  -a NOA       converting anchor to href, default = A
  -i NOIMG     converting img to includegraphics, default = IMG
  -t NOTBL     converting table to tabular ,default = TBL
```
#### html2latex.csv  

Please add and change.  

```
paired tag --> latex 
[pair_tag], [p], [], [\\par\n]
[pair_tag], [li], [\\item ] , [\n]
[pair_tag], [ol], [\n\\begin{enumerate}\n] , [\n\\end{enumerate}]
[pair_tag], [ul], [\n\\begin{itemize}\n],[\n\\end{itemize}]
[pair_tag], [dt], [],[\\newline\n]
[pair_tag], [dd], [~~~],[\\newline\n]
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
> antlr4_tex2sym.exe example\sample1.html
> antlr4_tex2sym.exe example\sample2.html -m MOD
```

------

### in japanese

#### antlr4_html2latex は HTMLのコードを解析して、  LaTeXのコードに変換する Python のツールです。  
同様のツールは、既にあるのですが、  
The Definitive ANTLR 4 Reference (by Terence Parr)    12.4 Parsing and Lexing  XML  
を参考に、いちからプログラムを書いてみました。  
完成したものを実行してみると、  
`line 3610:218 mismatched input '<EOF>' expecting '<'`  
と表示されることがあります。  

原因と思われるのは、  

1. タグが省略 されている。特に終了タグ。 ( optional tags : li, dd, tr, p, .... ) 
2. 終了タグが多い 。  
3. 終了タグが少ない。例えば、`</div>`  

対応策  
1. コードを読んで、適当な場所に closing tag を挿入   ( html, body, head を除く )    
2. 分かった時点で、closing tag を単純に削除 
3. error message を表示し、該当する paired tag をすべて削除     
```
> python.exe antlr4_html2latex.py example\sample2.html -m MOD
```
で確認してください。  
pdflatex.exe で pdf が作れないこともあります。  
その時は、  
option  ` -a NOA -i NOIMG　`を付けて実行。  
`\href, \includegraphics` なしで、LaTeX のコードを生成します。  
LaTeX の tabular はページを超えて表示することはできません。  
`-t NOTBL` とすると、  
'tabular' 形式ではなく、paired tag 'table' 内の TEXT のみ出力します。  

####  実行ファイル 、ソースコード について   
releases の各 zip fileをクリックして解凍。  
