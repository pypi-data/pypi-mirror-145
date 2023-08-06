
from __future__ import annotations

import cxx
import lcdoc
from os import path

class CxxTargetOptions :

    fileOpt : cxx.FileOptions
    
    def __init__(self) -> None:
        self.fileOpt = cxx.FileOptions()

class CxxTargetFile :

    fileName : str = ""
    additionalOptions : CxxTargetOptions
    
    def __init__(self) -> None:
        self.additionalOptions = CxxTargetOptions()

class CxxTarget :

    options : CxxTargetOptions

    files : list[CxxTargetFile]

    def __init__(self) -> None:
        self.options = CxxTargetOptions()
        self.files = []

    def add_file(self, fileName : str) :
        file = CxxTargetFile()
        file.fileName = fileName
        self.files.append(file)
