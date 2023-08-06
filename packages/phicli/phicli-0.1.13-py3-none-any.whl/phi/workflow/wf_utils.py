from collections import OrderedDict
from pathlib import Path
from typing import Optional, Dict, Tuple

from phidata.product import DataProduct
from phidata.workflow import Workflow
from phi.utils.cli_console import print_error, print_info, print_validation_errors
from phi.utils.log import logger


def get_workflow_file_and_name(
    wf_description: str, ws_dir_path: Path, products_dir: str
) -> Tuple[Optional[str], Optional[str]]:
    """
    Given a workflow description string, returns the workflow_file and workflow_name.
    The workflow_file is the path of the file starting after the products_dir.
    The workflow_file string can then be joined to the `products_dir` in the current env
    to get the absolute workflow file path
    Examples:

    `dau` -> (dau/dau.py, None)
    `dau:save` -> (dau/dau.py, save)
    `dau/dau2:save` -> (dau/dau2.py, save)

    Args:
        wf_description:
        ws_dir_path:
        products_dir:

    Returns:
        workflow_file: string path to the file containing the workflow,
                        relative to the products dir
        workflow_name: name of the workflow (if provided)
    """

    # Path to the file containing the workflow
    workflow_file: Optional[str] = None
    workflow_name: Optional[str] = None

    # Parse the workflow file and name
    _wf_path_slices = wf_description.strip().split(":")
    _wf_path: str = _wf_path_slices[0]
    _wf_py_file: str = _wf_path + ".py"
    workflow_name = _wf_path_slices[1] if len(_wf_path_slices) > 1 else None

    # Check if products dir is valid
    products_dir_path: Path = ws_dir_path.joinpath(products_dir)
    if not (products_dir_path.exists() and products_dir_path.is_dir()):
        logger.error("Invalid products dir: {}".format(products_dir))
        return None, None

    # Check if the workflow is a file or a directory
    _wf_file_check: Path = products_dir_path.joinpath(_wf_py_file)
    _wf_dir_check: Path = products_dir_path.joinpath(_wf_path)

    if _wf_file_check.exists() and _wf_file_check.is_file():
        workflow_file = _wf_py_file
    elif _wf_dir_check.exists() and _wf_dir_check.is_dir():
        _wf_file_in_dir_check = _wf_dir_check.joinpath(_wf_py_file)
        if _wf_file_in_dir_check.exists() and _wf_file_in_dir_check.is_file():
            workflow_file = "{}/{}".format(_wf_path, _wf_py_file)

    if workflow_file is None:
        # logger.error("Workflow file not found")
        return None, None

    return workflow_file, workflow_name


def get_data_products_and_workflows_from_file(
    file_path: Path,
) -> Tuple[Dict[str, DataProduct], Dict[str, Workflow]]:
    """
    Reads the DataProducts & Workflows from filepath
    Args:
        file_path:

    Returns:

    """

    import importlib.util
    from importlib.machinery import ModuleSpec
    from pydantic import ValidationError

    logger.debug(f"Reading {file_path}")

    # Read DataProduct and Workflow objects from file_path
    try:
        # https://docs.python.org/3/library/importlib.html#importing-a-source-file-directly
        # Create a ModuleSpec
        dp_module_spec: Optional[ModuleSpec] = importlib.util.spec_from_file_location(
            "dp_module", file_path
        )
        # Using the ModuleSpec create a module
        if dp_module_spec:
            dp_module = importlib.util.module_from_spec(dp_module_spec)
            dp_module_spec.loader.exec_module(dp_module)  # type: ignore

            # loop over all objects in module and find DataProduct and Workflow objects
            dp_dict: Dict[str, DataProduct] = OrderedDict()
            wf_dict: Dict[str, Workflow] = OrderedDict()
            for k, v in dp_module.__dict__.items():
                if isinstance(v, DataProduct):
                    logger.debug(f"Found {k} | Type: {v.__class__.__name__}")
                    dp_dict[k] = v
                if isinstance(v, Workflow):
                    logger.debug(f"Found {k} | Type: {v.__class__.__name__}")
                    wf_dict[k] = v
            logger.debug("--^^-- Loading complete")
            return dp_dict, wf_dict
    except NameError as name_err:
        print_error("Variable not defined")
        raise
    except ValidationError as validation_err:
        print_error(str(validation_err))
        # print_validation_errors(validation_err.errors())
        print_info("Please fix and try again")
        exit(0)
    except (ModuleNotFoundError, Exception) as e:
        # logger.exception(e)
        raise
