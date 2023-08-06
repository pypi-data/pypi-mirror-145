
from __future__ import annotations

from os import path
import os
import shutil

from . import string_utils

import abc

import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

# see https://medium.com/analytics-vidhya/monitoring-your-file-system-using-watchdog-64f7ad3279f

class MonitorFolder(FileSystemEventHandler):
    def __init__(self, generator : WebsiteGenerator, folder : str, outDir : str):
        self.folder = folder
        self.outDir = outDir
        self.generator = generator
        self.observer = Observer()
        self.observer.schedule(self, self.folder, recursive=True)
        self.observer.start()

    def on_any_event(self, event):
        if event.is_directory:
            return None
        else:
            #lcdoc.run(self.folder)
            self.generator.doc_dir(self.folder, self.outDir)

    def stop(self):
        self.observer.stop()
        self.observer.join()

class WebsiteGenerator :
    """
    WebsiteGenerator
    """

    m_currentOutFolder : str = ""
    m_currentFileFolder : str = ""

    resources_folder : str = ""

    def __init__(self) -> None:
        self.resources_folder = path.join(path.dirname(__file__), "../resources")
        pass

    def relative_href(self, href : str) -> str :
        if not self.m_currentFileFolder :
            return href
        return path.relpath(path.join(self.m_currentOutFolder, href), self.m_currentFileFolder)

    def write_rc_file(self, file : str, targetFolder : str) -> None :
        if not path.exists(targetFolder) :
            os.makedirs(targetFolder)
        shutil.copy(path.join(self.resources_folder, file), path.join(targetFolder, file))

    def html_header(self) -> str :
        return """
        <header>
            <div>
                <div class="button"><a href="">My Doc</a></div>
                <div class="links">
                    <div class="button"><a href="">References</a></div>
                    <div class="button"><a href="">Guides</a></div>
                    <div class="button"><a href="">pages</a></div>
                    <div class="button"><a href="">link</a></div>
                </div>
                <div class="button"><a href="">search</a></div>
            </div>
        </header>
        """

    def html_topnav(self) -> str :
        return """
        <lc-topnav>
            <div>
                <a href="">ciao</a>
                <a href="">ciao</a>
                <a href="">ciao</a>
            </div>
        </lc-topnav>
        """

    def html_page_base(self, title : str, content : str, additional_head_content : str = "", additional_body_content : str = "") -> str :
        return f"""
        <!DOCTYPE html>
        <html lang="en">
        <head class="light-mode">
            <meta charset="UTF-8">
            <meta http-equiv="X-UA-Compatible" content="IE=edge">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>{title}</title>

            {additional_head_content}
        </head>
        <body light-mode->
            {content}
            {additional_body_content}
        </body>
        </html>
        """

        return f"""
        <!DOCTYPE html>
        <html lang="en">
        <head class="light-mode">
            <meta charset="UTF-8">
            <meta http-equiv="X-UA-Compatible" content="IE=edge">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Document</title>

            <!--link rel="stylesheet" href="https://lucaciucci99.com/css/style.css"-->
            <!--link rel="stylesheet" href="./style.css"-->
            <link rel="stylesheet" href="{self.relative_href("style.css")}">

            <script async src="https://cdn.jsdelivr.net/npm/tex-math@latest/dist/tex-math.js"></script>

            <script src="//cdnjs.cloudflare.com/ajax/libs/highlight.js/11.5.0/highlight.min.js"></script>
            <script>
                //hljs.highlightAll();
                document.addEventListener("DOMContentLoaded", function() {{
                    document.querySelectorAll('code:not(.nohighlight)').forEach((block) => {{
                        hljs.highlightElement(block);
                    }});
                }})
            </script>
            
            <script src="https://cdn.jsdelivr.net/npm/style-scoped@latest/scoped.min.js"></script>
        </head>
        <body light-mode->

            {self.html_header()}
            {self.html_topnav()}

            <lc-content>
                <article>
                    {content}
                </article>
                <lc-nav-index></lc-nav-index>
            </lc-content>

            <script src="{self.relative_href("index.js")}"></script>
        </body>
        </html>
        """
        return f"""
        <!DOCTYPE html>
        <html lang="en">
        <head class="light-mode">
            <meta charset="UTF-8">
            <meta http-equiv="X-UA-Compatible" content="IE=edge">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Document</title>

            <link rel="stylesheet" href="https://lucaciucci99.com/css/style.css">
            <!--link rel="stylesheet" href="./style.css"-->
            <link rel="stylesheet" href="{self.relative_href("style.css")}">

            <script async src="https://cdn.jsdelivr.net/npm/tex-math@latest/dist/tex-math.js"></script>
        </head>
        <body light-mode->

            <lc-content>
                <section>
                    {content}
                </section>
            </lc-content>
        </body>
        </html>
        """

    def lcdoc_base_html(self, title : str, article : str) -> str :
        additional_head_content : str = f"""
        <!--link rel="stylesheet" href="https://lucaciucci99.com/css/style.css"-->
        <!--link rel="stylesheet" href="./style.css"-->
        <link rel="stylesheet" href="{self.relative_href("style.css")}">

        <script async src="https://cdn.jsdelivr.net/npm/tex-math@latest/dist/tex-math.js"></script>

        <script src="//cdnjs.cloudflare.com/ajax/libs/highlight.js/11.5.0/highlight.min.js"></script>
        <script>
            //hljs.highlightAll();
            document.addEventListener("DOMContentLoaded", function() {{
                document.querySelectorAll('code:not(.nohighlight)').forEach((block) => {{
                    hljs.highlightElement(block);
                }});
            }})
        </script>
        
        <script src="https://cdn.jsdelivr.net/npm/style-scoped@latest/scoped.min.js"></script>
        """
        body_content : str = f"""
        {self.html_header()}
        {self.html_topnav()}

        <lc-content>
            <article>
                {article}
            </article>
            <lc-nav-index></lc-nav-index>
        </lc-content>

        <script src="{self.relative_href("index.js")}"></script>
        """
        return self.html_page_base(title, body_content, additional_head_content=additional_head_content)

    def doc_dir(self, srcDir : str, outDir : str, root : bool = True) -> None :

        if root :
            self.m_currentOutFolder = outDir
            self.write_rc_file("style.css", outDir)
            self.write_rc_file("code.css", outDir)
            self.write_rc_file("index.js", outDir)

        for filename in os.listdir(srcDir) :
            in_path = path.join(srcDir, filename)
            out_path = path.join(outDir, filename)
            if path.isdir(in_path) :
                print(f"converting folder {in_path} -> {out_path}")
                self.doc_dir(in_path, out_path, False)
                continue

            if path.isfile(in_path) :
                print(f"converting file {in_path} -> {out_path}")
                content : str = ""
                with open(in_path, "r") as f :
                    content = f.read()
                    content = string_utils.recognizeCodeBlocks(content)
                p1 = content.find("---")
                p2 = content.find("---", p1 + 3)
                if p1 >= 0 and p2 >= 0 :
                    content = content[p2+3:]
                if not path.exists(path.dirname(out_path)) :
                    os.makedirs(path.dirname(out_path))
                with open(out_path, "wb") as f :
                    f.write(self.lcdoc_base_html("titolo", content).encode("utf-8"))


    def minitor_folder(self, srcDir : str, outDir : str) :
        monitor = MonitorFolder(self, srcDir, outDir)
        self.doc_dir(srcDir, outDir)
        print("running monitor")
        try:
            while True:
                time.sleep(10)
        except KeyboardInterrupt:
            monitor.stop()
            print("monitor stopped")