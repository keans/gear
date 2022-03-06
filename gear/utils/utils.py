import sys
import importlib
from pathlib import Path
from typing import Union, Any

from gear.utils.config import CONFIG_DIRECTORY


def ensure_path(
    path: Union[str, Path],
    must_exist: bool = False,
    must_exist_dir: bool = False,
    create_dir: bool = False
) -> Path:
    """
    ensure that given path is of type Path

    :param path: path that is checked
    :type path: Union[str, Path]
    :param must_exist: if True, path must exist otherwise exception is raised
    :type must_exist: bool, optional
    :param must_exist_dir: if True, path must be an existing directory
    :type must_exist_dir: bool, optional
    :param create_dir: if True, create the directory if not existing yet
    :type create_dir: bool, optional
    :return: path
    :rtype: Path
    """
    # ensure path is of type Path
    path = (
        path
        if isinstance(path, Path) else
        Path(path)
    )

    if must_exist and not path.exist():
        # file does not exist
        raise FileNotFoundError(
            f"The file '{path}' does not exist!"
        )

    if must_exist_dir and not path.is_dir():
        # path is not a directory
        raise FileNotFoundError(
            f"The path '{path}' is not a valid directory!"
        )

    if create_dir:
        # create directory, if not existing including parents
        path.mkdir(exist_ok=True, parents=True)

    return path


def get_classes(directory: Union[str, Path], cls: Any) -> list:
    """
    get all subclasses of the class type in the given directory

    :param directory: directory in which subclasses are searched
    :type directory: Union[str, Path]
    :param cls: class that is searched
    :type cls: Any
    :returns: list of subclasses found
    :type: list
    """
    assert isinstance(directory, (str, Path))

    # ensure that directory is a Path and it does exist
    directory = ensure_path(directory, must_exist_dir=True)

    # go through all python files from directory
    for fn in directory.glob("**/*.py"):
        # load specs from file
        spec = importlib.util.spec_from_file_location(
            name=f"{fn.parent.as_posix().replace('/', '.')}.{fn.stem}",
            location=fn
        )

        # get module from specs
        module = importlib.util.module_from_spec(spec)
        sys.modules[spec.name] = module

        # load the module
        spec.loader.exec_module(module)

    return cls.__subclasses__()


def guess_filename(
    name: Union[str, Path],
    directories: Union[Path, list],
    default_extension: str
) -> Path:
    """
    try to guess filename: first use given name as filename,
    if not exist try to find it in one of the given directories

    :param name: name of the file
    :type name: Union[str, Path]
    :param directories: directories that will be searched
    :type directories: Union[str, list]
    :param default_extension: default extension starting with '.'
    :type default_extension: str
    :return: Path of the filename found or None, if not existing
    :rtype: Path
    """
    assert isinstance(name, (str, Path))
    assert isinstance(directories, (str, Path, list))
    assert (
        isinstance(default_extension, str) and
        default_extension.startswith(".")
    )

    if isinstance(directories, (str, Path)):
        # convert string to list
        directories = [directories]

    # ensure that list contains only Path
    directories = [ensure_path(d) for d in directories]

    if Path(".") not in directories:
        # add local directory, if not provided
        directories.insert(0, Path("."))

    for directory in directories:
        # try to get file from directory
        for filename in (name, f"{name}{default_extension}"):
            if directory.joinpath(filename).exists():
                # return existing, filename
                return directory.joinpath(filename)

    # file does not exist
    raise FileNotFoundError(
         f"The file '{name}' could not be found!"
    )
