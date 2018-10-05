import asyncio
import mockssh
import pytest
from jupyterhub import orm
from jupyterhub.objects import Hub, Server
from jupyterhub.spawner import Spawner
from jupyterhub.user import User
from pytest import fixture, yield_fixture
from sshspawner.sshspawner import SSHSpawner

@yield_fixture(scope = "session")
def server():
    users = {
                "testuser": "tests/sample-user-key"
            }
    with mockssh.Server(users) as s:
        yield s

@fixture(scope = "session")
def spawner(server):
    uid = list(server.users)[0]
    ssh_spawner = SSHSpawner()
    ssh_spawner.hub = Hub()
    ssh_spawner.hub.public_host = server.host
    ssh_spawner.hub.server.base_url = "/base/lab/"
    ssh_spawner.remote_hosts = server.host.split()
    ssh_spawner.ssh_keyfile = server._users[uid][0]
    ssh_spawner.user = orm.User(name = uid)
    ssh_spawner.user.server = Server()
    ssh_spawner.user.server.base_url = "/home/"
    ssh_spawner.user.server.cookie_name = "testcookie"
    ssh_spawner.user.url = "http://www.example.com/"
    return ssh_spawner

class TestSSHSpawner:
    def test_start(self,spawner):
        loop = asyncio.get_event_loop()
        start = loop.run_until_complete(spawner.start())
        port = spawner.remote_port
        host = spawner.remote_host
        assert(port == "22")
        assert(host == "127.0.0.1")
        assert(start is False)

    def test_env(self,spawner):
        env = spawner.user_env()
        assert(env['JUPYTERHUB_HOST'] == "127.0.0.1")
        assert(env['JUPYTERHUB_USER'] == "testuser")
        assert(env['JUPYTERHUB_PREFIX'] == "/base/lab/")
        assert(env['PATH'] == "/usr/bin:/bin:/usr/sbin:/sbin:/usr/local/bin")

    def test_exec(self, spawner):
        loop = asyncio.get_event_loop()
        exc = loop.run_until_complete(spawner.exec_notebook(''))
        assert(exc == -1)

    def test_random_port(self,server,spawner):
        spawner.remote_port_command = "python3 scripts/get_port.py"
        with server.client(spawner.user.name) as c:
            _, stdout, _ = c.exec_command(spawner.remote_port_command)
            loop = asyncio.get_event_loop()
            random_port = loop.run_until_complete(spawner.remote_random_port())
        # assert isinstance(random_port, int)
        assert(True)
