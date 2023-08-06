

from mimetypes import common_types
import string_utils

class ParamDocBlock :
    name : str = ""
    descr : str = ""

    def handle(self, src : str) :
        comment = src.strip()
        pos : int = comment.find(" ")
        if (pos >= 0) :
            self.name = comment[:pos]
            self.descr = comment[pos:].strip()
        else :
            self.name = src

class DocBlock :

    brief : str = ""
    long : str = ""

    params : list[ParamDocBlock]

    def __init__(self) -> None:
        self.params = []
        pass

    def findParam(self, name : str) -> ParamDocBlock | None :
        for param in self.params :
            if (param.name == name) :
                return param
        return None
    
    def parse(self, src : str) -> None :
        #comment = string_utils.trimCommentLines(src)
        comment = src[:]

        # Find the brief block
        briefEnd = comment.find("\n\n")
        if briefEnd > 0 :
            self.brief = comment[:briefEnd]
            comment = comment[briefEnd+2:]
        else :
            self.brief = comment
            comment = ""
        self.brief = self.brief.replace("@brief ", "", 1)
        self.brief = self.brief.replace("\\brief ", "", 1)

        #print("brief: ", self.brief)
        #print("long: ", comment)

        while comment :
            lineEnd : int = comment.find("\n")
            line : str = comment[:]
            if lineEnd >= 0 :
                line = comment[:lineEnd]
            if line.startswith("@") :
                self.handleDifferentBlock(comment)
                break

            if lineEnd >= 0 :
                comment = comment[lineEnd+1:]
            else :
                comment = ""
            self.long += line + "\n"
        
        self.long = string_utils.recognizeCodeBlocks(self.long).replace("<p>", "<div class=\"paragraph\">").replace("</p>", "</div>")

    def handleDifferentBlock(self, src : str) -> None :
        if not src :
            return
        if src[1:].startswith("param ") :
            param = ParamDocBlock()
            self.params.append(param)
            param.handle(self.handleBlock(src[1:].replace("param ", "", 1)))
            pass

    def handleBlock(self, src : str) -> str :
        comment = src[:]
        result = ""
        while comment :
            lineEnd : int = comment.find("\n")
            line : str = comment[:]
            if lineEnd >= 0 :
                line = comment[:lineEnd]
            if line.startswith("@") :
                self.handleDifferentBlock(comment)
                break
            if lineEnd >= 0 :
                comment = comment[lineEnd+1:]
            else :
                comment = ""
            result += line + "\n"
        return result
