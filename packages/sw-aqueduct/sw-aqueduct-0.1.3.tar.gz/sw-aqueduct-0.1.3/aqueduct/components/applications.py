# Copyright: (c) 2022, Swimlane <info@swimlane.com>
# MIT License (see LICENSE or https://opensource.org/licenses/MIT)

from collections import OrderedDict
from ..base import Base
from ..utils.exceptions import (
    AddComponentError,
    GetComponentError
)
from .workspaces import Workspaces
from .workflows import Workflows


class Applications(Base):

    """Used to sync applications from a source instance to a destination instance of Swimlane
    """

    def __filter_out_field_from_layout(self, layout, field):
        if isinstance(layout, list):
            return [ self.__filter_out_field_from_layout(element, field) for element in layout if not element.get('fieldId') or element.get('fieldId') and element['fieldId'] != field['id'] ]
        elif isinstance(layout, dict):
            return { key: self.__filter_out_field_from_layout(value, field) for key, value in layout.items() }
        else:
            return layout

    def __add_fields(self, source: dict, destination: dict):
        self.__logger.info(f"Checking application '{source['name']}' application for missing fields.")
        update_layout = False
        for sfield in source['fields']:
            if sfield not in destination['fields']:
                update_layout = True
                self.__logger.info(f"Field '{sfield['name']}' not in destination application.")
                destination['fields'].append(sfield)
                self.__logger.info(f"Successfully added '{sfield['name']}' to destination application")
        if update_layout:
            destination['layout'] = source['layout']

    def __remove_fields(self, source: dict, destination: dict):
        self.__logger.info(f"Checking application '{source['name']}' application for fields to remove.")
        for dfield in destination['fields']:
            if dfield not in source['fields']:
                self.__logger.info(f"Removing field '{dfield['name']}' from '{destination['name']}' application layout.")
                destination['layout'] = self.__filter_out_field_from_layout(destination['layout'], dfield)

    def _remove_tracking_field(self, application: dict):
        """This method removes an applications tracking field since
        Swimlane automatically generates this for every new application.

        Args:
            application (dict): A Swimlane application to remove the tracking field from
        """
        for field in application.get('fields'):
            if field.get('fieldType') and field['fieldType'].lower() == 'tracking':
                application['fields'].remove(field)

    def get_reference_app_order(self):
        """This method creates an order of applications to be added or updated on a destination
        instance based on most to least reference relationships. For example, a source application
        that references 5 applications will be before an application which has 3 references to applications.

        Returns:
            dict: An reference application ordered (sorted) application dictionary
        """
        reference_dict = {}
        for application in self.source_instance.get_applications():
            application_ = self.source_instance.get_application(application_id=application['id'])
            if application_['id'] not in reference_dict:
                reference_dict[application_['id']] = []
            for field in application_['fields']:
                if field.get('$type') and field['$type'] == "Core.Models.Fields.Reference.ReferenceField, Core":
                    reference_dict[application_['id']].append(field['targetId'])

        return_dict = OrderedDict()
        for item in sorted(reference_dict, key=lambda k: len(reference_dict[k]), reverse=True):
            return_dict[item] = reference_dict[item]
        return return_dict

    def sync_application(self, application_id: str):
        """This method syncs a single application from a source instance to a destination instance.

        Once an application_id on a source instance is provided we retreive this application JSON.
        Next we remove the tracking_field from the application since Swimlane automatically generates
        a unique value for this field.

        If workspaces are defined in the application and do not currently exist will attempt to create
        or update them using the Workspaces class.

        If the source application does not exist on the destination we will create it with the same IDs for 
            1. application
            2. fields
            3. layout
            4. etc.
        
        By doing this, syncing of applications (and their IDs) is much easier.

        If the application exists we proceed to remove specific fields that are not needed.

        Next we check for fields which have been added to the source application but do not 
        exist on the destination instance. If fields are found we add them to the destination 
        object.

        Next we check to see if the destination has fields which are not defined in the source instance.
        If fields are found, we then remove them from the layout view of the source application. This equates
        to moving them to the "hidden" field section within the application builder so they can still be retrieved
        and reorganized as needed.

        Finally we update the application on the destination instance.

        After updating the application we then check to ensure that the workflow of that application is up to date
        and accurate.

        Args:
            application_id (str): A source application ID.
        """
        application_ = self.source_instance.get_application(application_id=application_id)
        if not application_:
            raise GetComponentError(name='application', id=application_id)
        if not self._is_in_include_exclude_lists(application_['name'], 'applications'):
            self.__logger.info(f"Processing application '{application_['name']}'")
            self._remove_tracking_field(application_)
            if application_.get('workspaces') and application_['workspaces']:
                for workspace in application_['workspaces']:
                    workspace_ = self.source_instance.get_workspace(workspace_id=workspace)
                    if not workspace_:
                        raise GetComponentError(name='workspace', id=workspace)
                    if workspace_ and not self.destination_instance.get_workspace(workspace_id=workspace):
                        Workspaces().sync_workspace(workspace=workspace_)

            dest_application = self.destination_instance.get_application(application_['id'])
            if not dest_application:
                self.__logger.info(f"Adding application '{application_['name']}' to destination.")
                application_.pop('trackingFieldId')
                dest_application = self.destination_instance.add_application(application=application_)
                if not dest_application:
                    raise AddComponentError(application_)
                self.__logger.info(f"Successfully added application '{application_['name']}' to destination.")
            else:
                self.__logger.info(f"Application '{application_['name']}' already exists on destination.")
                for item in ['$type', 'createdByUser', 'modifiedByUser', 'permissions']:
                    application_.pop(item)
                    dest_application.pop(item)
                self._remove_tracking_field(dest_application)
                self.__add_fields(application_, dest_application)
                self.__remove_fields(application_, dest_application)
                self.__logger.info(f"Updating application '{dest_application['name']}' on destination.")
                self.destination_instance.update_application(dest_application)
                self.__logger.info(f"Successfully updated application '{dest_application['name']}' on destination.")

            self.__logger.info(f"Checking for changes in workflow for application '{dest_application['name']}'")
            Workflows().sync_workflow(application_name=application_['name'])
        else:
            self.__logger.info(f"Skipping application '{application_['name']}' since it is excluded.")

    def sync(self):
        """This method will sync all applications on a source instance with a destination instance.
        """
        self.__logger.info(f"Starting to sync 'Applications' from '{self.source_host}' to '{self.dest_host}'")
        for application_id, values in self.get_reference_app_order().items():
            self.sync_application(application_id=application_id)
