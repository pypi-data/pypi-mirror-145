
"""LC_NOTICE_BEGIN
LC_NOTICE_END"""

#import clang.cindex

class Symbol :
    declaration : Declaration | None = None
    definition : Declaration | None = None

    name : str = ""

    parent : Symbol | None = None
    children : list[Symbol] = []

    def addToParent(self, parent : Symbol) -> None :
        parent.children.append(self)
        self.parent = parent

    def getCompleteName(self) -> str :
        if (self.parent) :
            return self.parent.getCompleteName() + "!!" + self.name
        return self.name



class Declaration :
    ciao : str = "aa"
    node : clang.cindex.Cursor

    symbol : Symbol | None = None

    def __init__(self, node : clang.cindex.Cursor) -> None :
        self.node = node

    def spelling(self) -> str :
        return self.node.spelling

    def __str__(self) -> str:
        return str(self.node.kind) + " " + self.node.spelling

    def __repr__(self) -> str:
        # see https://docs.python.org/3/reference/datamodel.html#object.__repr__
        return self.node.displayname
        return self.node.spelling