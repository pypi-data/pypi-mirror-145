
from __future__ import annotations
from os import link, path
import os

from cxx import *
from lcdoc import *
import cxx
from doc_utils import ParamDocBlock
from WebsiteGenerator import WebsiteGenerator

TAG_NAMESPACE = "code-namespace"
TAG_CLASS = "code-class"
TAG_FUNCTION = "code-function"

class SymbolsTree :

    symbol : Symbol | None = None
    children : list[SymbolsTree]

    def __init__(self) -> None:
        self.children = []

    def insertSymbolTree(self, root : Symbol, fileName : str) -> SymbolsTree :
        subTree : SymbolsTree | None = None
        
        # find the correct subtree
        for child in self.children :
            if root.mangledName == typing.cast(Symbol, child.symbol).mangledName :
                subTree = child
                break
        
        # if not found, add a subtree
        if not subTree :
            subTree = SymbolsTree()
            subTree.symbol = root
            self.children.append(subTree)

        # if it is declared in this file, force substitution
        if root.declaration :
            # TODO merge docs
            if root.declaration.node.file() == fileName :
                subTree.symbol = root

        for childSymbol in root.children :
            #print(childSymbol)
            subTree.insertSymbolTree(childSymbol, fileName)

        return subTree

    def fixParents(self) -> None :
        for childTree in self.children :
            if self.symbol :
                assert childTree.symbol
                childTree.symbol.addToParent(self.symbol)
            childTree.fixParents()


