from importlib import import_module
import inspect
import sys
from os import path



def get_uses(annotations: dict[str, object]) -> dict[str, object]:
	return {
		use.__name__: use.__name__
		if "<" in str(use)
		else use
		for use in tuple(annotations.values())
	}

class Class:
	def __init__(self, obj: object) -> None:
		self.object = obj
		self.name: str = obj.__name__
		self.bases: list[object] = obj.__bases__
		self.annotations: dict[str, object] = obj.__annotations__
		self.uses = get_uses(self.annotations)


	def get_mermaid(self) -> list[str]:
		content = [f"class {self.name} {{"]

		for prop, type in self.annotations.items():
			content.append(f"\t{type.__name__}: {prop}")

		# add its methods and return types
		for name, method in inspect.getmembers(self.object, predicate=inspect.isfunction):
			try:
				return_type = method.__annotations__["return"].__name__
			except (AttributeError, KeyError):
				return_type = None

			content.append(
				f"\t{name}({', '.join(get_function_args(method))}) {return_type}"
			)

		# if no properties or methods were added, just return an empty class
		return (content + ["}"] if len(content) >= 3 else [f"class {self.name}"])



def get_classes(module) -> list[Class]:
	return [Class(obj) for name, obj in inspect.getmembers(module, predicate=inspect.isclass)]

def get_function_args(func):
	return list(inspect.signature(func).parameters)








def gen_mermaid(objects: list[Class]) -> list[str]:
	content: list[str] = ["```mermaid", "classDiagram", "direction TB"]

	for obj in objects:
		# add class mermaid representation
		content += [""] + obj.get_mermaid()

		# add object parents
		for parent in obj.bases:
			content.append(f"{parent.__name__} <|-- {obj.name}: parent")

		# add objects that this object uses
		for name, use in obj.uses.items():
			content.append(f"{name} <.. {obj.name}: {use}")

	return content + ["```"]




def main():
	sys.path.append(path.dirname(sys.argv[1]))
	mod = import_module(path.basename(sys.argv[1].removesuffix(".py")))
	members = get_classes(mod)

	with open("test.md", "w") as f:
		f.write("\n".join(gen_mermaid(members)))


if __name__ == "__main__":
	main()