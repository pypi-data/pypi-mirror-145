import os
import ansible_runner


class AnsibleRunner:
    """
    A python client for running Ansible playbooks against specified hosts
    inputs:
      roles_directory (optional): path to where roles are installed. Defaults to ./roles
    """
    def __init__(self, roles_directory='./roles'):
        if os.path.isabs(roles_directory):
            roles_path = roles_directory
        else:
            roles_path = os.getcwd()+ '/' + roles_directory
        self.roles_path = roles_path
        self.play_list = []
        self.port = 0

    def update_port(self, port):
        self.port = port

    def add_play(self, play):
        self.play_list += play

    def load_roles(self, roles_list):
        role_to_task = lambda role: {
            'hosts': 'localhost',
            'tasks': [
                {
                    'name': 'include role ' + role['name'],
                    'include_role': {
                        'name': role['name']
                    }
                }
            ]}
        roles_play = list(map(role_to_task, roles_list))
        self.play_list += roles_play

    def execute_playbook(self, private_key = None, connection = 'ssh'):
        extravars = {'ansible_user': 'root', 'ansible_connection': connection}
        inventory = {'all': {'hosts': {'localhost': {}}, 'vars': {'ansible_port': self.port}}}
        ansible_runner.interface.run(
            playbook=self.play_list,
            roles_path=self.roles_path,
            ssh_key=private_key,
            extravars=extravars,
            inventory=inventory
        )
