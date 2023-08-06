import inspect
import sys
from argparse import Namespace
from typing import Callable, Optional, List, Mapping, Set, Any, Union


PrimitiveType = Union[int, float, bool, str]


def get_positional_arguments(argv: Optional[List[str]] = None) -> List[str]:
    argv = argv if argv else sys.argv[1:]

    arguments = []

    for argument in argv:
        if argument.startswith('-'):
            break

        arguments.append(argument)

    return arguments


def get_keyword_arguments(argv: Optional[List[str]] = None) -> Set[str]:
    argv = argv if argv else sys.argv[1:]

    num_positional_arguments = len(get_positional_arguments(argv))

    passed_arguments = {
        key.lstrip('-').replace('_', '-')
        for key in argv[num_positional_arguments::2]
        if key.startswith('-')
    }

    return passed_arguments


def get_script_parameters(function: Callable, ignore_keyword_arguments: bool = True) -> Mapping[str, PrimitiveType]:
    """
    Returns the arguments of a function with its values specified by the command line or its default values.
    Underscores in the name of the arguments are transformed to dashes.
    Can optionally filter out keyword arguments obtained through the command line.

    :param function: The function to inspect.
    :param ignore_keyword_arguments: Whether to filter out keyword command line arguments.
    :return: A map from argument names to default values.
    """
    positional_arguments, keyword_arguments = get_positional_arguments(), get_keyword_arguments()
    signature = inspect.signature(function)

    arguments = {}

    for index, (name, parameter) in enumerate(signature.parameters.items()):
        transformed_name = name.replace('_', '-')

        if index < len(positional_arguments):
            arguments[transformed_name] = positional_arguments[index]

        elif not (ignore_keyword_arguments and transformed_name in keyword_arguments):
            if parameter.default != parameter.empty:
                arguments[transformed_name] = parameter.default

    return arguments


def flatten_dictionary(parameters: Mapping[Any, Any], delimiter: str = '/') -> Mapping[str, PrimitiveType]:
    def _dictionary_generator(input_dictionary, prefixes=None):
        prefixes = prefixes[:] if prefixes else []

        if isinstance(input_dictionary, Mapping):
            for key, value in input_dictionary.items():
                key = str(key)

                if isinstance(value, (Mapping, Namespace)):
                    value = vars(value) if isinstance(value, Namespace) else value
                    yield from _dictionary_generator(value, prefixes + [key])

                else:
                    yield prefixes + [key, value if value is not None else str(None)]

        else:
            yield prefixes + [input_dictionary if input_dictionary is None else str(input_dictionary)]

    return {delimiter.join(keys): val for *keys, val in _dictionary_generator(parameters)}
