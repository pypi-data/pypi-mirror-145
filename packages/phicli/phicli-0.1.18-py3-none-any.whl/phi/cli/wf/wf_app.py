"""Phi Workflow Cli

This is the entrypoint for the `phi wf` commands
"""

from typing import Optional

import typer

from phi.utils.cli_console import (
    print_error,
    print_info,
    print_conf_not_available_msg,
    print_active_workspace_not_available,
    print_available_workspaces,
)
from phi.utils.dttm import yesterday_datetime, dttm_to_dttm_str
from phi.utils.log import logger, set_log_level_to_debug
from phi.workflow.wf_enums import WorkflowEnv

wf_app = typer.Typer(
    name="wf",
    short_help="Commands to build and run workflows",
    help="""\b
Use `phi wf <command>` to build and run workflows.
Run `phi wf <command> --help` for more info.
    """,
    no_args_is_help=True,
    add_completion=False,
    invoke_without_command=True,
    options_metavar="\b",
    subcommand_metavar="<command>",
)


@wf_app.command(short_help="Run workflow", options_metavar="\b", no_args_is_help=True)
def run(
    wf_description: str = typer.Argument(
        ...,
        help="Workflow description. Format - Dir/File:Workflow. Where `Dir` is the path to the workflow dir relative to the products dir",
        metavar="[wf_desc]",
    ),
    env_filter: Optional[str] = typer.Option(
        "local",
        "-e",
        "--env",
        metavar="",
        help="The environment to run the workflow in. Default: local. Available Options: {}".format(
            WorkflowEnv.values_list()
        ),
    ),
    app_name: Optional[str] = typer.Option(
        None,
        "-a",
        metavar="",
        help="The App to run the workflow in. Default: `databox`",
    ),
    run_date: Optional[str] = typer.Option(
        None, "-dt", help="Run datetime for the workflow. Default: yesterday"
    ),
    dry_run: bool = typer.Option(
        False,
        "-dr",
        "--dry-run",
        help="Perform a dry run for each task. Does not run the task.",
    ),
    print_debug_log: bool = typer.Option(
        False,
        "-d",
        "--debug",
        help="Print debug logs.",
    ),
):
    """\b
    Run a workflow in the target environment.

    \b
    Examples:
    $ phi wf run dau -> Runs file: dau/dau.py, data products: all
    $ phi wf run dau:save -> Runs file: dau/dau.py, workflow: save
    $ phi wf run dau/dau2:save -> Runs file: dau/dau2.py, workflow: save
    """
    from phi.conf.phi_conf import PhiConf, PhiWsData
    from phi.workflow.wf_operator import run_workflow

    if print_debug_log:
        set_log_level_to_debug()

    phi_conf: Optional[PhiConf] = PhiConf.get_saved_conf()
    if not phi_conf:
        print_conf_not_available_msg()
        return

    active_ws_data: Optional[PhiWsData] = phi_conf.get_active_ws_data(refresh=True)
    if active_ws_data is None:
        print_active_workspace_not_available()
        avl_ws = phi_conf.available_ws
        if avl_ws:
            print_available_workspaces(avl_ws)
        return

    target_env: Optional[WorkflowEnv] = None
    target_app: Optional[str] = app_name
    target_dt: str = run_date or dttm_to_dttm_str(
        yesterday_datetime(), dttm_format="%Y-%m-%d"
    )

    target_env_str = env_filter or active_ws_data.ws_config.default_env or "dev"
    try:
        target_env = WorkflowEnv.from_str(target_env_str)
    except Exception as e:
        print_error(e)
        print_error(
            f"{target_env_str} is not supported, please choose from: {WorkflowEnv.values_list()}"
        )
        return

    logger.debug("Running workflow")
    logger.debug(f"\tworkflow     : {wf_description}")
    logger.debug(f"\ttarget_env   : {target_env}")
    logger.debug(f"\ttarget_dt    : {target_dt}")
    logger.debug(f"\tdry_run      : {dry_run}")
    logger.debug(f"\ttarget_app   : {target_app}")
    run_workflow(
        wf_description=wf_description,
        ws_data=active_ws_data,
        target_env=target_env,
        target_dt=target_dt,
        dry_run=dry_run,
        target_app=target_app,
    )


@wf_app.command(short_help="Build workflow")
def build(workflow: str = typer.Argument(..., help="The workflow to build")):
    print_info(f"Building workflow {workflow}")
    print_info(f"To be implemented")


@wf_app.command(short_help="List workflows", options_metavar="\b", no_args_is_help=True)
def ls(
    wf_description: str = typer.Argument(
        ...,
        help="Workflow description. Format - Dir/File:Workflow. Where `Dir` is the path to the workflow dir relative to the products dir",
        metavar="[wf_desc]",
    ),
    print_debug_log: bool = typer.Option(
        False,
        "-d",
        "--debug",
        help="Print debug logs.",
    ),
):
    from phi.conf.phi_conf import PhiConf, PhiWsData
    from phi.workflow.wf_operator import list_workflows

    if print_debug_log:
        set_log_level_to_debug()

    phi_conf: Optional[PhiConf] = PhiConf.get_saved_conf()
    if not phi_conf:
        print_conf_not_available_msg()
        return

    active_ws_data: Optional[PhiWsData] = phi_conf.get_active_ws_data(refresh=True)
    if active_ws_data is None:
        print_active_workspace_not_available()
        avl_ws = phi_conf.available_ws
        if avl_ws:
            print_available_workspaces(avl_ws)
        return

    list_workflows(
        wf_description=wf_description,
        ws_data=active_ws_data,
    )