class HtmlGenerator(WebsiteGenerator) :

    symbolTree : SymbolsTree

    def __init__(self) -> None:
        super().__init__()
        self.symbolTree = SymbolsTree()

    def add_doc(self, doc : ParsedDocument) -> None :
        for root in doc.symbolTable.root_symbols :
            self.symbolTree.insertSymbolTree(root, doc.filePath)
            self.symbolTree.fixParents()
        pass

    def generate_symbol_href(self, symbol : Symbol, final : bool = True) -> str :
        href : str = ""

        pre_v : str = "symbols"
        if symbol.parent :
            pre_v = self.generate_symbol_href(symbol.parent, False)

        if isinstance(symbol, NamespaceSymbol) :
            if final :
                return self.relative_href(path.join(pre_v, symbol.name))
            return path.join(pre_v, symbol.name)

        if isinstance(symbol, StructSymbol) :
            if final :
                return self.relative_href(path.join(pre_v, symbol.name))
            return path.join(pre_v, symbol.name)

        if isinstance(symbol, ClassSymbol) :
            if final :
                return self.relative_href(path.join(pre_v, symbol.name))
            return path.join(pre_v, symbol.name)

        if isinstance(symbol, TypeAliasSymbol) :
            if final :
                return self.relative_href(path.join(pre_v, symbol.name))
            return path.join(pre_v, symbol.name)

        if isinstance(symbol, MethodSymbol) :
            if final :
                return path.join(self.relative_href(pre_v), "#" + self.generete_symbol_id(symbol).replace("?", "%3f"))
            return "#".join([pre_v, symbol.name])

        return "#ERROR"

    def generete_symbol_id(self, symbol : Symbol, pre : str = "") -> str :
        pre_v : str = pre[:]
        #if symbol.parent :
        #    pre_v += self.generete_symbol_id() + "::"

        return pre_v + symbol.mangledName

    def generate_keyword_href(self, ky : str) -> str| list[str] :
        # see https://en.cppreference.com/w/cpp/keyword
        # https://en.cppreference.com/w/cpp/language/structured_binding

        if ky == "const" :
            return [
                "https://en.cppreference.com/w/cpp/keyword/const",
                "https://en.cppreference.com/book/intro/const"
            ]

        if ky == "int" :
            return [
                "https://en.cppreference.com/w/cpp/keyword/int",
                "https://en.cppreference.com/w/cpp/language/types",
            ]

        if ky == "void" :
            return [
                "https://en.cppreference.com/w/cpp/keyword/void",
                "https://en.cppreference.com/w/cpp/language/types",
            ]

        if ky == "class" :
            return [
                "https://en.cppreference.com/w/cpp/keyword/class",
                "https://en.cppreference.com/w/cpp/language/class",
                #"https://en.cppreference.com/w/cpp/language/classes",
                #"https://en.cppreference.com/book/intro/classes",
                #"https://en.cppreference.com/book/class"
            ]

        if ky == "auto" :
            return [
                "https://en.cppreference.com/w/cpp/keyword/auto",
                "https://en.cppreference.com/w/cpp/language/auto",
                "https://docs.microsoft.com/en-us/cpp/cpp/auto-cpp?view=msvc-170"
            ]


        if ky == "&&" or ky == "&" :
            return [
                "https://en.cppreference.com/w/cpp/language/reference",
                "https://en.cppreference.com/book/intro/reference"
            ]

        if ky == "*" :
            return [
                "https://en.cppreference.com/w/cpp/language/pointer",
                "https://en.cppreference.com/book/pointers"
            ]

        return ""

    def tag(self, tagName : str, content : str, data : str = "") -> str :
            if data :
                return f"<{tagName} {data}>{content}</{tagName}>"
            return f"<{tagName}>{content}</{tagName}>"

    def code_tag(self, content : str) -> str :
        return self.tag("code", content, 'class="nohighlight"')
    
    def code_span_tag(self, tagName : str, content : str, href : str | list[str] = "") -> str :
        if isinstance(href, list) :
            links : str = ""
            for h in href :
                links += self.tag("li", self.tag("a", h, f'href="{h}"'))
            tooltiptext : str = self.tag("span", "links:" + self.tag("ol", links), 'class="tooltiptext"')
            # TODO change
            return self.tag(tagName, content + tooltiptext, 'class="tooltip"')

        if href :
            return f"<a class=\"code-link\" href=\"{href}\"><{tagName}>{content}</{tagName}></a>"
        return f"<{tagName}>{content}</{tagName}>"

    def symbolHtmlName(self, symbol : Symbol) :

        if isinstance(symbol, NamespaceSymbol) :
            return self.code_span_tag(TAG_NAMESPACE, symbol.name, self.generate_symbol_href(symbol))

        if isinstance(symbol, StructSymbol) or isinstance(symbol, ClassSymbol) :
            return self.code_span_tag(TAG_CLASS, symbol.name, self.generate_symbol_href(symbol))
        
        if isinstance(symbol, MethodSymbol) :
            return self.code_span_tag(TAG_FUNCTION, symbol.name, self.generate_symbol_href(symbol))

        if isinstance(symbol, TypeAliasSymbol) :
            return self.code_span_tag(TAG_CLASS, symbol.name, self.generate_symbol_href(symbol))

        return "symbolHtmlName_ERROR"

    def symbolCompleteHtmlName(self, symbol : Symbol) -> str :
        if symbol.parent :
            return self.symbolCompleteHtmlName(symbol.parent) + "::" + self.symbolHtmlName(symbol)
        return self.symbolHtmlName(symbol)

    # TODO conetxt
    def type2Html(self, ty : Type) -> str :
        if isinstance(ty, BasicType) :
            if ty.const_qualified :
                return self.keyword2Html("const") + " " + self.keyword2Html(ty.ty)
            return self.keyword2Html(ty.ty)

        if isinstance(ty, RValueRefType) :
            assert ty.to
            if ty.const_qualified :
                return self.keyword2Html("const") + " " + self.type2Html(ty.to) + self.keyword2Html("&&")
            return self.type2Html(ty.to) + self.keyword2Html("&&")

        if isinstance(ty, LValueRefType) :
            assert ty.to
            if ty.const_qualified :
                return self.keyword2Html("const") + " " + self.type2Html(ty.to) + self.keyword2Html("&")
            return self.type2Html(ty.to) + self.keyword2Html("&")

        if isinstance(ty, PointerType) :
            assert ty.to
            if ty.const_qualified :
                return self.keyword2Html("const") + " " + self.type2Html(ty.to) + self.keyword2Html("*")
            return self.type2Html(ty.to) + self.keyword2Html("*")

        # TODO conetxt
        if isinstance(ty, ClassType) :
            assert ty.classSymbol
            if ty.const_qualified :
                return self.keyword2Html("const") + " " + self.symbolCompleteHtmlName(ty.classSymbol)
            return self.symbolCompleteHtmlName(ty.classSymbol)

        if isinstance(ty, TypeAliasType) :
            assert ty.aliasSymbol
            if ty.const_qualified :
                return self.keyword2Html("const") + " " + self.symbolCompleteHtmlName(ty.aliasSymbol)
            return self.symbolCompleteHtmlName(ty.aliasSymbol)

        if isinstance(ty, AutoType) :
            assert ty.deduced
            if ty.const_qualified :
                # TODO span-to-change
                return "(" + self.keyword2Html("const") + " " + self.symbolCompleteHtmlName(ty.deduced) + " " + self.tag("span-to-change", "d.f." + self.tag("span", "<b>d</b>educed <b>f</b>rom", 'class="tooltiptext"'), 'class="tooltip"') + " " + self.keyword2Html("const") + " " + self.keyword2Html("auto") + ")"
            return "(" + self.symbolCompleteHtmlName(ty.deduced) + " d.f. " + self.keyword2Html("auto") + ")"
        
        return "type2Html_ERROR"

    def keyword2Html(self, ky : str) -> str :
        href : str | list[str] = self.generate_keyword_href(ky)

        if ky == "&" or ky == "&&" or ky == "*" :
            # TODO better without span
            if href :
                # TODO change span
                return self.code_span_tag("span-to-change", ky, href)
                return self.tag("a", ky, f'href="{href}" class="code-link"')
            else :
                return ky

        return self.code_span_tag("code-keyword", ky, href)

    def tmp_page(self, doc : ParsedDocument) -> str :
        html : str = ""
        for s in doc.symbolTable.symbols :
            html += self.symbolCompleteHtmlName(s) + "<br>"
        html += "<hr>"
        for s in doc.symbolTable.symbols :
            if isinstance(s, MethodSymbol) :
                ret = typing.cast(cxx.FuncArg, s.ret)
                assert ret.typ
                html += self.type2Html(ret.typ) + " ciao<br>"
        html += "<hr>"
        for s in doc.symbolTable.symbols :
            if s.declaration :
                if s.declaration.node.file() == doc.filePath :
                    html += self.symbolCompleteHtmlName(s) + "<br>"
        return f"""
    <!DOCTYPE html>
    <html lang="en">
    <head class="light-mode">
        <meta charset="UTF-8">
        <meta http-equiv="X-UA-Compatible" content="IE=edge">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Document</title>

        <link rel="stylesheet" href="https://lucaciucci99.com/css/style.css">
        <link rel="stylesheet" href="./style.css">

        <script async src="https://cdn.jsdelivr.net/npm/tex-math@latest/dist/tex-math.js"></script>
    </head>
    <body light-mode->

        <lc-content>
            <section>
                <article>
                    <article-page>
                        <pre><code>{html}</code></pre>
                        <hr>
                    </article-page>
                    <article-page>
                    </article-page>
                </article>
            </section>
        </lc-content>
    </body>
    </html>
        """

    def html_article(self, content : str) -> str :
        return self.tag("article", content)

    def html_article_page(self, content : str) -> str :
        return self.tag("article-page", content)

    def get_relative_path(self, symbol : Symbol) -> str :
        if symbol.parent :
            return path.join(self.get_relative_path(symbol.parent), symbol.name)
        return symbol.name

    def write_namespace_page(self, ns : NamespaceSymbol, folder : str) -> None :
        #folder2 = path.join(folder, self.get_relative_path(ns))
        folder2 = folder
        self.m_currentFileFolder = folder2
        filePath = path.join(folder2, "index.html")
        os.makedirs(os.path.dirname(filePath), exist_ok=True)
        with open(filePath, 'wb') as f :
            html : str = ""

            # title
            html += f"<h1>Namespace {self.symbolCompleteHtmlName(ns)}</h1>"

            classes : str = ""
            for symbol in ns.children :
                if isinstance(symbol, ClassSymbol) :
                    classes += self.tag("tr",
                        self.tag("td", self.keyword2Html("class"), 'style="width:15%;text-align:right;"') + self.tag("td", self.symbolHtmlName(symbol), 'style="width:15%"') + self.tag("td", symbol.documentationString.brief)
                        )
                    #classes += f"<li>{} {symbol.documentationString.brief}</li>"
            if classes :
                html += f"<h2>Classes</h2><hr>"
                html += self.tag("table", classes, 'class="basic-table"')
                #html += f"<ul><code>{classes}</code></ul>"

            f.write(self.html_page_base(self.html_article(self.html_article_page(html))).encode('utf-8'))

    def write_class_page(self, cl : ClassSymbol, folder : str) -> None :
        self.m_currentFileFolder = folder
        filePath = path.join(folder, "index.html")
        os.makedirs(os.path.dirname(filePath), exist_ok=True)
        with open(filePath, 'wb') as f :
            html : str = ""

            # title
            html += f"<h1>Class {self.symbolHtmlName(cl)}</h1>"
            
            # brief description
            if cl.documentationString.docStr and cl.documentationString.docStr.rstrip(" \n\t*") != cl.documentationString.brief :
               html += f"""<p>{cl.documentationString.brief} {self.tag("a", "More...", 'href="#detailed-description"')}</p>"""
            else :
                # brief description only
                html += f"<p>{cl.documentationString.brief}</p>"

            # class full name
            html += f"""<div class=\"p\">Full symbol: {self.code_tag(self.keyword2Html('class') + " " + self.symbolCompleteHtmlName(cl))}</p>"""

            # methods
            rows : str = ""
            for method in cl.children :
                if isinstance(method, MethodSymbol) :
                    if method.access_specifier == AccessSpecifier.PUBLIC or True:
                        rows += self.method2tr(method)

            methods_table = self.methods_table(cl.children, [AccessSpecifier.PUBLIC])
            if methods_table :
                html += self.tag("h2", "Public methods")
                html += methods_table

            methods_table = self.methods_table(cl.children, [AccessSpecifier.PROTECTED])
            if methods_table :
                html += self.tag("h2", "Protected methods")
                html += methods_table

            methods_table = self.methods_table(cl.children, [AccessSpecifier.PRIVATE])
            if methods_table :
                html += self.tag("h2", "Private methods")
                html += methods_table

            # detailed description
            if cl.documentationString.docStr and cl.documentationString.docStr.rstrip(" \n\t*") != cl.documentationString.brief :
                html += "<br><br>" + self.tag("h2", "Detailed description", 'id="detailed-description"')
                 # brief description and long description
                doc = DocBlock()
                doc.parse(cl.documentationString.docStr)
                html += doc.brief + "<br>" + doc.long


            f.write(self.html_page_base(html).encode('utf-8'))
            #f.write(self.html_page_base(self.tag("lc-sidebar", "Lorem ipsum dolor sit amet consectetur adipisicing elit. Qui deleniti recusandae itaque cum ipsa obcaecati quod ex tempora quo quibusdam non ipsam suscipit, velit veniam id, corporis, in reprehenderit cumque.") + self.html_article(self.html_article_page(html))).encode('utf-8'))

    def methods_table(self, children : list[Symbol], aps : list[AccessSpecifier]) -> str :
        rows : str = ""
        for method in children :
            if isinstance(method, MethodSymbol) :
                found : bool = len(aps) <= 0
                for ap in aps :
                    if method.access_specifier == ap :
                        found = True

                if found :
                    rows += self.method2tr(method)

        return self.tag("table", rows, 'class="basic-table"') if rows else ""

    def method2tr(self, method : MethodSymbol) -> str :
        row : str = ""

        # return type
        ret = typing.cast(cxx.FuncArg, method.ret)
        assert ret.typ
        row += self.tag("td", self.code_tag(self.type2Html(ret.typ)), 'class="return-type"')

        # function
        func : str = ""
        # TODO method.args cast!
        func += self.code_tag(self.symbolHtmlName(method) + "(" + self.named_arg_list(typing.cast(list[cxx.FuncArg], method.args)) + ")" + (" " + self.keyword2Html("const") if method.const_qualified else ""))

        # description
        doc_html : str = ""
        if method.documentationString.docStr and method.documentationString.docStr.rstrip(" \n\t*") != method.documentationString.brief:
            doc = doc_utils.DocBlock()
            doc.parse(method.documentationString.docStr)
            doc_html += self.tag("details",
                self.tag("summary", doc.brief) +
                doc.long +
                (self.tag("h4", "Params") + self.named_args_doc(typing.cast(list[cxx.FuncArg], method.args), doc.params) if len(method.args) > 0 else "")
                )
            # TODO params
        else :
            doc_html += method.documentationString.brief

        row += self.tag("td", func + "<br>" + doc_html)

        return self.tag("tr", row, f'id="{self.generete_symbol_id(method)}"')

    def named_arg_list(self, args : list[cxx.FuncArg]) -> str : 
        result : str = ""
        for i in range(len(args)) :
            arg = args[i]

            # type
            assert arg.typ
            result += self.type2Html(arg.typ) + " "

            # name
            # TODO link for param
            result += self.tag("code-mvar", arg.name)

            if i < len(args) - 1 :
                result += ", "
        return result

    def named_args_doc(self, args : list[cxx.FuncArg], paramsdoc : list[ParamDocBlock]) -> str :
        if len(args) <= 0 :
            return ""

        rows : str = ""
        for arg in args :
            row : str = ""

            # type
            assert arg.typ
            row += self.tag("td", self.code_tag(self.type2Html(arg.typ)), 'class="type"')

            # find the paramdoc
            paramdoc : ParamDocBlock | None = None
            for pd in paramsdoc :
                if arg.name == pd.name :
                    paramdoc = pd
                    break

            doc_str : str = ""
            
            # name
            doc_str += self.code_tag(self.tag("code-mvar", arg.name))

            # doc
            if paramdoc :
                doc = DocBlock()
                doc.parse(paramdoc.descr)
                doc_str += self.tag("details", self.tag("summary", doc.brief) + doc.long)

            row += self.tag("td", doc_str)
            
            rows += self.tag("tr", row)

        return self.tag("table", rows, 'class="basic-table"')



    def write_symbolTree(self, symbolTree : SymbolsTree, dir : str) -> None :
        dir2 : str = dir
        if symbolTree.symbol :
            dir2 = path.join(dir, symbolTree.symbol.name)

        # write pages
        if isinstance(symbolTree.symbol, NamespaceSymbol) :
            self.write_namespace_page(symbolTree.symbol, dir2)
        if isinstance(symbolTree.symbol, ClassSymbol) :
            self.write_class_page(symbolTree.symbol, dir2)

        for child in symbolTree.children :
            self.write_symbolTree(child, dir2)

    def write_to(self, folder : str) -> None :
        self.m_currentOutFolder = folder
        folder2 = path.join(folder, "symbols")
        self.write_rc_file("style.css", folder)
        self.write_rc_file("code.css", folder)
        self.write_rc_file("index.js", folder)

        self.write_symbolTree(self.symbolTree, folder2)

        return
        for t in self.symbolTree.children :
            s = t.symbol
            if isinstance(s, NamespaceSymbol) :
                self.write_namespace_page(s, folder2)
        pass
