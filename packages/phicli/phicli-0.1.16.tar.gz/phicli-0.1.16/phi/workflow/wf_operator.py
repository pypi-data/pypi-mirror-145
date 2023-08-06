from pathlib import Path
from typing import Optional, Dict, List

from phidata.product import DataProduct
from phidata.workflow import Workflow
from phidata.workspace import WorkspaceConfig
from phidata.types.context import RunContext
from pydantic import ValidationError

from phi.utils.cli_console import (
    print_error,
    print_info,
    print_subheading,
    print_heading,
    print_info,
    print_warning,
)
from phi.utils.log import logger
from phi.workflow.wf_enums import WorkflowEnv
from phi.workflow.wf_utils import (
    get_workflow_file_and_name,
    get_data_products_and_workflows_from_file,
)
from phi.workspace.phi_ws_data import PhiWsData


def run_workflow(
    wf_description: str,
    ws_data: PhiWsData,
    target_env: WorkflowEnv,
    target_dt: str,
    dry_run: bool,
    target_app: Optional[str] = None,
    run_env_vars: Optional[Dict[str, str]] = None,
    run_params: Optional[Dict[str, str]] = None,
) -> None:
    """Runs the Phidata Workflow in the target environment.
    The run_workflow() function is called from `phi wf run`
    """

    if ws_data is None or ws_data.ws_config is None:
        print_error("WorkspaceConfig invalid")
        return
    ws_config: WorkspaceConfig = ws_data.ws_config

    # Step 1: Get the ws_dir_path and products_dir
    if ws_data.ws_dir_path is None:
        print_error("Workspace directory invalid")
        return
    ws_dir_path: Path = ws_data.ws_dir_path

    if ws_config.products_dir is None:
        print_error("Products directory invalid")
        return
    products_dir: str = ws_config.products_dir

    # Step 2: Get the workflow_file and workflow_name
    # The workflow_file is the path of the file relative to the products_dir.
    workflow_file, workflow_name = get_workflow_file_and_name(
        wf_description=wf_description,
        ws_dir_path=ws_dir_path,
        ws_name=ws_data.ws_name,
        products_dir=products_dir,
    )
    # Validate workflow_file
    if workflow_file is None:
        print_error("Workflow file not found")
        return
    print_heading(f"Running workflow: {wf_description}")
    print_info("Loading file: {}".format(workflow_file))
    if workflow_name:
        print_info("Workflow: {}".format(workflow_name))

    # Step 3: Get the absolute workflow_file_path
    workflow_file_path: Path
    try:
        workflow_file_path = (
            ws_dir_path
            .joinpath(products_dir)
            .joinpath(workflow_file)
            .resolve(strict=True)
        )
    except FileNotFoundError as e:
        print_error("Workflow file not found: {}".format(workflow_file))
        return

    # Step 4: Get DataProducts/Workflows in the workflow_file_path
    dp_dict: Dict[str, DataProduct]
    wf_dict: Dict[str, Workflow]
    try:
        dp_dict, wf_dict = get_data_products_and_workflows_from_file(workflow_file_path)
    except ValidationError as e:
        from phidata.utils.cli_console import print_validation_errors

        print_validation_errors(e.errors())
        print_info("Please fix and try again")
        return

    # Final run status
    run_status: bool = False
    # Build the RunContext
    run_context = RunContext(
        run_date=target_dt,
        dry_run=dry_run,
        run_env=target_env.value,
        run_env_vars=run_env_vars,
        run_params=run_params,
    )

    # Step 5: Run DataProducts/Workflows in target runtime
    # Run Workflow locally
    if target_env == WorkflowEnv.local:
        from phi.local.local_operator import run_workflows_local
        from phi.local.local_operator import run_data_products_local

        # ** CASE 1: If a workflow_name is provided
        #   Run only the Workflow
        if workflow_name is not None and len(wf_dict) > 0:
            run_status = run_workflows_local(
                workflow_file=workflow_file,
                workflows=wf_dict,
                run_context=run_context,
                ws_data=ws_data,
                workflow_name=workflow_name,
            )
        # ** CASE 2: If a workflow_name is not provided
        #   but workflow_file contains DataProducts.
        #   Run the DataProducts
        elif dp_dict is not None and len(dp_dict) > 0:
            run_status = run_data_products_local(
                workflow_file=workflow_file,
                data_products=dp_dict,
                run_context=run_context,
                ws_data=ws_data,
            )
        # ** CASE 3: If a workflow_name is not provided
        #   and workflow_file does NOT contain DataProducts
        #   but workflow_file contains Workflows
        #   Run the Workflows
        elif wf_dict is not None and len(wf_dict) > 0:
            run_status = run_workflows_local(
                workflow_file=workflow_file,
                workflows=wf_dict,
                run_context=run_context,
                ws_data=ws_data,
            )
    # Run Workflow in docker
    elif target_env == WorkflowEnv.dev:
        from phidata.infra.docker.config import DockerConfig
        from phi.docker.docker_operator import (
            run_workflows_docker,
            run_data_products_docker,
        )

        docker_configs: Optional[List[DockerConfig]] = ws_config.docker
        docker_config_to_use: Optional[DockerConfig] = None
        if docker_configs is not None and isinstance(docker_configs, list):
            if len(docker_configs) == 1:
                docker_config_to_use = docker_configs[0]
            else:
                for dc in docker_configs:
                    if dc.env == target_env:
                        docker_config_to_use = dc
                        break
        if docker_config_to_use is None:
            print_error(f"No DockerConfig found for env: {target_env.value}")
            return

        ######################################################################
        # NOTE: VERY IMPORTANT TO GET RIGHT
        # Update sub-configs data using WorkspaceConfig
        # 1. Pass down the paths from the WorkspaceConfig
        #       These paths are used everywhere from Infra to Apps
        # 2. Pass down docker_env which is used to set the env variables
        #       when running the docker command
        ######################################################################

        # The ws_dir_path is the ROOT directory for the workspace
        docker_config_to_use.workspace_root_path = ws_data.ws_dir_path
        docker_config_to_use.workspace_config_file_path = ws_data.ws_config_file_path
        docker_config_to_use.scripts_dir = ws_config.scripts_dir
        docker_config_to_use.storage_dir = ws_config.storage_dir
        docker_config_to_use.meta_dir = ws_config.meta_dir
        docker_config_to_use.products_dir = ws_config.products_dir
        docker_config_to_use.notebooks_dir = ws_config.notebooks_dir
        docker_config_to_use.workspace_config_dir = ws_config.workspace_config_dir
        docker_config_to_use.docker_env = ws_config.docker_env

        # ** CASE 1: If a workflow_name is provided
        #   Run only the Workflow
        if workflow_name is not None and len(wf_dict) > 0:
            # Because this is a single workflow, we need to identify the DAG
            # it belongs to. Workflow DAGs are usually provided by their DataProducts.
            # But Workflows can independently have their own DAGs as well.
            # To run a single workflow, lets find out if this workflow
            #   is a part of a DataProduct
            #   or an independent workflow
            wf_dag_id = None
            logger.debug(f"Finding DAG for {workflow_name}")
            if len(dp_dict) > 0:
                if workflow_name not in wf_dict:
                    print_error(
                        "Could not find '{}' in {}".format(
                            workflow_name, "[{}]".format(", ".join(wf_dict.keys()))
                        )
                    )
                else:
                    _workflow = wf_dict[workflow_name]
                    # logger.debug(f"Found workflow: {_workflow}")
                    for dp_name, dp_obj in dp_dict.items():
                        dp_workflows = dp_obj.workflows
                        # logger.debug(f"dp_workflows: {dp_workflows}")
                        if dp_workflows is not None and _workflow in dp_workflows:
                            # logger.debug(f"Found data product: {dp_name}")
                            wf_dag_id = dp_obj.dag_id
                            print_info(f"Workflow DAG: {wf_dag_id}")

            run_status = run_workflows_docker(
                workflow_file=workflow_file,
                workflows=wf_dict,
                run_context=run_context,
                docker_config=docker_config_to_use,
                target_app=target_app,
                workflow_name=workflow_name,
                use_dag_id=wf_dag_id,
            )
        # ** CASE 2: If a workflow_name is not provided
        #   but workflow_file contains DataProducts.
        #   Run the DataProducts
        elif dp_dict is not None and len(dp_dict) > 0:
            run_status = run_data_products_docker(
                workflow_file=workflow_file,
                data_products=dp_dict,
                run_context=run_context,
                docker_config=docker_config_to_use,
                target_app=target_app,
            )
        # ** CASE 3: If a workflow_name is not provided
        #   and workflow_file does NOT contain DataProducts
        #   but workflow_file contains Workflows
        #   Run the Workflows
        elif wf_dict is not None and len(wf_dict) > 0:
            run_status = run_workflows_docker(
                workflow_file=workflow_file,
                workflows=wf_dict,
                run_context=run_context,
                docker_config=docker_config_to_use,
                target_app=target_app,
            )
    # Run Workflow in staging k8s
    elif target_env == WorkflowEnv.stg:
        print_error(f"WorkflowEnv: {target_env} not yet supported")
    # Run Workflow in prod k8s
    elif target_env == WorkflowEnv.prd:
        print_warning(
            f"Running workflows in {target_env.value} is in alpha, please verify results"
        )
        from phidata.infra.k8s.config import K8sConfig
        from phi.k8s.k8s_operator import (
            run_workflows_k8s,
            run_data_products_k8s,
        )

        k8s_configs: Optional[List[K8sConfig]] = ws_config.k8s
        k8s_config_to_use: Optional[K8sConfig] = None
        if k8s_configs is not None and isinstance(k8s_configs, list):
            if len(k8s_configs) == 1:
                k8s_config_to_use = k8s_configs[0]
            else:
                for dc in k8s_configs:
                    if dc.env == target_env:
                        k8s_config_to_use = dc
                        break
        if k8s_config_to_use is None:
            print_error(f"No K8sConfig found for env: {target_env.value}")
            return

        ######################################################################
        # NOTE: VERY IMPORTANT TO GET RIGHT
        # Update sub-configs data using WorkspaceConfig
        # 1. Pass down the paths from the WorkspaceConfig
        #       These paths are used everywhere from Infra to Apps
        # 2. Pass down k8s_env which is used to set the env variables
        #       when running the k8s command
        ######################################################################

        # The ws_dir_path is the ROOT directory for the workspace
        k8s_config_to_use.workspace_root_path = ws_data.ws_dir_path
        k8s_config_to_use.workspace_config_file_path = ws_data.ws_config_file_path
        k8s_config_to_use.scripts_dir = ws_config.scripts_dir
        k8s_config_to_use.storage_dir = ws_config.storage_dir
        k8s_config_to_use.meta_dir = ws_config.meta_dir
        k8s_config_to_use.products_dir = ws_config.products_dir
        k8s_config_to_use.notebooks_dir = ws_config.notebooks_dir
        k8s_config_to_use.workspace_config_dir = ws_config.workspace_config_dir
        k8s_config_to_use.k8s_env = ws_config.k8s_env

        # ** CASE 1: If a workflow_name is provided
        #   Run only the Workflow
        if workflow_name is not None and len(wf_dict) > 0:
            # Because this is a single workflow, we need to identify the DAG
            # it belongs to. Workflow DAGs are usually provided by their DataProducts.
            # But Workflows can independently have their own DAGs as well.
            # To run a single workflow, lets find out if this workflow
            #   is a part of a DataProduct
            #   or an independent workflow
            wf_dag_id = None
            logger.debug(f"Finding DAG for {workflow_name}")
            if len(dp_dict) > 0:
                if workflow_name not in wf_dict:
                    print_error(
                        "Could not find '{}' in {}".format(
                            workflow_name, "[{}]".format(", ".join(wf_dict.keys()))
                        )
                    )
                else:
                    _workflow = wf_dict[workflow_name]
                    # logger.debug(f"Found workflow: {_workflow}")
                    for dp_name, dp_obj in dp_dict.items():
                        dp_workflows = dp_obj.workflows
                        # logger.debug(f"dp_workflows: {dp_workflows}")
                        if dp_workflows is not None and _workflow in dp_workflows:
                            # logger.debug(f"Found data product: {dp_name}")
                            wf_dag_id = dp_obj.dag_id
                            print_info(f"Workflow DAG: {wf_dag_id}")

            run_status = run_workflows_k8s(
                workflow_file=workflow_file,
                workflows=wf_dict,
                run_context=run_context,
                k8s_config=k8s_config_to_use,
                target_app=target_app,
                workflow_name=workflow_name,
                use_dag_id=wf_dag_id,
            )
        # ** CASE 2: If a workflow_name is not provided
        #   but workflow_file contains DataProducts.
        #   Run the DataProducts
        elif dp_dict is not None and len(dp_dict) > 0:
            run_status = run_data_products_k8s(
                workflow_file=workflow_file,
                data_products=dp_dict,
                run_context=run_context,
                k8s_config=k8s_config_to_use,
                target_app=target_app,
            )
        # ** CASE 3: If a workflow_name is not provided
        #   and workflow_file does NOT contain DataProducts
        #   but workflow_file contains Workflows
        #   Run the Workflows
        elif wf_dict is not None and len(wf_dict) > 0:
            run_status = run_workflows_k8s(
                workflow_file=workflow_file,
                workflows=wf_dict,
                run_context=run_context,
                k8s_config=k8s_config_to_use,
                target_app=target_app,
            )
    else:
        print_error(f"WorkflowEnv: {target_env} not supported")

    # Report the run_status
    if run_status:
        print_heading("Workflow run success")
    else:
        print_error("Workflow run failure")


