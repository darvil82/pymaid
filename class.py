from importlib import import_module, util
import inspect
import sys
from os import path
from typing import Any


def get_classes(obj) -> list["Class"]:
	"""Returns a list of all classes in the given object"""
	return [Class(obj) for name, obj in inspect.getmembers(obj, predicate=inspect.isclass)]

def get_function_args(func):
	"""Returns a list of the arguments of a function"""
	return list(inspect.signature(func).parameters)

#! SHIT SHIT SHIT SHIT
def get_name(obj: Any, basic_name: bool = True) -> str:
	"""Returns the name of the given object"""
	return obj.__name__ if "<" in str(obj) and ">" in str(obj) else str(obj)

def get_used_objects(annotations: dict[str, Any]) -> dict[str, tuple[str, str]]:
	"""
	Returns a dictionary of the used objects of the given object.
	`{name: (type_name, type)}`
	"""
	return {k: (get_name(v, False), get_name(v)) for k, v in annotations.items()}

def gen_props_mermaid(obj: "Class") -> list[str]:
	"""Returns a list of the properties of the given object in mermaid format"""
	content = [f"class {obj.name} {{"]

	for prop, type in obj.annotations.items():
		content.append(f"\t{get_name(type)}: {prop}")

	# add its methods and return types
	for name, method in inspect.getmembers(obj.object, predicate=inspect.isfunction):
		try:
			return_type = get_name(method.__annotations__["return"])
		except (AttributeError, KeyError):
			return_type = None

		# the method representation
		content.append(
			f"\t{name}({', '.join(get_function_args(method))}) {return_type}"
		)

	# if no properties or methods were added, just return an empty class definition
	return (content + ["}"] if len(content) >= 3 else [f"class {obj.name}"])

def gen_uses_mermaid(obj: "Class", display_use_path: bool = True) -> list[str]:
	"""Returns a list of the used objects of the given object in mermaid format"""
	new = []	# the new mermaid representation
	shown = []	# used to prevent duplicates

	for name, type in obj.uses.items():
		if type[0] in shown:
			continue
		count = tuple(x[0] for x in obj.uses.values()).count(type[0])
		new.append(f'{obj.name} "{count}" ..> {type[0]}: {type[1] if display_use_path else ""}')
		shown.append(type[0])

	return new

def gen_parents_mermaid(obj: "Class", display_parent_path: bool = True) -> list[str]:
	"""Returns a list of the parents of the given object in mermaid format"""
	return [
		f"{parent.__name__} <|-- {obj.name}: {'parent' if display_parent_path else ''}"
		for parent in obj.parents
	]



class Class:
	def __init__(self, obj: object) -> None:
		self.object = obj
		self.name: str = obj.__name__
		self.parents: list[object] = obj.__bases__
		self.annotations: dict[str, object] = obj.__annotations__
		self.uses = get_used_objects(self.annotations)

	def get_mermaid(
		self,
		show_path_text: bool = False,
		show_parents: bool = True,
		show_uses: bool = False,
	) -> list[str]:
		"""Returns a list of the mermaid representation of the given object"""
		return [
			*gen_props_mermaid(self),
			*(gen_uses_mermaid(self, show_path_text) if show_uses else []),
			*(gen_parents_mermaid(self, show_path_text) if show_parents else [])
		]






def gen_mermaid(
	objects: list[Class],
	show_path_text: bool = False,
	show_parents: bool = True,
	show_uses: bool = False,
) -> list[str]:
	"""Returns a list of the mermaid representation of the given objects"""
	content: list[str] = ["```mermaid", "classDiagram", "direction LR"]

	for obj in objects:
		# add class mermaid representation
		content += [""] + obj.get_mermaid(show_path_text, show_parents, show_uses)

	return content + ["```"]



def main():
	sys.path.append(path.dirname(sys.argv[1]))
	mod = import_module(path.basename(sys.argv[1].removesuffix(".py")))
	members = get_classes(mod)

	with open("test.md", "w") as f:
		f.write("\n".join(gen_mermaid(members, True, True, True)))


if __name__ == "__main__":
	main()