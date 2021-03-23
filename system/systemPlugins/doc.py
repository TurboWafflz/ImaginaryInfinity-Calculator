import rich
from systemPlugins.core import config, theme
import shutil
import os
import pydoc

def findDoc(article):
	if os.path.exists(config["paths"]["userPath"] + f"/docs/{article}.md"):
		return config["paths"]["userPath"] + f"/docs/{article}.md"
	elif os.path.exists(config["paths"]["systemPath"] + f"/docs/{article}.md"):
		return config["paths"]["systemPath"] + f"/docs/{article}.md"
	else:
		return None

def view(article):
	path=findDoc(article)
	if path == None:
		print(theme["styles"]["error"] + "Error: Article does not exist")
		return

	md = rich.markdown.Markdown(open(path, "r").read(), inline_code_lexer="python", inline_code_theme=config['appearance']['syntaxhighlight'], hyperlinks=False)
	console = rich.console.Console()

	if shutil.which('less') != None:
		with console.capture() as capture:
			console.print(md)
		str_output = capture.get()
		pydoc.pipepager(str_output, cmd='less -R --prompt \"Press [up] and [down] to scroll, press [q] to quit.\"')
	else:
		console.print(md)