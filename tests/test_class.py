import asyncio
import mockssh
import pytest
from jupyterhub import orm
from jupyterhub.objects import Hub, Server
from jupyterhub.spawner import Spawner
from jupyterhub.user import User
from pytest import fixture, yield_fixture
from sshspawner.sshspawner import SSHSpawner

@yield_fixture(scope= "session")
def server():
    users = {
                "testuser": "tests/sample-user-key"
            }
    with mockssh.Server(users) as s:
        yield s

@fixture(scope= "session")
def spawner(server):
    ssh_spawner = SSHSpawner()
    ssh_spawner.hub = Hub()
    ssh_spawner.hub.public_host = server.host
    ssh_spawner.remote_hosts = server.host.split()
    ssh_spawner.user = orm.User(name = list(server.users)[0])
    ssh_spawner.user.server = Server()
    return ssh_spawner

class TestSSHSpawner:
    def test_start(self,server,spawner):
        loop = asyncio.get_event_loop()
        loop.run_until_complete(spawner.start())
        port = spawner.remote_port
        host = spawner.remote_host
        assert(port == "22")
        assert(host == "127.0.0.1")
        assert(spawner.user.name == "testuser")

    def test_env(self,server,spawner):
        spawner.user.server.cookie_name = "testcookie"
        spawner.user.url = "http://www.example.com/"
        env = spawner.user_env()
        assert(env['JPY_USER'] == "testuser")
        assert(env['JPY_COOKIE_NAME'] == "testcookie")
        assert(env['PATH'] == "/usr/bin:/bin:/usr/sbin:/sbin:/usr/local/bin")

    def test_random_port(self,server,spawner):
        loop = asyncio.get_event_loop()
        random_port = loop.run_until_complete(spawner.remote_random_port())
        assert(True)