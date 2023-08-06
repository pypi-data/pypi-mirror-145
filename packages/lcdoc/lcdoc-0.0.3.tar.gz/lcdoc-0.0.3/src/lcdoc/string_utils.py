

from dataclasses import replace
from unittest import result


def trimCommentLines(src : str) -> str :
    content : str = src.replace("/*!", "").replace("/**", "").replace("/*", "").replace("*/", "").replace("///", "").replace("//", "")

    # https://stackoverflow.com/questions/3054604/iterate-over-the-lines-of-a-string
    result : str = ""
    for line in content.splitlines() :
        strippedLine = line.strip(" ")
        if strippedLine.startswith("* ") :
            strippedLine = strippedLine[2:]
        else :
            if strippedLine.startswith("*") :
                strippedLine = strippedLine[1:]
        result += strippedLine + "\n"

    return result

def subsSpecialChars(src : str) -> str :
    result : str = src[:]
    #result = src.replace("<", "&lt;")
    #result = result.replace(">", "&gt;")
    return result

def recognizeNewLines(src : str) -> str :
    #return src.replace("  ", "<br>")
    #return src.replace("&lt;br&gt;", "<br>") # Terribile non funziona sempre
    return src.replace("\n\n", "<br>")
    return src[:]

def recognizeCodeBlocks(src : str) -> str :
    result : str = src[:]

    # ignore highlighing for code blocks withoud type
    result = result.replace("<code>", """<code class="nohighlight">""")

    while True:
        pos_1 : int = result.find("```")
        pos_2 : int = result[:].find("```", pos_1+3)
        if pos_1 >= 0 and pos_2 >= 0 :
            code = result[pos_1+3:pos_2].replace("<", "&lt;").replace(">", "&gt;")
            
            language : str = ""
            def check_language(extensions : list[str], hljs_extension : str) :
                nonlocal language, code
                for ext in extensions :
                    if code.lower().startswith(ext.lower()) :
                        language = hljs_extension
                        code = code[len(ext):]
                        break
            if not language : check_language(["cpp", "c++"], "cpp")
            if not language : check_language(["c"], "c")
            if not language : check_language(["python", "py"], "py")
            if not language : check_language(["json"], "json")
            if not language : check_language(["js", "javascript"], "js")
            if not language : check_language(["html"], "html")
            if not language : check_language(["tex", "latex"], "tex")

            code = code.strip(" \n\t")


            #result = result[:pos_1] + code + result[pos_2:]
            code_block : str = ""
            if language :
                code_block = f"""<pre><code class="language-{language}">{code}</code></pre>"""
                #result = result.replace("```", f"""<pre><code class="language-{language}">""", 1).replace("```", "</code></pre>", 1)
            else :
                code_block = f"""<pre><code class="nohighlight">{code}</code></pre>"""
                #result = result.replace("```", "<pre><code>", 1).replace("```", "</code></pre>", 1)
            result = result[:pos_1] + code_block + result[pos_2+3:]
        else :
            break

    result = result.replace("\\`", "&#96;") # wow! copilod completed with "&#96;" !!!

    return result