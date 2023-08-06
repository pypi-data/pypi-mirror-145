import os

class ContainerManager:
    """
    Manages all container operations for oompa
    """
    def __init__(self, client):
        self.client = client
        self.name = None
        self.image = None

    def image_pull(self, image):
        print(f"Pulling image {image}")
        try:
            self.client.images.pull(image)
            self.image = image
        except RuntimeError as error:
            raise RuntimeError(f"Not able to pull image {image}") from error

    def start_container(self, name=None):
        try:
            container = self.client.containers.create(
                self.image,
                detach=True,
                tty=True,
                ports={'22/tcp': None},
                name=name,
                entrypoint='sh')
            container.start()
            self.name = container.name
        except RuntimeError as error:
            raise RuntimeError(f"Not able to start container from image {self.image}") from error

    def prepare_container(self):
        print("Preparing container for Ansible execution...")
        container = self.client.containers.get(self.name)
        boostrap_path = os.path.join(os.path.dirname(__file__), '../utils/oompa-bootstrap.sh.tar')
        with open(boostrap_path, 'rb') as bootstrap_file:
            data = bootstrap_file.read()
            container.put_archive("/tmp", data)
            container.exec_run('/tmp/oompa-bootstrap.sh')

    def add_publickey(self, public_key):
        container = self.client.containers.get(self.name)
        container.exec_run('mkdir /root/.ssh')
        container.exec_run('chmod 700 /root/.ssh')
        container.exec_run("sh -c 'echo " + public_key.decode('ascii') + " > /root/.ssh/authorized_keys'")
        container.exec_run('chmod 600 /root/.ssh/authorized_keys')

    def get_port(self):
        container = self.client.containers.get(self.name)
        return container.ports.get('22/tcp')[0].get('HostPort')

    def save(self, repository, tag):
        container = self.client.containers.get(self.name)
        container.commit(repository=repository, tag=tag)
        print(f"Successfully created new image {repository}:{tag}")
