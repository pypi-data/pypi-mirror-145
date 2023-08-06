from typing import Dict

from phi.workspace.ws_enums import WorkspaceStarterTemplate

template_to_repo_map: Dict[WorkspaceStarterTemplate, str] = {
    WorkspaceStarterTemplate.docker: "https://github.com/phidata-public/phidata_starter_docker.git",
    WorkspaceStarterTemplate.aws: "https://github.com/phidata-public/phidata_starter_aws.git",
}
