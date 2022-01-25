from importlib import import_module
from io import TextIOWrapper
import sys
from os import path

def get_import_file(file):
	sys.path.append(path.dirname(file))
	return import_module(path.basename(file.removesuffix(".py")))

def generate_mermaid(
	mermaid: list[str],
	type: str,
	direction: str,
	file: TextIOWrapper = None,
	show_md_block: bool = True,
):
	content = "\n".join(
		[
			"```mermaid" * show_md_block,
			type,
			f"direction {direction.upper()}",
			*mermaid,
			"```" * show_md_block,
		]
	)

	if file:
		file.write(content)
	else:
		print(content)