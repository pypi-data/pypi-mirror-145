# Copyright: (c) 2022, Swimlane <info@swimlane.com>
# MIT License (see LICENSE or https://opensource.org/licenses/MIT)

from ..base import Base
from ..models import Workspace
from ..utils.exceptions import (
    AddComponentError,
    UpdateComponentError
)

class Workspaces(Base):

    """Used to sync workspaces from a source instance to a destination instance of Swimlane
    """

    def sync_workspace(self, workspace: Workspace):
        if not self._is_in_include_exclude_lists(workspace.name, 'workspaces'):
            self.__logger.info(f"Processing workspace '{workspace.name}'")
            dest_workspace = self.destination_instance.get_workspace(workspace.id)
            if not dest_workspace:
                self.__logger.info(f"Adding workspace '{workspace.name}' to destination.")
                dest_workspace = self.destination_instance.add_workspace(workspace)
                if not dest_workspace:
                    raise AddComponentError(model=workspace, name=workspace.name)
                self.__logger.info(f"Successfully added workspace '{workspace.name}' to destination.")
            else:
                if workspace.uid == dest_workspace.uid:
                    if workspace.version == dest_workspace.version:
                        self.__logger.info(f"Workspace '{workspace.name}' already exists on destination and is the same version ({dest_workspace.version}). Skipping...")
                    else:
                        self.__logger.info(f"Workspace '{workspace.name}' already exists on destination and is a different version ({dest_workspace.version}). Updating...")
                        from .applications import Applications
                        for application_id in workspace.applications:
                            Applications().sync_application(application_id=application_id)
                        resp = self.destination_instance.update_workspace(workspace_id=dest_workspace.id, workspace=workspace)
                        if not resp:
                            raise UpdateComponentError(model=workspace, name=workspace.name)
                        self.__logger.info(f"Successfully updated workspace '{workspace.name}' on destination.")

    def sync(self):
        """This method is used to sync all workspaces from a source instance to a destination instance
        """
        self.__logger.info(f"Starting to sync workspaces from '{self.source_host}' to '{self.dest_host}'")
        for workspace in self.source_instance.get_workspaces():
            self.sync_workspace(workspace=workspace)
