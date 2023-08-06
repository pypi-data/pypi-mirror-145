from pathlib import Path
from typing import Optional, List

from pydantic import ValidationError
from phidata.workspace import WorkspaceConfig

from phi.utils.cli_console import print_error, print_info, print_validation_errors
from phi.utils.log import logger


def load_workspace(config_file_path: Path) -> List[WorkspaceConfig]:
    """
    Loads a workspace using a config_file_path and returns List[WorkspaceConfig]

    NOTE: When loading a workspace, relative imports or package imports dont work.
    This is a known problem in python :(
        eg: https://stackoverflow.com/questions/6323860/sibling-package-imports/50193944#50193944
    To make them work, we need to install the workspace as a python module
    But when we run `phi ws setup`, the ws module is not yet installed
    So we add workspace_root to sys.path so is treated as a package
    """

    import importlib.util
    from importlib.machinery import ModuleSpec

    logger.debug(f"--^^-- Loading workspace from: {config_file_path}")

    # Add workspace_root to sys.path so is treated as a package
    try:
        import sys

        workspace_config_dir_path = config_file_path.parent.resolve()
        workspace_root_dir_path = workspace_config_dir_path.parent
        workspace_parent_dir_path = workspace_root_dir_path.parent.resolve()
        logger.debug(f"Adding {workspace_parent_dir_path} to path")
        sys.path.insert(0, str(workspace_parent_dir_path))
    except Exception as e:
        print_error(
            "Could not add workspace parent directory to Path, this will break references to the workspace config"
        )
        logger.exception(e)

    # Read the WorkspaceConfig objects from config_file_path
    try:
        # https://docs.python.org/3/library/importlib.html#importing-a-source-file-directly
        # Create a ModuleSpec
        ws_config_module_spec: Optional[
            ModuleSpec
        ] = importlib.util.spec_from_file_location("ws_config_module", config_file_path)
        # Using the ModuleSpec create a module
        if ws_config_module_spec:
            ws_config_module = importlib.util.module_from_spec(ws_config_module_spec)
            ws_config_module_spec.loader.exec_module(ws_config_module)  # type: ignore

            # loop over all objects in module and find WorkspaceConfig objects
            ws_configs: List[WorkspaceConfig] = []
            for k, v in ws_config_module.__dict__.items():
                # logger.debug(f"Found {k}: | Type: {v.__class__.__name__}")
                if isinstance(v, WorkspaceConfig):
                    ws_configs.append(v)
            logger.debug("--^^-- Loading complete")
            return ws_configs
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
