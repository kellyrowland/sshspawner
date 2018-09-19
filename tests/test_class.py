import pytest
from jupyterhub.objects import Hub
from jupyterhub import orm
from sshspawner.sshspawner import SSHSpawner

class TestSSHSpawner:
    @classmethod
    def setup_class(cls):
        cls.SSHSpawner = SSHSpawner()
        cls.SSHSpawner.hub = Hub()
        cls.SSHSpawner.hub.public_host = "testhost"
        orm_user = orm.User(name="testuser")
        cls.SSHSpawner.user = orm_user
        cls.SSHSpawner.user.url = "http://localhost"
        orm_server = orm.Server()
        cls.SSHSpawner.user.server = orm_server
        cls.SSHSpawner.user.server.cookie_name = "testcookie"

    def test_remote(self):
        port = self.SSHSpawner.remote_port
        host = self.SSHSpawner.remote_host
        assert(port == "22")
        assert(host == "remote_host")

    def test_env(self):
        env = self.SSHSpawner.user_env()
        assert(env['JPY_USER'] == "testuser")
        assert(env['JPY_COOKIE_NAME'] == "testcookie")
        assert(env['PATH'] == "/usr/bin:/bin:/usr/sbin:/sbin:/usr/local/bin")
