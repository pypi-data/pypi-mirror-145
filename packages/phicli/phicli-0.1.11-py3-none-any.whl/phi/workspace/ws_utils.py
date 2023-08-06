from pathlib import Path
from typing import Dict, Optional, Set, Tuple

from phi.backend_api.api_exceptions import CliAuthException
from phi.backend_api.auth_api import authenticate_and_get_user_schema
from phi.conf.constants import PHI_SIGNIN_URL_WITHOUT_PARAMS
from phi.conf.phi_conf import PhiWsData
from phi.schemas.user_schemas import UserSchema
from phi.utils.cli_auth_server import (
    get_port_for_auth_server,
    get_tmp_access_token_from_web_flow,
)
from phi.utils.cli_console import (
    print_info,
    print_info,
    print_error,
    print_subheading,
)
from phi.utils.common import is_empty
from phi.utils.log import logger
from phi.workspace.ws_enums import WorkspaceSetupActions
from phi.workspace.exceptions import WorkspaceConfigException


def get_ws_config_file_path(ws_dir: Path) -> Path:
    logger.debug(f"Looking for a workspace config for {ws_dir}")
    # Phidata looks for a workspace config dir in 2 places:
    # 1. In a folder with the same name as ws_dir
    # 2. In a folder named data
    #
    # When users have multiple workspaces in the same env, its better to have
    # different names for each package to separate the imports. So the package/folder
    # name is the same name as the workspace
    #
    # But in 99% of the cases, users will have 1 workspace per virtual env, so
    # using the workspace name: data works as a great default option

    ws_config_dir: Optional[Path] = None

    # Case 1: Look for a folder with the same name as ws_dir
    ws_root_name = ws_dir.stem
    # logger.debug(f"ws_dir: {ws_dir}")
    # logger.debug(f"ws_root_name: {ws_root_name}")
    ws_src_dir = ws_dir.joinpath(ws_root_name)
    if ws_src_dir.exists() and ws_src_dir.is_dir():
        ws_config_dir = ws_src_dir.joinpath("workspace")
    # Case 2: Look for a folder with the name: data
    if ws_config_dir is None:
        ws_data_dir = ws_dir.joinpath("data")
        if ws_data_dir.exists() and ws_data_dir.is_dir():
            ws_config_dir = ws_data_dir.joinpath("workspace")
    # logger.debug(f"ws_config_dir: {ws_config_dir}")

    if ws_config_dir is not None and ws_config_dir.exists() and ws_config_dir.is_dir():
        return ws_config_dir.joinpath("config.py")
    print_error(f"Could not find a workspace at: {ws_dir}")
    exit(0)


def get_ws_k8s_resources_dir_path(ws_dir: Path) -> Path:
    return ws_dir.joinpath("workspace").joinpath("prd")


def is_valid_ws_config_file_path(ws_config_file_path: Optional[Path]) -> bool:
    # TODO: add more checks for validating the ws_config_file_path
    if (
        ws_config_file_path is not None
        and ws_config_file_path.exists()
        and ws_config_file_path.is_file()
    ):
        return True
    return False


def select_version_contol_using_web_flow() -> Optional[UserSchema]:
    import typer

    port = get_port_for_auth_server()
    redirect_uri = "http%3A%2F%2Flocalhost%3A{}%2F".format(port)
    auth_url = "{}?source=cli&action=SELECT_VERSION_CONTROL&redirect_uri={}".format(
        PHI_SIGNIN_URL_WITHOUT_PARAMS, redirect_uri
    )
    print_info("\nYour browser will be opened to visit:\n\n{}\n".format(auth_url))
    typer.launch(auth_url)
    print_info("Waiting for a response from browser")

    tmp_access_token = get_tmp_access_token_from_web_flow(port)
    if tmp_access_token is None:
        print_error("tmp_access_token")
        return None
    try:
        user: Optional[UserSchema] = authenticate_and_get_user_schema(tmp_access_token)
    except CliAuthException as e:
        print_error("CliAuthException")
        return None

    return user


