import inspect
from typing import Callable

from . import utils

class Class:
	def __init__(self, obj: object) -> None:
		self.object = obj
		self.name: str = obj.__name__
		self.parents: list[object] = obj.__bases__
		self.annotations: dict[str, object] = inspect.get_annotations(obj)
		self.uses = get_used_objects(self.annotations)

	def __repr__(self) -> str:
		return self.name

	def get_mermaid(
		self,
		show_path_text: bool = False,
		show_parents: bool = True,
		show_uses: bool = False,
		show_props: bool = True,
		show_methods: bool = True,
		read_init: bool = True,
	) -> list[str]:
		"""Returns a list of the mermaid representation of the given object"""
		return [
			*(gen_class_mermaid(self, show_props, read_init, show_methods)),
			*(gen_uses_mermaid(self, show_path_text) if show_uses else []),
			*(gen_parents_mermaid(self, show_path_text) if show_parents else []),
		]


def get_classes(obj: object) -> list[Class]:
	"""Returns a list of all classes in the given object"""
	return [Class(obj) for _, obj in inspect.getmembers(obj, predicate=inspect.isclass)]


def get_function_args(func: Callable) -> list[str]:
	"""Returns a list of the arguments of a function"""
	return [*inspect.signature(func).parameters]


def get_name(obj: object) -> str:
	"""Returns the name of the given object"""
	return obj.__name__ if all(i in str(obj) for i in "><") else str(obj)


def get_used_objects(annotations: dict[str, object]) -> dict[str, tuple[str, str]]:
	"""
	Returns a dictionary of the used objects of the given object.
	`{name: (type_name, type)}`
	"""
	return {
		k: ((v if isinstance(v, str) else v.__name__), get_name(v))
		for k, v in annotations.items()
	}


def gen_props_mermaid(obj: Class, read_init: bool = True) -> list[str]:
	"""Returns a list of the properties of the given object in mermaid format"""
	# get all properties of the object
	props_to_show: list[str] = [
		f"\t{get_name(type)}: {prop}" for prop, type in obj.annotations.items()
	]

	# check if obj has innit method, make sure we are not dealing with object
	if "__init__" in obj.object.__dict__ and obj.object is not object and read_init:
		method = obj.object.__init__
		# get first argument of the init method
		args = inspect.getfullargspec(method).annotations
		# get the lines of the init method
		for prop, type in args.items():
			if prop == "return":
				continue
			props_to_show.append(f"\tself 🡪 {get_name(type)}: {prop}")

	# make sure there are no brackets in the type name,
	# otherwise mermaid will display these as methods
	return [x.replace("(", "[").replace(")", "]") for x in props_to_show]


def gen_methods_mermaid(obj: Class) -> list[str]:
	content: list[str] = []
	for name, method in inspect.getmembers(obj.object, predicate=inspect.isfunction):
		try:
			return_type: str | None = method.__annotations__["return"].__name__
		except (AttributeError, KeyError):
			return_type = None

		# the method representation
		content.append(
			f"\t{name}({', '.join(get_function_args(method))}) {return_type}"
		)
	return content


def gen_class_mermaid(
	obj: Class,
	show_props: bool = True,
	read_init: bool = True,
	show_methods: bool = True,
) -> list[str]:
	content = [
		f"class {obj.name} {{",
		*(gen_props_mermaid(obj, read_init) if show_props else []),
		*(gen_methods_mermaid(obj) if show_methods else []),
		"}",
	]
	return content if len(content) >= 3 else [f"class {obj.name}"]


def gen_uses_mermaid(obj: Class, display_use_path: bool = True) -> list[str]:
	"""Returns a list of the used objects of the given object in mermaid format"""
	new = []  # the new mermaid representation
	shown = []  # used to prevent duplicates

	for _, type in obj.uses.items():
		if type[0] in shown:
			continue
		count = tuple(x[0] for x in obj.uses.values()).count(type[0])
		new.append(
			f'{obj.name} "{count}" ..> {type[0]}{f": {type[1]}" * display_use_path}'
		)
		shown.append(type[0])

	return new


def gen_parents_mermaid(obj: Class, display_parent_path: bool = True) -> list[str]:
	"""Returns a list of the parents of the given object in mermaid format"""
	return [
		f"{parent.__name__} <|-- {obj.name}{': parent' * display_parent_path}"
		for parent in obj.parents
	]


def get_parents_recursive(obj: Class) -> list[Class]:
	objs = [obj]
	for parent in obj.parents:
		objs.extend(get_parents_recursive(Class(parent)))
	return objs


def gen_mermaid(args) -> None:
	"""Returns a list of the mermaid representation of the given objects"""
	file = utils.get_import_file(args.input)
	classes = get_classes(file)

	if args.no_extra:
		classes_to_parse: list[Class] = []
		for cls in classes:
			parents = get_parents_recursive(cls)
			# check for duplicates
			for x in parents:
				if x.name not in [y.name for y in classes_to_parse]:
					classes_to_parse.append(x)
	else:
		classes_to_parse = classes

	content = []
	for obj in classes_to_parse:
		content += obj.get_mermaid(
			args.text, args.parents, args.uses, args.props, args.methods, args.init
		)

	utils.generate_mermaid(
		content, "classDiagram", args.direction, args.output, args.no_md
	)
