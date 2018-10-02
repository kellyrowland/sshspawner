import asyncio
import pytest
from jupyterhub.objects import Hub
from sshspawner.sshspawner import SSHSpawner
import mockssh
from pytest import fixture, yield_fixture
from jupyterhub.objects import Hub
from sshspawner.sshspawner import SSHSpawner

@yield_fixture()
def server():
    users = {
                "testuser": "tests/sample-user-key"
            }
    socket = 80
    with mockssh.Server(users) as s:
        yield s

class TestSSHSpawner:
    @fixture()
    def spawner(self,server):
        s = server
        self.SSHSpawner = SSHSpawner()
        SSHSpawner.hub = Hub()
        for uid in s.users:
            SSHSpawner.user.name = uid

    def test_server(self,spawner):
        assert(SSHSpawner.user.name == "testuser")
        # for uid in server.users:
        #     with server.client(uid) as c:
        #         port = SSHSpawner.remote_port
        #         # loop = asyncio.get_event_loop()
        #         # random_port = loop.run_until_complete(self.SSHSpawner.remote_random_port())
        #         # assert(port == 80)
        # SSHSpawner.hub.public_host = server.host
        # assert(SSHSpawner.hub.public_host == "127.0.0.1")

    def test_remote(self,server):
        assert(True)
        # SSHSpawner.remote_hosts = server.host.split()
        # loop = asyncio.get_event_loop()
        # loop.run_until_complete(SSHSpawner.start(self))
        # SSHSpawner.user.server = server()
        # SSHSpawner.user.name = server.users
        # SSHSpawner.user.url = "127.0.0.1"
        # port = self.SSHSpawner.remote_port
        # host = self.SSHSpawner.remote_host
        # random_port = loop.run_until_complete(self.SSHSpawner.remote_random_port())
        # assert(port == "22")
        # assert(host == "127.0.0.1")
        # assert(random_port == 80)
        # assert(SSHSpawner.user.name == "testuser")

    def test_env(self):
        assert(True)
        # env = self.SSHSpawner.user_env()
        # assert(env['JPY_USER'] == "testuser")
        # assert(env['JPY_COOKIE_NAME'] == "testcookie")
        # assert(env['PATH'] == "/usr/bin:/bin:/usr/sbin:/sbin:/usr/local/bin")
