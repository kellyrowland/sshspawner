import pytest
from sshspawner.sshspawner import SSHSpawner

class TestSSHSpawner:
    @classmethod
    def setup_class(cls):
        cls.SSHSpawner = SSHSpawner()

    def test_remote(self):
        port = self.SSHSpawner.remote_port
        host = self.SSHSpawner.remote_host
        assert(port == "22")
        assert(host == "remote_host")

