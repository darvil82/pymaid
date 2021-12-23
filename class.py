from importlib import import_module
import inspect
import sys
from os import path


def get_classes(obj) -> list["Class"]:
	"""Returns a list of all classes in the given object"""
	return [Class(obj) for name, obj in inspect.getmembers(obj, predicate=inspect.isclass)]

def get_function_args(func):
	"""Returns a list of the arguments of a function"""
	return list(inspect.signature(func).parameters)

def get_uses(annotations: dict[str, object]) -> dict[str, object]:
	"""Returns a dictionary of all the object names of the given annotations"""
	return {
		use.__name__: use.__name__
		if "<" in str(use)
		else use
		for use in tuple(annotations.values())
	}

def gen_props_mermaid(obj: "Class") -> list[str]:
	"""Returns a list of the properties of the given object in mermaid format"""
	content = [f"class {obj.name} {{"]

	for prop, type in obj.annotations.items():
		content.append(f"\t{type.__name__}: {prop}")

	# add its methods and return types
	for name, method in inspect.getmembers(obj.object, predicate=inspect.isfunction):
		try:
			return_type = method.__annotations__["return"].__name__
		except (AttributeError, KeyError):
			return_type = None

		content.append(
			f"\t{name}({', '.join(get_function_args(method))}) {return_type}"
		)

	# if no properties or methods were added, just return an empty class
	return (content + ["}"] if len(content) >= 3 else [f"class {obj.name}"])

def gen_uses_mermaid(obj: "Class") -> list[str]:
	"""Returns a list of the used objects of the given object in mermaid format"""
	return [f"{name} <.. {obj.name}: {use}" for name, use in obj.uses.items()]

def gen_parents_mermaid(obj: "Class") -> list[str]:
	"""Returns a list of the parents of the given object in mermaid format"""
	return [f"{parent.__name__} <|-- {obj.name}: parent" for parent in obj.parents]



class Class:
	def __init__(self, obj: object) -> None:
		self.object = obj
		self.name: str = obj.__name__
		self.parents: list[object] = obj.__bases__
		self.annotations: dict[str, object] = obj.__annotations__
		self.uses = get_uses(self.annotations)

	def get_mermaid(self) -> list[str]:
		"""Returns a list of the mermaid representation of the given object"""
		return [
			*gen_props_mermaid(self),
			*gen_uses_mermaid(self),
			*gen_parents_mermaid(self)
		]






def gen_mermaid(objects: list[Class]) -> list[str]:
	"""Returns a list of the mermaid representation of the given objects"""
	content: list[str] = ["```mermaid", "classDiagram", "direction LR"]

	for obj in objects:
		# add class mermaid representation
		content += [""] + obj.get_mermaid()

	return content + ["```"]



def main():
	sys.path.append(path.dirname(sys.argv[1]))
	mod = import_module(path.basename(sys.argv[1].removesuffix(".py")))
	members = get_classes(mod)

	with open("test.md", "w") as f:
		f.write("\n".join(gen_mermaid(members)))


if __name__ == "__main__":
	main()