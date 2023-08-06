from os import environ
from pathlib import Path
from typing import Optional, Dict, List

from phidata import constants
from phidata.product import DataProduct
from phidata.workflow import Workflow
from phidata.workspace import WorkspaceConfig
from phidata.types.context import PathContext, RunContext

from phi.types.run_status import RunStatus
from phi.utils.cli_console import (
    print_error,
    print_info,
    print_heading,
    print_dict,
    print_info,
    print_subheading,
)
from phi.utils.log import logger
from phi.workspace.phi_ws_data import PhiWsData


def set_local_env(
    ws_config: WorkspaceConfig,
    path_context: PathContext,
) -> None:
    """VERY IMPORTANT TO RUN BEFORE RUNNING ANY LOCAL WORKFLOWS
    This function updates the local environment with Paths and Configuration
    Main uses:
        1. Path env variables used by DataAssets for building file_paths
        2. Cloud config variables used by AwsAssets like aws_region and profile
    """
    # 1. Path env variables used by DataAssets for building file_paths
    if path_context.scripts_dir is not None:
        environ[constants.SCRIPTS_DIR_ENV_VAR] = str(path_context.scripts_dir)
    if path_context.storage_dir is not None:
        environ[constants.STORAGE_DIR_ENV_VAR] = str(path_context.storage_dir)
    if path_context.meta_dir is not None:
        environ[constants.META_DIR_ENV_VAR] = str(path_context.meta_dir)
    if path_context.products_dir is not None:
        environ[constants.PRODUCTS_DIR_ENV_VAR] = str(path_context.products_dir)
    if path_context.notebooks_dir is not None:
        environ[constants.NOTEBOOKS_DIR_ENV_VAR] = str(path_context.notebooks_dir)
    if path_context.workspace_config_dir is not None:
        environ[constants.WORKSPACE_CONFIG_DIR_ENV_VAR] = str(
            path_context.workspace_config_dir
        )
    # 2. Cloud config variables used by AwsAssets like aws_region and profile
    if ws_config.aws_region is not None:
        environ[constants.AWS_REGION_ENV_VAR] = ws_config.aws_region
    if ws_config.aws_profile is not None:
        environ[constants.AWS_PROFILE_ENV_VAR] = ws_config.aws_profile
    if ws_config.aws_config_file is not None:
        environ[constants.AWS_CONFIG_FILE_ENV_VAR] = ws_config.aws_config_file
    if ws_config.aws_shared_credentials_file is not None:
        environ[
            constants.AWS_SHARED_CREDENTIALS_FILE_ENV_VAR
        ] = ws_config.aws_shared_credentials_file
    if ws_config.local_env:
        environ.update(ws_config.local_env)


def run_workflows_local(
    workflow_file: str,
    workflows: Dict[str, Workflow],
    run_context: RunContext,
    ws_data: PhiWsData,
    workflow_name: Optional[str] = None,
) -> bool:
    """
    Runs a workflow in the local environment

    Args:
        workflow_file: Path of the workflow file relative to the products_dir.
            This is used to build the path_context
        workflows: Dict[str, Workflow] to run
        run_context: RunContext
        ws_data: PhiWsData
        workflow_name:

    Returns:
        run_status (bool): True is the Workflow ran successfully
    """

    # Validate
    if ws_data.ws_config is None:
        print_error("WorkspaceConfig invalid")
        return False
    if ws_data.ws_dir_path is None:
        print_error("Workspace directory invalid")
        return False

    # Step 1: Build the PathContext for the workflows.
    ws_config = ws_data.ws_config
    ws_dir_path = ws_data.ws_dir_path
    scripts_dir_path = ws_dir_path.joinpath(ws_config.scripts_dir).resolve()
    storage_dir_path = ws_dir_path.joinpath(ws_config.storage_dir).resolve()
    meta_dir_path = ws_dir_path.joinpath(ws_config.meta_dir).resolve()
    products_dir_path = ws_dir_path.joinpath(ws_config.products_dir).resolve()
    notebooks_dir_path = ws_dir_path.joinpath(ws_config.notebooks_dir).resolve()
    workspace_config_dir_path = ws_dir_path.joinpath(
        ws_config.workspace_config_dir
    ).resolve()
    workflow_file_path = Path(products_dir_path).joinpath(workflow_file)
    wf_path_context: PathContext = PathContext(
        scripts_dir=scripts_dir_path,
        storage_dir=storage_dir_path,
        meta_dir=meta_dir_path,
        products_dir=products_dir_path,
        notebooks_dir=notebooks_dir_path,
        workspace_config_dir=workspace_config_dir_path,
        workflow_file=workflow_file_path,
    )
    logger.debug(f"PathContext: {wf_path_context.json(indent=4)}")

    ######################################################################
    # NOTE: VERY IMPORTANT TO RUN BEFORE RUNNING ANY LOCAL WORKFLOWS
    # Update the local environment with Paths and Configuration
    ######################################################################
    set_local_env(ws_config=ws_config, path_context=wf_path_context)

    # Step 3: Run single Workflow if workflow_name is provided
    if workflow_name is not None:
        if workflow_name not in workflows:
            print_error(
                "Could not find '{}' in {}".format(
                    workflow_name, "[{}]".format(", ".join(workflows.keys()))
                )
            )
            return False

        wf_run_status: bool = False
        workflow_to_run = workflows[workflow_name]
        _name = workflow_name or workflow_to_run.name
        print_subheading(f"\nRunning {_name}")
        # Pass down context
        workflow_to_run.run_context = run_context
        workflow_to_run.path_context = wf_path_context
        wf_run_success = workflow_to_run.run_in_local_env()

        print_subheading("\nWorkflow run status:")
        print_info("{}: {}".format(_name, "Success" if wf_run_success else "Fail"))
        print_info("")
        return wf_run_success
    # Step 4: Run all Workflows if workflow_name is None
    else:
        wf_run_status: List[RunStatus] = []
        for wf_name, wf_obj in workflows.items():
            _name = wf_name or wf_obj.name
            print_subheading(f"\nRunning {_name}")
            # Pass down context
            wf_obj.run_context = run_context
            wf_obj.path_context = wf_path_context
            run_success = wf_obj.run_in_local_env()
            wf_run_status.append(RunStatus(_name, run_success))

        print_subheading("\nWorkflow run status:")
        print_info(
            "\n".join(
                [
                    "{}: {}".format(wf.name, "Success" if wf.success else "Fail")
                    for wf in wf_run_status
                ]
            )
        )
        print_info("")
        for _run in wf_run_status:
            if not _run.success:
                return False
        return True


