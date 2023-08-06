from collections import OrderedDict
from pathlib import Path
from typing import Any, Dict, List, Optional, Set, Tuple

from phi.conf.constants import PHI_CONF_PATH
from phi.schemas.user_schemas import UserSchema
from phi.utils.cli_console import (
    print_available_workspaces,
    print_info,
    print_dict,
    print_error,
    print_heading,
    print_horizontal_line,
    print_info,
    print_subheading,
)
from phi.utils.common import pickle_object_to_file, unpickle_object_from_file
from phi.utils.dttm import current_datetime_utc
from phi.utils.filesystem import delete_from_fs
from phi.utils.log import logger
from phi.workspace.phi_ws_data import PhiWsData
from phi.workspace.ws_enums import WorkspaceSetupActions
from phi.workspace.ws_schemas import WorkspaceSchema


class PhiConf:
    """The PhiConf class manages data for the phi cli"""

    def __init__(self):
        # Current user, populated after authenticating with the backend
        # To add a user, use the user setter
        self._user: Optional[UserSchema] = None

        # Primary ws for the user - used as the default for `phi ws` commands
        # To add a primary workspace, use the active_ws_name setter
        self._active_ws_name: Optional[str] = None

        # ** The self._ws_data_map holds the data for all workspaces available to this user.
        self._ws_data_map: Dict[str, PhiWsData] = OrderedDict()
        # When phi is initialized using `phi init`, this is an empty dict
        # When the user is authenticated, we get a list of all the workspaces this user has access to.
        # These workspaces are then added using the `primary_ws` and `available_ws` setters.
        # Note: These workspaces arent yet cloned on the users machines and only a record of their availability is kept
        # When the workspace is setup on the users machine, we update the remaining workspace data.

        # Quick access from ws_path -> ws data.
        self._path_to_ws_data_map: Dict[Path, PhiWsData] = OrderedDict()

        # Save the config to disk once initialized
        self.save_config()

    ######################################################
    ## User functions
    ######################################################

    @property
    def user(self) -> Optional[UserSchema]:
        return self._user

    @user.setter
    def user(self, user: Optional[UserSchema]) -> None:
        """Sets the user"""
        if user is not None:
            self._user = user
            self.save_config()

    ######################################################
    ## Workspace functions
    ######################################################

    @property
    def active_ws_name(self) -> Optional[str]:
        return self._active_ws_name

    @active_ws_name.setter
    def active_ws_name(self, ws_name: Optional[str]) -> None:
        """Set the active_ws_name during phi auth"""
        if ws_name is not None:
            self._active_ws_name = ws_name
            self._add_or_update_ws_data(ws_name=ws_name)
            self.save_config()

    @property
    def available_ws(self) -> List[WorkspaceSchema]:
        return [
            w.ws_schema for w in self._ws_data_map.values() if w.ws_schema is not None
        ]

    @available_ws.setter
    def available_ws(self, avl_ws: Optional[List[WorkspaceSchema]]) -> None:
        """Set the available ws during phi init"""
        if avl_ws:
            for ws_schema in avl_ws:
                self._add_or_update_ws_data(ws_name=ws_schema.name, ws_schema=ws_schema)
            self.save_config()

    def _add_or_update_ws_data(
        self,
        ws_name: str,
        ws_schema: Optional[WorkspaceSchema] = None,
        ws_dir_path: Optional[Path] = None,
        ws_config_file_path: Optional[Path] = None,
        refresh_data: bool = False,
    ) -> None:
        """Create or update PhiWsData in PhiConf.
        ws_name is the only required argument.
        This function does not call self.save_config(). call it from the parent.

        This function is called from 5 places:
        1. During `phi auth` when primary/available workspaces are requested from the backend.
        2. During `phi ws init` when a new workspace is created on the users machine.
        3. When the user already has a local workspace dir on their machine
            and need to manually add the ws to the PhiConf
            (possible after running `phi init -r` which reset the config)
        4. Whenever ws config, creds or data needs to be refreshed. This function is called with just the `ws_name` arg
        5. When primary or available workspaces are updated, this function is called from the
            @primary_ws.setter and @available_ws.setter with the ws_name and ws_schema

        Note: Cloud data (ws_gcp_data etc.) should be updated using their respective functions.
        """

        ######################################################
        # Validate ws_name and ws_schema
        ######################################################

        # ws_name should not be None
        if ws_name is None or not isinstance(ws_name, str):
            return

        ######################################################
        # Create ws_data
        ######################################################

        if ws_name not in self._ws_data_map:
            logger.debug(f"Adding new ws {ws_name} to PhiConf")
            self._ws_data_map[ws_name] = PhiWsData(
                ws_name=ws_name,
                ws_schema=ws_schema,
                ws_dir_path=ws_dir_path,
                ws_config_file_path=ws_config_file_path,
            )
            if ws_dir_path:
                self._path_to_ws_data_map[ws_dir_path] = self._ws_data_map[ws_name]
            logger.debug(
                "Created new Workspace: {}".format(
                    self._ws_data_map[ws_name].json(indent=2)
                )
            )

        ######################################################
        # Update or Refresh ws_data
        ######################################################

        # By this point there should be a PhiWsData object for this ws_name
        # If by chance ws_name not in self._ws_data_map, then we just create a new PhiWsData object
        existing_ws_data: PhiWsData = self._ws_data_map.get(
            ws_name, PhiWsData(ws_name=ws_name)
        )
        # Make a deep copy of the existing workspace data
        # This allows us to update the fields we want, and keep any existing fields as is
        _ws_data: PhiWsData = existing_ws_data.copy(deep=True)

        # Add values where available
        if ws_schema is not None and ws_schema != existing_ws_data.ws_schema:
            logger.info("Updating ws_schema")
            _ws_data.ws_schema = ws_schema
        if ws_dir_path is not None and ws_dir_path != existing_ws_data.ws_dir_path:
            logger.info("Updating ws_dir_path")
            _ws_data.ws_dir_path = ws_dir_path
        if (
            ws_config_file_path is not None
            and ws_config_file_path != existing_ws_data.ws_config_file_path
        ):
            logger.info("Updating ws_config_file_path")
            _ws_data.ws_config_file_path = ws_config_file_path

        # Refresh the WorkspaceConfig if needed.
        # There are 3 cases where we read/parse the WorkspaceConfig
        # 1. refresh_data == True
        # 2. ws_config_file_path has changed
        # 3. current ws_config is None
        # But before we refresh the WorkspaceConfig, we need to check if a ws_config_file_path is available
        if _ws_data.ws_config_file_path is not None:
            if (
                refresh_data
                or _ws_data.ws_config_file_path != existing_ws_data.ws_config_file_path
                or _ws_data.ws_config is None
            ):
                _ws_data.load_workspace_from_config_file()
        _ws_data.last_update_ts = current_datetime_utc()

        # Point the ws_data in _ws_data_map and _path_to_ws_data_map to _ws_data
        logger.debug(f"Updating ws_data_map object for: {ws_name}")
        # Pop the existing object from the self._ws_data_map
        if ws_name in self._ws_data_map:
            popped_ws_data_from_map: Optional[PhiWsData] = self._ws_data_map.pop(
                ws_name
            )
            # logger.debug(f"Removed existing ws_data for {ws_name} from mapping")
        self._ws_data_map[ws_name] = _ws_data

        if _ws_data.ws_dir_path is not None:
            # If the ws_dir_path has been updated, pop the existing_ws_data.ws_dir_path
            if (
                existing_ws_data.ws_dir_path is not None
                and existing_ws_data.ws_dir_path in self._path_to_ws_data_map
            ):
                popped_ws_data_from_path_map: Optional[
                    PhiWsData
                ] = self._path_to_ws_data_map.pop(existing_ws_data.ws_dir_path)
            self._path_to_ws_data_map[_ws_data.ws_dir_path] = self._ws_data_map[ws_name]

        ######################################################
        # END
        ######################################################

    def add_new_created_ws_to_config(
        self,
        ws_name: str,
        ws_dir_path: Path,
        ws_config_file_path: Path,
        refresh_data: bool = False,
    ) -> None:
        """Adds a newly created workspace to the PhiConf"""
        self._add_or_update_ws_data(
            ws_name=ws_name,
            ws_dir_path=ws_dir_path,
            ws_config_file_path=ws_config_file_path,
            refresh_data=refresh_data,
        )
        self.save_config()

    def update_ws_schema_for_workspace(
        self,
        ws_schema: WorkspaceSchema,
        set_as_primary: bool = False,
    ) -> None:
        """Updates the schema for a workspace and sets as primary if needed"""
        self._add_or_update_ws_data(
            ws_name=ws_schema.name,
            ws_schema=ws_schema,
        )
        if set_as_primary:
            self.active_ws_name = ws_schema.name
        self.save_config()

    def update_ws_data(
        self,
        ws_name: str,
        ws_schema: Optional[WorkspaceSchema] = None,
        ws_dir_path: Optional[Path] = None,
        ws_config_file_path: Optional[Path] = None,
    ) -> None:
        """Update workspace data and return True if successful"""

        print_info(f"Updating ws_data for {ws_name}")
        self._add_or_update_ws_data(
            ws_name=ws_name,
            ws_schema=ws_schema,
            ws_dir_path=ws_dir_path,
            ws_config_file_path=ws_config_file_path,
        )
        self.save_config()

    def update_ws_data_for_cloned_ws(
        self,
        ws_name: str,
        ws_dir_path: Path,
        ws_config_file_path: Path,
    ) -> bool:
        """For a workspace to be cloned, it would already have ws_data and ws_schema available.
        After the directory from the git_url is cloned, we can fill in the gaps to update
        the ws_data for the workspace. Call this function through ws_operator.clone_workspace()
        """
        ws_data: Optional[PhiWsData] = self._ws_data_map.get(ws_name, None)
        if ws_data is None:
            return False

        self._add_or_update_ws_data(
            ws_name=ws_name,
            ws_dir_path=ws_dir_path,
            ws_config_file_path=ws_config_file_path,
        )
        self.save_config()
        return True

    def add_ws_data_using_config_file(
        self, ws_dir_path: Path, ws_config_file_path: Optional[Path]
    ) -> Optional[PhiWsData]:
        """Maps a ws at `ws_dir_path` to an available workspace. using the config file at `ws_config_file_path`.
        Also updates the ws_config_file_path in the ws_data if provided.

        This is used in 2 cases:
        1. If the user ran `phi init -r`, the PhiConf gets erased and so does self._path_to_ws_data_map
            So there is no link from the ws_dir_path to the workspace.
        2. The user manually cloned the workspace directory. In that case we don't have a record of this
            ws_dir_path matching any available workspace.

        This function basically reads the workspace config and tries to map it to an available workspace.
        Returns the PhiWsData if successful
        """

        logger.debug(f"Looking for the workspace at {ws_dir_path}")
        _best_guess_ws_name = ws_dir_path.stem
        logger.debug(f"_best_guess_ws_name: {_best_guess_ws_name}")
        _ws_schema: Optional[WorkspaceSchema] = None
        for avl_ws in self.available_ws:
            if avl_ws.name == _best_guess_ws_name:
                _ws_schema = avl_ws
            break
        if _ws_schema is None:
            print_error(
                f"Workspace name: {_best_guess_ws_name} does not match any available workspaces"
            )
            print_available_workspaces(self.available_ws)
            return None

        logger.debug(f"Found matching workspace {_ws_schema.name}")
        logger.debug(
            f"Mapping {_ws_schema.name} to dir: {ws_dir_path} and config: {ws_config_file_path}"
        )
        self._add_or_update_ws_data(
            ws_name=_ws_schema.name,
            ws_schema=_ws_schema,
            ws_dir_path=ws_dir_path,
            ws_config_file_path=ws_config_file_path,
            refresh_data=True,
        )
        self.save_config()
        return self._ws_data_map.get(_ws_schema.name, None)

    def validate_workspace(
        self, ws_name: str
    ) -> Tuple[bool, Optional[Set[WorkspaceSetupActions]]]:
        """Validates a workspace and returns a tuple of [validation_status, pending_setup_actions]
        Returns:
            (False, None): If PhiWsData is not valid
            (True, None): If Validation is successful and everything is properly setup
            (True, set(WorkspaceSetupActions)): If Validation is successful but user has pending setup actions
            (False, set(WorkspaceSetupActions)): If Validation is unsuccessful and user has pending setup actions
        """

        # Validate the ws has a valid entry
        if ws_name is None or ws_name not in self._ws_data_map:
            return False, None
        logger.debug(f"Validating workspace: {ws_name}")

        ws_data: PhiWsData = self._ws_data_map[ws_name]

        # If ws_config is missing add a pending action
        if ws_data.ws_config is None:
            ws_data.pending_actions.add(WorkspaceSetupActions.WS_CONFIG_IS_AVL)
        else:
            ws_data.pending_actions.discard(WorkspaceSetupActions.WS_CONFIG_IS_AVL)

        # If ws_schema is missing add a pending action
        if ws_data.ws_schema is None:
            ws_data.pending_actions.add(WorkspaceSetupActions.WS_IS_AUTHENTICATED)
        else:
            ws_data.pending_actions.discard(WorkspaceSetupActions.WS_IS_AUTHENTICATED)

        # If git_url is missing add a pending action
        if ws_data.ws_schema is None or ws_data.ws_schema.git_url is None:
            ws_data.pending_actions.add(WorkspaceSetupActions.GIT_REMOTE_ORIGIN_IS_AVL)
        else:
            ws_data.pending_actions.discard(
                WorkspaceSetupActions.GIT_REMOTE_ORIGIN_IS_AVL
            )

        # logger.debug(f"Required Actions for this workspace: {ws_data.required_actions}")
        # logger.debug(f"Pending Actions for this workspace: {ws_data.pending_actions}")

        # Check how many required_actions are pending
        if len(ws_data.required_actions.intersection(ws_data.pending_actions)) > 0:
            return False, ws_data.pending_actions

        return True, ws_data.pending_actions

    def delete_ws(self, ws_dir_path: Path, delete_ws_dir: bool = False) -> bool:
        """Handles Deleting a workspace from the PhiConf using ws_dir_path"""

        ws_data: Optional[PhiWsData] = None
        if ws_dir_path in self._path_to_ws_data_map:
            ws_data = self._path_to_ws_data_map.pop(ws_dir_path, None)
        # Return False if a ws using this path does not exist
        if ws_data is None:
            print_error(f"Could not locate workspace on path {str(ws_dir_path)}")
            return False

        print_info("")
        print_info(f"Deleting workspace {ws_data.ws_name}")
        print_info("")
        # Check if we're deleting the primary workspace, if yes, unset the primary ws
        if (
            self._active_ws_name is not None
            and ws_data.ws_name is not None
            and self._active_ws_name == ws_data.ws_name
        ):
            print_info(f"Removing {ws_data.ws_name} as the primary workspace")
            self._active_ws_name = None

        # Then delete the workspace data
        logger.debug(f"Removing WorkspaceSchema Data")
        deleted_ws_data: Optional[PhiWsData] = self._ws_data_map.pop(
            ws_data.ws_name, None
        )

        ws_dir_path_deleted: bool = False
        if delete_ws_dir and ws_dir_path:
            print_info(f"Deleting {str(ws_dir_path)}")
            ws_dir_path_deleted = delete_from_fs(ws_dir_path)

        # Save the config after deleting workspace
        self.save_config()

        if deleted_ws_data is not None:
            if delete_ws_dir:
                return ws_dir_path_deleted
            return True
        return False

    ######################################################
    ## Get Workspace Data
    ######################################################

    ## Workspace Name
    def get_ws_name_by_path(self, ws_dir_path: Path) -> Optional[str]:
        if ws_dir_path in self._path_to_ws_data_map:
            return self._path_to_ws_data_map[ws_dir_path].ws_name
        return None

    ## Workspace Schema
    def get_ws_schema_by_name(self, ws_name: str) -> Optional[WorkspaceSchema]:
        if ws_name in self._ws_data_map:
            return self._ws_data_map[ws_name].ws_schema
        return None

    def get_ws_schema_by_path(self, ws_dir_path: Path) -> Optional[WorkspaceSchema]:
        if ws_dir_path in self._path_to_ws_data_map:
            return self._path_to_ws_data_map[ws_dir_path].ws_schema
        return None

    ## Workspace Directory
    def get_ws_dir_path_by_name(self, ws_name: str) -> Optional[Path]:
        if ws_name in self._ws_data_map:
            return self._ws_data_map[ws_name].ws_dir_path
        return None

    ## Workspace Config File Path
    def get_ws_config_file_path_by_name(self, ws_name: str) -> Optional[Path]:
        if ws_name in self._ws_data_map:
            return self._ws_data_map[ws_name].ws_config_file_path
        return None

    ## Workspace Pending Actions
    def get_ws_pending_actions_by_name(
        self, ws_name: str
    ) -> Optional[Set[WorkspaceSetupActions]]:
        if ws_name in self._ws_data_map:
            return self._ws_data_map[ws_name].pending_actions
        return None

    ## Workspace Data
    def get_ws_data_by_name(
        self, ws_name: str, refresh: bool = False
    ) -> Optional[PhiWsData]:
        if ws_name in self._ws_data_map:
            # if refresh or self._ws_data_map[ws_name].ws_config is None:
            if refresh:
                self.refresh_ws_config(ws_name)
            return self._ws_data_map[ws_name]
        return None

    def get_ws_data_by_path(self, ws_dir_path: Path) -> Optional[PhiWsData]:
        if ws_dir_path in self._path_to_ws_data_map:
            return self._path_to_ws_data_map[ws_dir_path]
        return None

    def refresh_ws_config(self, ws_name: str) -> bool:
        """Refresh the workspace config for a given workspace name"""

        logger.debug(f"++**++ Refreshing WorkspaceConfig for {ws_name}")
        self._add_or_update_ws_data(ws_name=ws_name, refresh_data=True)
        # we check that refresh was successful to avoid saving bad data
        # TODO: add checks to ensure refresh success.
        refresh_success = True
        if refresh_success:
            logger.debug(f"++**++ Refresh success")
            self.save_config()
        return refresh_success

    # ## Workspace Pak8Conf
    # def get_ws_pak8_conf_by_name(
    #     self, ws_name: str, refresh: bool = False, add_kubeconfig: bool = False
    # ) -> Optional[Pak8Conf]:
    #     if ws_name in self._ws_data_map:
    #         logger.debug(f"Getting Pak8Conf for {ws_name}")
    #         _ws_pak8_conf = self._ws_data_map[ws_name].ws_pak8_conf
    #         if refresh or _ws_pak8_conf is None:
    #             logger.debug(f"Refreshing Pak8Conf for {ws_name}")
    #             self.refresh_ws_config(ws_name)
    #         if add_kubeconfig:
    #             # Check if a kubeconfig is available, if yes, update the Pak8Conf
    #             ws_k8s_data: Optional[PhiK8sData] = self._ws_data_map[
    #                 ws_name
    #             ].ws_k8s_data
    #             if ws_k8s_data:
    #                 logger.debug(f"Adding Kubeconfig to Pak8Conf for {ws_name}")
    #                 kconf_resource = ws_k8s_data.get_kubeconfig()
    #                 if kconf_resource:
    #                     # TODO: convert this into a function
    #                     # self._ws_data_map[
    #                     #     ws_name
    #                     # ].ws_pak8_conf.k8s.kubeconfig_resource = kconf_resource
    #                     self.save_config()
    #         return self._ws_data_map[ws_name].ws_pak8_conf
    #     return None

    # def get_ws_pak8_conf_by_path(
    #     self, ws_dir_path: Path, refresh: bool = False
    # ) -> Optional[Pak8Conf]:
    #     if ws_dir_path in self._path_to_ws_data_map:
    #         if refresh:
    #             ws_data: PhiWsData = self._path_to_ws_data_map[ws_dir_path]
    #             self.refresh_ws_config(ws_data.ws_name)
    #         return self._path_to_ws_data_map[ws_dir_path].ws_pak8_conf
    #     return None

    ######################################################
    ## GCP
    ######################################################

    # def update_ws_gcp_data(
    #     self,
    #     ws_name: str,
    #     gcp_project_id: Optional[str] = None,
    #     gcp_project: Optional[GCPProjectSchema] = None,
    #     gke_cluster: Optional[GKEClusterSchema] = None,
    #     gcloud_default_creds_avl: Optional[bool] = None,
    #     gcp_svc_account: Optional[Dict[str, Any]] = None,
    #     gcp_svc_account_key: Optional[Dict[str, Any]] = None,
    # ) -> Optional[PhiGcpData]:
    #     """This function creates/updates the PhiGcpData for ws_name.
    #     When creating the PhiGcpData for the first time, the gcp_project_id must be provided.
    #     """
    #     if ws_name not in self._ws_data_map:
    #         return None
    #
    #     ws_data = self._ws_data_map[ws_name]
    #     ws_gcp_data: Optional[PhiGcpData] = ws_data.ws_gcp_data
    #     # If this is the first time we are creating the PhiGcpData for this workspace
    #     if ws_gcp_data is None:
    #         logger.debug(f"Creating PhiGcpData for {ws_name}")
    #         if gcp_project_id is None:
    #             logger.error(
    #                 "gcp_project_id must be provided when creating PhiGcpData for the first time"
    #             )
    #             return None
    #         ws_gcp_data = PhiGcpData(
    #             gcp_project_id=gcp_project_id,
    #             gcp_project=gcp_project,
    #             gke_cluster=gke_cluster,
    #             gcloud_default_creds_avl=gcloud_default_creds_avl
    #             if gcloud_default_creds_avl
    #             else False,
    #             gcp_svc_account=gcp_svc_account,
    #             gcp_svc_account_key=gcp_svc_account_key,
    #         )
    #         self._ws_data_map[ws_name].ws_gcp_data = ws_gcp_data
    #         self.save_config()
    #         return ws_gcp_data
    #
    #     logger.debug(f"Updating PhiGcpData for {ws_name}")
    #     if gcp_project_id is not None:
    #         if gcp_project_id != ws_gcp_data.gcp_project_id:
    #             print_warning(
    #                 "Updating GCP Project Id from {} to {}".format(
    #                     ws_gcp_data.gcp_project_id, gcp_project_id
    #                 )
    #             )
    #         ws_gcp_data.gcp_project_id = gcp_project_id
    #     if gcp_project is not None:
    #         ws_gcp_data.gcp_project = gcp_project
    #     if gke_cluster is not None:
    #         ws_gcp_data.gke_cluster = gke_cluster
    #     if gcloud_default_creds_avl is not None:
    #         ws_gcp_data.gcloud_default_creds_avl = gcloud_default_creds_avl
    #     if gcp_svc_account is not None:
    #         ws_gcp_data.gcp_svc_account = gcp_svc_account
    #     if gcp_svc_account_key is not None:
    #         ws_gcp_data.gcp_svc_account_key = gcp_svc_account_key
    #         ws_data.pending_actions = ws_data.pending_actions - {
    #             WorkspaceSetupActions.GCP_SVC_ACCOUNT_IS_AVL
    #         }
    #         logger.debug(f"Pending Actions: {ws_data.pending_actions}")
    #
    #     self.save_config()
    #     return ws_gcp_data
    #
    # def get_ws_gcp_data_by_name(self, ws_name: str) -> Optional[PhiGcpData]:
    #     if ws_name in self._ws_data_map:
    #         return self._ws_data_map[ws_name].ws_gcp_data
    #     return None

    # def get_gcp_project_schema_by_ws_name(
    #     self, ws_name: str
    # ) -> Optional[GCPProjectSchema]:
    #     if ws_name in self._ws_data_map:
    #         ws_gcp_data: Optional[PhiGcpData] = self._ws_data_map[ws_name].ws_gcp_data
    #         if ws_gcp_data:
    #             return ws_gcp_data.gcp_project
    #     return None

    # def get_gke_cluster_by_ws_name(self, ws_name: str) -> Optional[GKEClusterSchema]:
    #     if ws_name in self._ws_data_map:
    #         ws_gcp_data: Optional[PhiGcpData] = self._ws_data_map[ws_name].ws_gcp_data
    #         if ws_gcp_data:
    #             return ws_gcp_data.gke_cluster
    #     return None

    ######################################################
    ## ReleaseSchema Data
    ######################################################

    # def get_ws_releases_by_name(self, ws_name: str) -> Optional[WsReleases]:
    #     if ws_name in self._ws_data_map:
    #         return self._ws_data_map[ws_name].ws_releases
    #     return None
    #
    # def add_release_for_ws(self, ws_name: str, release: ReleaseSchema) -> None:
    #     if (ws_name in self._ws_data_map) and release:
    #         logger.debug(f"Adding release for ws {ws_name}")
    #         self._ws_data_map[ws_name].ws_releases.add_release(release)
    #     self.save_config()
    #
    # def get_latest_release_for_ws(self, ws_name: str) -> Optional[ReleaseSchema]:
    #     if ws_name in self._ws_data_map:
    #         return self._ws_data_map[ws_name].ws_releases.get_latest_release()
    #     return None

    ######################################################
    ## K8s functions
    ######################################################

    # def get_k8s_resources_dir_path_by_ws_name(self, ws_name: str) -> Optional[Path]:
    #     ws_dir_path: Optional[Path] = None
    #     if ws_name and ws_name in self._ws_data_map:
    #         ws_dir_path = self._ws_data_map[ws_name].ws_dir_path
    #     if ws_dir_path:
    #         return ws_dir_path.joinpath("phi").joinpath("prd")
    #     return None
    #
    # def get_ws_k8s_data_by_name(self, ws_name: str) -> Optional[PhiK8sData]:
    #     if ws_name in self._ws_data_map:
    #         return self._ws_data_map[ws_name].ws_k8s_data
    #     return None
    #
    # def update_ws_k8s_data(
    #     self,
    #     ws_name: str,
    #     kubeconfig_resource: Optional[Kubeconfig] = None,
    #     kubeconfig_path: Optional[Path] = None,
    # ) -> Optional[PhiK8sData]:
    #     """This function creates/updates the PhiK8sData for ws_name.
    #     When creating the PhiK8sData for the first time, the kubeconfig_resource must be provided.
    #     """
    #     if ws_name not in self._ws_data_map:
    #         return None
    #
    #     ws_data = self._ws_data_map[ws_name]
    #     ws_k8s_data: Optional[PhiK8sData] = ws_data.ws_k8s_data
    #     # If this is the first time we are creating the PhiK8sData for this workspace
    #     if ws_k8s_data is None:
    #         logger.debug(f"Creating PhiK8sData for {ws_name}")
    #         if kubeconfig_resource is None:
    #             logger.error(
    #                 "kubeconfig_resource must be provided when creating PhiK8sData for the first time"
    #             )
    #             return None
    #         ws_k8s_data = PhiK8sData.create_using_kubeconfig_resource(
    #             ws_name=ws_name, kconf_resource=kubeconfig_resource
    #         )
    #         self._ws_data_map[ws_name].ws_k8s_data = ws_k8s_data
    #         self.save_config()
    #         return ws_k8s_data
    #
    #     logger.debug(f"Updating PhiK8sData for {ws_name}")
    #     if kubeconfig_resource is not None:
    #         ws_k8s_data.update_kubeconfig_resource(kconf_resource=kubeconfig_resource)
    #     self.save_config()
    #     return ws_k8s_data

    ######################################################
    ## PhiConf functions
    ######################################################

    def save_config(self):
        # logger.debug(f"Saving config to {str(PHI_CONF_PATH)}")
        pickle_object_to_file(self, PHI_CONF_PATH)

    @classmethod
    def get_saved_conf(cls):
        # logger.debug(f"Reading phidata conf at {PHI_CONF_PATH}")
        if PHI_CONF_PATH.exists():
            # logger.debug(f"{PHI_CONF_PATH} exists")
            if PHI_CONF_PATH.is_file():
                return unpickle_object_from_file(
                    file_path=PHI_CONF_PATH, verify_class=cls
                )
            elif PHI_CONF_PATH.is_dir():
                logger.debug(f"{PHI_CONF_PATH} is a directory, deleting and exiting")
                delete_from_fs(PHI_CONF_PATH)
        return None

    def print_to_cli(self):
        print_heading("Phidata Config\n")
        if self.user:
            print_info(f"User: {self.user.email}")
        if self.active_ws_name:
            print_info(f"Primary workspace: {self.active_ws_name}")
        if len(self._ws_data_map) > 0:
            print_subheading("\nAvailable workspaces")
            for k, v in self._ws_data_map.items():
                print_info(f"name: {v.ws_name}")
                print_info(f"dir_path: {v.ws_dir_path}")
                print_info(f"config_file_path: {v.ws_config_file_path}")
                print_horizontal_line()
