import os
import ansible_runner

class RolesInstaller:
    """
    A python client for interacting with ansible galaxy
    Currently only used to install lists of roles
    inputs:
      roles_directory (optional): path to where roles should be installed. Defaults to ./roles
    """
    def __init__(self, roles_directory= './roles'):
        self.roles_directory = roles_directory

    def install_roles(self, roles_list):
        """
        Inputs:
        roles_list - (List String) a list of role names in the form ROLE_NAME or ROLE_NAME:VERSION
        """
        for role in roles_list:
            parsed_role = self.parse_role(role)
            self.install_role(parsed_role)

    def install_role(self,role):
        args = ['role','install','-p',self.roles_directory,role.get('name')+','+role.get('version','')]
        ansible_runner.interface.run_command('ansible-galaxy',cmdline_args=args)

    def role_installed(self,role):
        foldername = role.get('name')
        return os.path.isdir(os.getcwd() + '/' + self.roles_directory + '/' + foldername)

    @classmethod
    def parse_role(cls, role):
        parsed_role = {}
        if ':' not in role:
            parsed_role['name'] = role
        else:
            [name, version] = role.split(':')
            parsed_role['name'] = name
            parsed_role['version'] = version
        return parsed_role
