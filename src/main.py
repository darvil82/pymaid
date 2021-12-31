import argparse
from importlib import import_module
from io import TextIOWrapper
import sys
from os import path

from . import mclass


def log(msg: str, quit: bool = False):
	print(msg, file=sys.stderr)
	if quit:
		exit(1)


DIRECTIONS = ("LR", "RL", "TB", "BT")


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


def parse_args():
	pargs = argparse.ArgumentParser("pymaid")
	pargs.add_argument("input", help="The input file", type=str)
	pargs.add_argument(
		"-d",
		"--direction",
		help="The direction of the diagram",
		type=str,
		default="TB",
		choices=DIRECTIONS,
	)
	pargs.add_argument(
		"-o",
		"--output",
		help="The output file to append the content to",
		type=argparse.FileType("a"),
	)
	pargs.add_argument(
		"-m", "--no-md", help="Do not output markdown block", action="store_false"
	)
	subparsers = pargs.add_subparsers()

	class_args = subparsers.add_parser("class")
	class_args.add_argument(
		"-p", "--parents", action="store_false", help="Don't show the parent classes"
	)
	class_args.add_argument(
		"-u", "--uses", action="store_true", help="Show the used classes"
	)
	class_args.add_argument(
		"-t", "--text", action="store_true", help="Show text on the paths"
	)
	class_args.add_argument(
		"-P", "--props", action="store_false", help="Don't show the properties"
	)
	class_args.add_argument(
		"-i",
		"--init",
		action="store_true",
		help="Check the __init__ method for instance properties too",
	)
	class_args.add_argument(
		"-m", "--methods", action="store_false", help="Don't show the methods"
	)
	class_args.add_argument(
		"-e", "--no-extra", action="store_false", help="Don't show parents recursively"
	)
	class_args.set_defaults(func=mclass.gen_mermaid)

	pargs.set_defaults(func=lambda _: pargs.print_help())

	return pargs.parse_args()


def main():
	args = parse_args()
	args.func(args)


if __name__ == "__main__":
	main()
