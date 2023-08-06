# Copyright: (c) 2022, Swimlane <info@swimlane.com>
# MIT License (see LICENSE or https://opensource.org/licenses/MIT)

from .utils.logger import LoggingBase


class Base(metaclass=LoggingBase):

    source_instance = None
    destination_instance = None
    remove_keys = ['createdDate', 'modifiedDate', 'createdByUser', 'modifiedByUser']
    group_exclusions = ['Everyone']
    role_exclusions = ['Administrator']
    source_host = None
    dest_host = None
    offline = False
    update_reports = False
    update_dashboards = False
    continue_on_error = False
    include = None
    exclude = None

    def log_exception(self, val, level='error'):
        getattr(self.__logger, level)(val)

    def _is_in_include_exclude_lists(self, name, type):
        if self.exclude.get(type) and name in self.exclude[type]:
            self.__logger.info(f"{type.capitalize()} '{name}' in exclude list. Skipping...")
            return True
        if self.include.get(type) and name not in self.include[type]:
            self.__logger.info(f"{type.capitalize()} '{name}' is not in include list. Skipping...")
            return True
        return False

    def scrub(self, obj, bad_key="$type"):
        """Used to remove a specific provided key from a dictionary
        that may contain both nested dictionaries and lists.
        
        This method is recurisve.

        Args:
            obj (dict): A dictionary or list to remove keys from.
            bad_key (str, optional): The bad key to remove from the provided dict or list. Defaults to "$type".
        """
        if isinstance(obj, dict):
            for key in list(obj.keys()):
                if key == bad_key:
                    del obj[key]
                else:
                    self.scrub(obj[key], bad_key)
        elif isinstance(obj, list):
            for i in reversed(range(len(obj))):
                if obj[i] == bad_key:
                    del obj[i]
                else:
                    self.scrub(obj[i], bad_key)
        else:
            pass
