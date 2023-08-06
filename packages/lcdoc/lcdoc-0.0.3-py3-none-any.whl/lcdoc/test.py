
from __future__ import annotations
from ast import parse
import pathlib
import time

#from ast import parse
#from sqlite3 import Cursor
#from types import NoneType
from typing import Iterator
#import typing

# https://pypi.org/project/libclang/
# https://libclang.readthedocs.io/en/latest/
# https://sudonull.com/post/907-An-example-of-parsing-C-code-using-libclang-in-Python
#import clang.cindex



#from .lcdoc import *
from lcdoc import *
from cxx import *
from cxx_generator import *
from cxx_target import *
from WebsiteGenerator import WebsiteGenerator

#from src.Declaration import Declaration



#index : clang.cindex.Index = clang.cindex.Index.create()
#tu : clang.cindex.TranslationUnit = index.parse("D:/LUCA/LUCE_STRUTTURATA/develop/StructuredLight/StructuredLight/include/StructuredLight/SLScanner/scans.hpp")




parser = DocumentParser()
#doc = ParsedDocument()
#doc.AST = parser.parse("D:/LUCA/LUCE_STRUTTURATA/develop/StructuredLight/StructuredLight/include/StructuredLight/SLScanner/scans.hpp")
#parser.includes.append(pathlib.Path.absolute(pathlib.Path("./include")))
parser.includes.append("./example/project/include")
parser.inFileOnly = False
doc : ParsedDocument | None = None
doc = parser.parse("./example/project/src/test.cpp")
try :
    #doc = parser.parse("./out/test.cpp")
    pass
except ValueError as ve:
    print("Value Error: ", ve)
except clang.cindex.LibclangError as e:
    print("error: ", e)
except clang.cindex.CompilationDatabaseError as e2:
    print(e2)
except :
    print("error")

#doc.findDeclarations()
#print(doc.declarations)
print(doc.symbolTable.symbols)

generator = Generator()
#print(generator.html(doc))
#with open('./out/index.html', 'wb') as f:
#    f.write(generator.html(doc).encode('utf-8'))

gen = HtmlGenerator()
#for s in doc.symbolTable.symbols :
#    print(gen.symbolHtmlName(s))

gen.add_doc(doc)
#with open('./out/index2.html', 'wb') as f:
    #f.write(gen.tmp_page(doc).encode('utf-8'))
#    pass
gen.write_to("./example/out")

while True :
    gen.doc_dir("./doc", "./doc_out")
    time.sleep(10)

#show_list_CursorKind()