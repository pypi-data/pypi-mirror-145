# Copyright: (c) 2022, Swimlane <info@swimlane.com>
# MIT License (see LICENSE or https://opensource.org/licenses/MIT)

from ..base import Base
from ..utils.exceptions import (
    GetComponentError,
    UpdateComponentError
)


class Workflows(Base):

    """Used to sync workflows from a source instance to a destination instance of Swimlane
    """

    def sync_workflow(self, application_name: str):
        """This methods syncs a single applications workflow from a source Swimlane instance to 
        a destination instance.

        If an application_name is in our include or exclude filters we will either ignore or
        process the workflow updates for that application.

        Once an application_name is provided we retrieve the workflow for that application from 
        our workflow_dict. Additionally we retrieve the destination workflow for the provided
        application.

        We create a temporary object that compares the stages of a source workflow to a destination
        workflow. If they are exactly the same we skip updating the workflow. If they are not, we 
        copy the source workflow to the destination and update it to reflect the new workflow ID.

        Finally we update the destination workflow with our changes.

        Args:
            application_name (str): The name of an application to check and update workflow if applicable.
        """
        if not self._is_in_include_exclude_lists(application_name, 'applications'):
            workflow = self.source_instance.workflow_dict.get(application_name)
            if workflow:
                self.__logger.info(f"Processing workflow '{workflow['id']}' for application '{application_name}' ({workflow['applicationId']}).")
                dest_workflow = self.destination_instance.get_workflow(application_id=workflow['applicationId'])
                if not dest_workflow:
                    raise GetComponentError(type='Workflow', name=application_name)
                # Checking if all items under stages in the destination are the same the source workflow
                # To do this we are creating a temporary variable and updating the root stages to include
                # the same parentId value as the source location. This is just to test the conditional below.
                temp_stages = dest_workflow['stages']
                for item in temp_stages:
                    if hasattr(item, 'parentId'):
                        item['parentId'] = workflow['id']

                if workflow['stages'] != temp_stages:
                    action_string = 'Updating' if dest_workflow['stages'] else 'Adding' 
                    self.__logger.info(f"{action_string} workflow for application '{application_name}' ({self.source_instance.application_dict[application_name]['id']}).")
                    
                    # We are setting the source stages of workflow to the destination workflow stages
                    # Once we do this we need to update the parentId value to be the existing workflow ID value
                    dest_workflow['stages'] = workflow['stages']
                    for item in dest_workflow['stages']:
                        if hasattr(item, 'parentId') and item['parentId'] == workflow['id']:
                            item['parentId'] = dest_workflow['id']

                    resp = self.destination_instance.update_workflow(workflow=dest_workflow)
                    if not resp:
                        raise UpdateComponentError(model=workflow, name=workflow['name'])
                    self.__logger.info(f"Successfully updated workflow for application '{application_name}'.")
                else:
                    self.__logger.info(f"No Workflow '{workflow['id']}' updates found for application '{application_name}'. Skipping...")
            else:
                raise GetComponentError(type='Workflow', name=application_name)

    def sync(self):
        """This method is used to sync all workflows from a source instance to a destination instance
        """
        raise NotImplementedError("General workflow syncing is currently not implemented.")
