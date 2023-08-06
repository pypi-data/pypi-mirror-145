import datetime
from pathlib import Path
from typing import List, Optional, Set

from pydantic import BaseModel
from phidata.workspace import WorkspaceConfig

from phi.utils.common import is_empty
from phi.utils.dttm import current_datetime_utc
from phi.utils.log import logger
from phi.workspace.ws_enums import WorkspaceSetupActions
from phi.workspace.exceptions import WorkspaceConfigException
from phi.workspace.ws_schemas import WorkspaceSchema


class PhiWsData(BaseModel):
    """The PhiWsData model stores data for a phidata workspace."""

    # Name of the workspace
    ws_name: str
    # WorkspaceSchema: If exists then indicates that this ws has been authenticated
    # with the backend
    ws_schema: Optional[WorkspaceSchema] = None
    # The root directory for the workspace.
    # This field indicates that this ws has been downloaded on this machine
    ws_dir_path: Optional[Path] = None
    # WorkspaceConfig for the workspace
    ws_config: Optional[WorkspaceConfig] = None
    # Path for the WorkspaceConfig file
    ws_config_file_path: Optional[Path] = None
    # A Set of WorkspaceSetupActions which this workspace must satisfy to become valid.
    # if len(ws_data.required_actions.intersection(ws_data.pending_actions)) > 0:
    # the workspace is invalid
    required_actions: Set[WorkspaceSetupActions] = {
        WorkspaceSetupActions.WS_CONFIG_IS_AVL
    }
    # A Set of WorkspaceSetupActions which this workspace currently has not
    # completed and needs to fulfill.
    # When (pending_actions is None or len(pending_actions) == 0), the workspace is valid
    pending_actions: Set[WorkspaceSetupActions] = set()
    # Timestamp of when this workspace was created on the users machine
    create_ts: datetime.datetime = current_datetime_utc()
    # Timestamp when this ws was last updated
    last_update_ts: Optional[datetime.datetime] = None

    class Config:
        arbitrary_types_allowed = True

    ######################################################
    ## WorkspaceConfig functions
    ######################################################

    def load_workspace_from_config_file(self) -> None:

        if self.ws_config_file_path is None or self.ws_dir_path is None:
            raise WorkspaceConfigException("WorkspaceConfig invalid")

        from phi.workspace.ws_loader import load_workspace

        logger.debug(f"**--> Loading WorkspaceConfig")
        ws_configs: List[WorkspaceConfig]
        ws_configs = load_workspace(self.ws_config_file_path)

        if is_empty(ws_configs):
            logger.debug(f"No WorkspaceConfig found")
            self.ws_config = None
            raise WorkspaceConfigException("No WorkspaceConfig found")

        if len(ws_configs) > 1:
            logger.warning(
                "Found {} WorkspaceConfigs, first one will be selected".format(
                    len(ws_configs)
                )
            )
        ws_config: WorkspaceConfig = ws_configs[0]
        # logger.debug("loading workspace config:\n{}".format(ws_config.args))
        self.ws_config = ws_config

    ######################################################
    ## Print functions
    ######################################################

    def print_to_cli(self):
        from rich.pretty import pprint

        pprint(self.dict())