def run_data_products_local(
    workflow_file: str,
    data_products: Dict[str, DataProduct],
    run_context: RunContext,
    ws_data: PhiWsData,
) -> bool:
    """

    Args:
        workflow_file: Path of the workflow file relative to the products_dir.
            This is used to build the path_context
        data_products: Dict[str, DataProduct] to run
        run_context: RunContext
        ws_data: PhiWsData

    Returns:
        run_status (bool): True is the DataProduct ran successfully
    """

    # Validate
    if ws_data.ws_dir_path is None:
        print_error("Workspace directory invalid")
        return False
    if ws_data.ws_config is None:
        print_error("WorkspaceConfig invalid")
        return False

    # Step 1: Build the PathContext for the DataProducts.
    ws_config = ws_data.ws_config
    ws_dir_path = ws_data.ws_dir_path
    scripts_dir_path = ws_dir_path.joinpath(ws_config.scripts_dir).resolve()
    storage_dir_path = ws_dir_path.joinpath(ws_config.storage_dir).resolve()
    meta_dir_path = ws_dir_path.joinpath(ws_config.meta_dir).resolve()
    products_dir_path = ws_dir_path.joinpath(ws_config.products_dir).resolve()
    notebooks_dir_path = ws_dir_path.joinpath(ws_config.notebooks_dir).resolve()
    workspace_config_dir_path = ws_dir_path.joinpath(
        ws_config.workspace_config_dir
    ).resolve()
    workflow_file_path = Path(products_dir_path).joinpath(workflow_file)
    dp_path_context: PathContext = PathContext(
        scripts_dir=scripts_dir_path,
        storage_dir=storage_dir_path,
        meta_dir=meta_dir_path,
        products_dir=products_dir_path,
        notebooks_dir=notebooks_dir_path,
        workspace_config_dir=workspace_config_dir_path,
        workflow_file=workflow_file_path,
    )
    logger.debug(f"PathContext: {dp_path_context.json(indent=4)}")

    ######################################################################
    # NOTE: VERY IMPORTANT TO RUN BEFORE RUNNING ANY LOCAL WORKFLOWS
    # Update the local environment with Paths and Configuration
    ######################################################################
    set_local_env(ws_config=ws_config, path_context=dp_path_context)

    # Step 3: Run the DataProducts
    dp_run_status: List[RunStatus] = []
    for dp_name, dp_obj in data_products.items():
        _name = dp_name or dp_obj.name
        print_subheading(f"\nRunning {_name}")
        # Pass down context
        dp_obj.run_context = run_context
        dp_obj.path_context = dp_path_context
        run_success = dp_obj.run_in_local_env()
        dp_run_status.append(RunStatus(_name, run_success))

    print_subheading("DataProduct run status:")
    print_info(
        "\n".join(
            [
                "{}: {}".format(dp.name, "Success" if dp.success else "Fail")
                for dp in dp_run_status
            ]
        )
    )
    print_info("")
    for _run in dp_run_status:
        if not _run.success:
            return False
    return True
