import inspect
from typing import Callable



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
		show_props: bool = True,
		show_methods: bool = True
	) -> list[str]:
		"""Returns a list of the mermaid representation of the given object"""
		return [
			*(gen_class_mermaid(self, show_props, show_methods)),
			*(gen_uses_mermaid(self, show_path_text) if show_uses else []),
			*(gen_parents_mermaid(self, show_path_text) if show_parents else [])
		]


def get_classes(obj: object) -> list[Class]:
	"""Returns a list of all classes in the given object"""
	return [Class(obj) for _, obj in inspect.getmembers(obj, predicate=inspect.isclass)]


def get_function_args(func: Callable):
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
		k: (
			(v if isinstance(v, str) else v.__name__),
			get_name(v)
		) for k, v in annotations.items()
	}


def gen_props_mermaid(obj: Class) -> list[str]:
	"""Returns a list of the properties of the given object in mermaid format"""
	return [
	    f"\t{get_name(type)}: {prop}" for prop, type in obj.annotations.items()
	]


def gen_methods_mermaid(obj: Class) -> list[str]:
	content: list[str] = []
	for name, method in inspect.getmembers(obj.object, predicate=inspect.isfunction):
		try:
			return_type: str | None = get_name(method.__annotations__["return"])
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
	show_methods: bool = True
) -> list[str]:
	content = [
		f"class {obj.name} {{",
		*(gen_props_mermaid(obj) if show_props else []),
		*(gen_methods_mermaid(obj) if show_methods else []),
		"}"
	]
	return content if len(content) >= 3 else [f"class {obj.name}"]


def gen_uses_mermaid(obj: Class, display_use_path: bool = True) -> list[str]:
	"""Returns a list of the used objects of the given object in mermaid format"""
	new = []	# the new mermaid representation
	shown = []	# used to prevent duplicates

	for _, type in obj.uses.items():
		if type[0] in shown:
			continue
		count = tuple(x[0] for x in obj.uses.values()).count(type[0])
		new.append(f'{obj.name} "{count}" ..> {type[0]}{f": {type[1]}" * display_use_path}')
		shown.append(type[0])

	return new


def gen_parents_mermaid(obj: Class, display_parent_path: bool = True) -> list[str]:
	"""Returns a list of the parents of the given object in mermaid format"""
	return [
		f"{parent.__name__} <|-- {obj.name}{': parent' * display_parent_path}"
		for parent in obj.parents
	]


def gen_mermaid(
	objects: list[Class],
	show_parents: bool = True,
	show_uses: bool = False,
	show_path_text: bool = False,
	show_properties: bool = True,
	show_methods: bool = True
) -> list[str]:
	"""Returns a list of the mermaid representation of the given objects"""
	content: list[str] = []

	for obj in get_classes(objects):
		# add class mermaid representation
		content += [""] + obj.get_mermaid(
			show_path_text, show_parents, show_uses, show_properties, show_methods
		)

	return content