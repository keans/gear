from pathlib import Path

import jinja2

from gear.utils.typing import PathOrString
from gear.utils.utils import ensure_path


def render(
    search_path: PathOrString,
    template_filename: PathOrString,
    theme_path: PathOrString = None,
    **kwargs
) -> str:
    assert isinstance(search_path, (str, Path))
    assert isinstance(template_filename, (str, Path))
    assert (theme_path is None) or isinstance(theme_path, (str, Path))

    # ensure that search path is a Path and it does exist
    search_path = ensure_path(search_path, must_exist_dir=True)

    # ensure that template file is a Path
    template_filename = ensure_path(template_filename)

    search_path = [search_path]
    if theme_path is not None:
        # if theme path is set, add it to the search path
        search_path.append(theme_path)

    # prepare environment for rendering
    templateEnv = jinja2.Environment(
        loader=jinja2.FileSystemLoader(searchpath=search_path)
    )
    template = templateEnv.get_template(template_filename.as_posix())

    return template.render(**kwargs)