def get_ws_setup_status(ws_data: PhiWsData) -> Tuple[bool, str]:
    """This function validates that a workspace is properly set up and returns an
    error message if ws not setup. The error message is displayed to the user,
    so we need to make sure it doesn't contain any sensitive information.
    """

    # Version Control Provider check
    # user: UserSchema = config.user
    # if user.version_control_provider is None:
    #     return (
    #         False,
    #         "Version control provider not available. Please run `phi init -r` to initialize phi",
    #     )

    if ws_data is None:
        return (
            False,
            "WorkspaceSchema not yet registered with Phidata. Please run `phi ws init` to create a new workspace or `phi ws setup` for an existing workspace",
        )

    # Validate WorkspaceSchema Directory
    ws_dir_path: Optional[Path] = ws_data.ws_dir_path
    if ws_dir_path is None or not ws_dir_path.exists() or not ws_dir_path.is_dir():
        return (
            False,
            "The WorkspaceSchema directory is not available or invalid.\n\tTo create a new workspace, run `phi ws init`.\n\tFor an existing workspace, run `phi ws setup` from the workspace directory",
        )

    # Validate WorkspaceSchema Config Exists (we will validate the contents later)
    ws_config_file_path: Optional[Path] = ws_data.ws_config_file_path
    if (
        ws_config_file_path is None
        or not ws_config_file_path.exists()
        or not ws_config_file_path.is_file()
    ):
        return (
            False,
            "WorkspaceSchema config is not available or invalid. Please run `phi ws init` to create a new workspace or `phi ws setup` for an existing workspace",
        )

    # Validate that the workspace is registered with phidata
    if ws_data is not None and ws_data.ws_schema is None:
        return (
            False,
            "WorkspaceSchema not registered with phidata. Please run `phi ws setup` from the workspace dir",
        )

    # Validate that the workspace has a git repo
    if (
        ws_data is not None
        and ws_data.ws_schema is not None
        and is_empty(ws_data.ws_schema.git_url)
    ):
        return (
            False,
            "WorkspaceSchema does not have a remote origin setup. Please run `phi ws setup` from the workspace dir",
        )

    return (True, "WorkspaceSchema setup successful")


ws_setup_action_todo: Dict[WorkspaceSetupActions, str] = {
    WorkspaceSetupActions.WS_CONFIG_IS_AVL: "[ERROR] WorkspaceConfig is missing",
    WorkspaceSetupActions.WS_IS_AUTHENTICATED: "Workspace is not authenticated. run `phi auth` for more info",
    WorkspaceSetupActions.GCP_SVC_ACCOUNT_IS_AVL: "GCP Service Account is unavailable. run `phi gcp auth` for more info",
    WorkspaceSetupActions.GIT_REMOTE_ORIGIN_IS_AVL: "No git repo setup for workspace. run `phi ws git` for more info",
}


def print_howtofix_pending_actions(
    pending_actions: Optional[Set[WorkspaceSetupActions]],
) -> None:
    """This function prints how to fix pending setup actions for a workspace"""

    if pending_actions is None:
        return

    for action in pending_actions:
        print_info("\t" + ws_setup_action_todo.get(action, action.value))


def secho_ws_status(ws_data: PhiWsData) -> None:

    ws_dir_path: Optional[Path] = ws_data.ws_dir_path
    ws_config_file_path: Optional[Path] = ws_data.ws_config_file_path

    print_info("")
    print_subheading("WorkspaceSchema: {}".format(ws_data.ws_name))
    print_info("WorkspaceSchema Directory: {}".format(str(ws_dir_path)))
    print_info("Workspace Config file: {}".format(str(ws_config_file_path)))

    ws_is_setup, ws_setup_msg = get_ws_setup_status(ws_data)
    if ws_is_setup:
        print_info("WorkspaceSchema Status: Active")
    else:
        print_info("WorkspaceSchema Status: {}".format(ws_setup_msg))

    # ws_pak8_conf: Optional[Pak8Conf] = ws_data.ws_pak8_conf
    # if ws_pak8_conf and ws_pak8_conf.cloud_provider == pak8_Pak8CloudProvider.GCP:
    #     secho_gcp_status(ws_data)
