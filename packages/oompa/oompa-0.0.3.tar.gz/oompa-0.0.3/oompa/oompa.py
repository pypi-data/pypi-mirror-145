import argparse
import docker

from oompa.ansible_clients.ansible_runner import AnsibleRunner
from oompa.ansible_clients.roles_installer import RolesInstaller
from oompa.docker_clients.container_manager import ContainerManager
from oompa.file_parser.file_parser import FileParser
from oompa.utils.keystore import Keystore

def main():
    keystore = Keystore()
    container = ContainerManager(client=docker.from_env())
    installer = RolesInstaller()
    runner = AnsibleRunner()
    file_parser = FileParser()
    keystore.create_private_key_file()
    keystore.create_public_key_file()

    parser = argparse.ArgumentParser(
        description='A tool to replace messy Dockerfiles with type-safe configuration'
        )
    args = parser.add_argument(
        '-f',
        '--file',
        metavar='string',
        type=str,
        help="Name of the Dhall builder file (Default is 'PATH/builder.dhall')")
    args = parser.parse_args()

    file_parser.set_path('.')
    if args.file:
        file_parser.set_file(args.file)
    config = file_parser.parse_file()

    container.image_pull(config['srcImage'])
    container.start_container()
    container.prepare_container()
    container.add_publickey(keystore.public_key)
    port = container.get_port()

    installer.install_roles(config['rolesList'])

    # Require a different format for roles_list input for runner.execute_playbook
    playbook_roles = list(map(lambda role: installer.parse_role(role), config['rolesList']))
    runner.update_port(port)
    runner.load_roles(playbook_roles)
    runner.execute_playbook( private_key = keystore.private_key.decode())

    if ':' in config['destImage']:
        [DEST_IMAGE, DEST_TAG] = config['destImage'].split(':')
    else:
        DEST_IMAGE = config['destImage']
        DEST_TAG = 'latest'

    container.save(DEST_IMAGE, DEST_TAG)

if __name__ == '__main__':
    main()