def list_workflows(
    wf_description: str,
    ws_data: PhiWsData,
) -> None:

    if ws_data is None or ws_data.ws_config is None:
        print_error("WorkspaceConfig invalid")
        return
    ws_config: WorkspaceConfig = ws_data.ws_config

    # Step 1: Get the ws_dir_path and products_dir
    if ws_data.ws_dir_path is None:
        print_error("Workspace directory invalid")
        return
    ws_dir_path: Path = ws_data.ws_dir_path

    if ws_config.products_dir is None:
        print_error("Products directory invalid")
        return
    products_dir: str = ws_config.products_dir

    # Step 2: Get the workflow_file and workflow_name
    # The workflow_file is the path of the file relative to the products_dir.
    workflow_file, workflow_name = get_workflow_file_and_name(
        wf_description=wf_description,
        ws_dir_path=ws_dir_path,
        ws_name=ws_data.ws_name,
        products_dir=products_dir,
    )
    # Validate workflow_file
    if workflow_file is None:
        print_error("Workflow file not found")
        return
    print_heading(f"Workflows in: {wf_description}")
    print_info("Loading file: {}".format(workflow_file))
    if workflow_name:
        print_info("Workflow: {}".format(workflow_name))

    # Step 3: Get the absolute workflow_file_path
    workflow_file_path: Path
    try:
        workflow_file_path = (
            ws_dir_path
            .joinpath(products_dir)
            .joinpath(workflow_file)
            .resolve(strict=True)
        )
    except FileNotFoundError as e:
        print_error("Workflow file not found: {}".format(workflow_file))
        return

    # Step 4: Get DataProducts/Workflows in the workflow_file_path
    dp_dict: Dict[str, DataProduct]
    wf_dict: Dict[str, Workflow]
    try:
        dp_dict, wf_dict = get_data_products_and_workflows_from_file(workflow_file_path)
    except ValidationError as e:
        from phidata.utils.cli_console import print_validation_errors

        print_validation_errors(e.errors())
        print_info("Please fix and try again")
        return

    # Step 5: Print :)
    if dp_dict is not None and len(dp_dict) > 0:
        print_heading(f"\nFound {len(dp_dict)} DataProduct(s)")
        for key, dp in dp_dict.items():
            print_info("{}: {}".format(key, dp.name))
    if wf_dict is not None and len(wf_dict) > 0:
        print_heading(f"\nFound {len(wf_dict)} Workflow(s)")
        for key, wf in wf_dict.items():
            print_info("{}: {}".format(key, wf.name))
        if workflow_name is not None:
            if workflow_name not in wf_dict:
                print_info("")
                print_warning(
                    "Could not find '{}' in {}".format(
                        workflow_name, "[{}]".format(", ".join(wf_dict.keys()))
                    )
                )
