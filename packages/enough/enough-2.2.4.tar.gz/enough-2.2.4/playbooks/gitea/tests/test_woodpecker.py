import os
import re
import requests
import time
import yaml
from bs4 import BeautifulSoup

from enough.common import retry

testinfra_hosts = ['ansible://gitea-host']


def get_domain(inventory):
    vars_dir = f'{inventory}/group_vars/all'
    return yaml.safe_load(open(vars_dir + '/domain.yml'))['domain']


class Gitea(object):
    def __init__(self, url):
        self._url = url
        self._users = self.users_factory()(self)
        self._projects = self.projects_factory()(self)
        self._s = requests.Session()

    @property
    def url(self):
        return self._url

    @property
    def projects(self):
        return self._projects

    @property
    def users(self):
        return self._users

    @property
    def s(self):
        return self._s

    def certs(self, certs):
        self.s.verify = certs

    def authenticate(self, **kwargs):
        self._session()
        self.login(kwargs["username"], kwargs["password"])
        self._user = self.s.get(f"{self.s.api}/user").json()

    @property
    def is_authenticated(self):
        return hasattr(self, "_user")

    @property
    def username(self):
        return self._user["login"]

    @property
    def is_admin(self):
        return self._user["is_admin"]

    def _session(self):
        self.s.api = f"{self.url}/api/v1"

    def login(self, username, password):
        r = self.s.post(
            f"{self.s.api}/users/{username}/tokens",
            auth=(username, password),
            json={
                "name": f"TEST{time.time()}",
            },
        )
        r.raise_for_status()
        self.set_token(r.json()["sha1"])

    def get_token(self):
        return self.token

    def set_token(self, token):
        self.token = token
        self.s.headers["Authorization"] = f"token {token}"

    def projects_factory(self):
        return GiteaProjects

    def users_factory(self):
        return GiteaUsers


class GiteaUsers(object):
    def __init__(self, forge):
        self._forge = forge

    @property
    def forge(self):
        return self._forge

    @property
    def s(self):
        return self.forge.s

    def get(self, username):
        if username == self.forge.username:
            r = self.s.get(f"{self.s.api}/user")
        elif self.forge.is_admin:
            r = self.s.get(f"{self.s.api}/user", params={"sudo": username})
        else:
            r = self.s.get(f"{self.s.api}/users/{username}")
        if r.status_code == 404:
            return None
        else:
            r.raise_for_status()
            return GiteaUser(self.forge, r.json())


class GiteaUser(object):
    def __init__(self, forge, user):
        self._forge = forge
        self._user = user

    @property
    def url(self):
        return f"{self.forge.url}/{self.username}"

    @property
    def username(self):
        return self._user["username"]

    @property
    def emails(self):
        return [self._user["email"]]

    @property
    def forge(self):
        return self._forge

    @property
    def s(self):
        return self.forge.s

    def get_keys(self):
        r = self.s.get(f"{self.s.api}/user/keys")
        r.raise_for_status()
        return r.json()

    def get_key(self, title):
        for key in self.get_keys():
            if key["title"] == title:
                return key
        return None

    def delete_key(self, title):
        key = self.get_key(title)
        if key:
            r = self.s.delete(f"{self.s.api}/user/keys/{key['id']}")
            r.raise_for_status()

    def create_key(self, title, key):
        data = {
            "title": title,
            "key": key,
        }
        r = self.s.post(f"{self.s.api}/user/keys", data=data)
        print(r.text)
        r.raise_for_status()

    def get_applications(self):
        r = self.s.get(f"{self.s.api}/user/applications/oauth2")
        r.raise_for_status()
        return r.json()

    def get_application(self, name):
        for app in self.get_applications():
            if app["name"] == name:
                return app
        return None

    def delete_application(self, name):
        app = self.get_application(name)
        if app:
            r = self.s.delete(f"{self.s.api}/user/applications/oauth2/{app['id']}")
            r.raise_for_status()


class GiteaProjects(object):
    def __init__(self, forge):
        self._forge = forge

    @property
    def forge(self):
        return self._forge

    @property
    def s(self):
        return self.forge.s

    def project_factory(self):
        return GiteaProject

    def get(self, namespace, project):
        r = self.s.get(f"{self.s.api}/repos/{namespace}/{project}")
        if r.status_code == requests.codes.ok:
            return self.project_factory()(self.forge, r.json())
        else:
            return None

    class DeletionInProgress(Exception):
        pass

    @retry.retry(DeletionInProgress, tries=5)
    def _create(self, namespace, project, **data):
        data.update(
            {
                "name": project,
            }
        )
        r = self.s.post(f"{self.s.api}/user/repos", data=data)
        print(r.text)
        if r.status_code == 201:
            return self.get(namespace, project)
        r.raise_for_status()

    def create(self, namespace, project, **data):
        p = self.get(namespace, project)
        if p is None:
            return self._create(namespace, project, **data)
        else:
            return p

    def delete(self, namespace, project):
        p = self.get(namespace, project)
        if p is None:
            return False
        r = self.s.delete(f"{self.s.api}/repos/{namespace}/{project}")
        r.raise_for_status()
        while self.get(namespace, project) is not None:
            time.sleep(1)
        return True


class GiteaProject(object):
    def __init__(self, forge, project):
        self._forge = forge
        self._project = project

    @property
    def id(self):
        return self._project["id"]

    @property
    def namespace(self):
        return self._project["owner"]["login"]

    @property
    def project(self):
        return self._project["name"]

    @property
    def ssh_url_to_repo(self):
        return self._project["ssh_url"]

    @property
    def http_url_to_repo(self):
        return self._project["clone_url"]


def test_admin_user(host):
    with host.sudo():
        cmd = host.run("docker exec --user 1000 gitea gitea admin user list --admin")
        print(cmd.stdout)
        print('--------------------------')
        print(cmd.stderr)
        assert 0 == cmd.rc
        assert "root" in cmd.stdout


def woodpecker_sign_in(request, pytestconfig, host):
    certs = request.session.infrastructure.certs()
    domain = get_domain(pytestconfig.getoption("--ansible-inventory"))

    #
    # Gitea home page
    #
    g = requests.Session()
    g_url = f'https://gitea.{domain}'
    r = g.get(g_url + '/user/login', verify=certs)
    r.raise_for_status()
    soup = BeautifulSoup(r.text, 'html.parser')
    csrf = soup.select(
        'form[action="/user/login"] input[name="_csrf"]')[0]['value']

    #
    # Gitea Login
    #
    r = g.post(g_url + '/user/login', data={
        '_csrf': csrf,
        'user_name': 'root',
        'password': "etquofEtseudett",
    }, verify=certs)
    r.raise_for_status()

    #
    # Revoke woodpecker application (in case test is run multiple times)
    #
    r = g.get(g_url + '/user/settings/applications', verify=certs)
    r.raise_for_status()
    soup = BeautifulSoup(r.text, 'html.parser')
    csrf = soup.select(
        'form[action="/user/settings/applications"] input[name="_csrf"]')[0]['value']
    for b in soup.select('button[data-modal-id="revoke-gitea-oauth2-grant"]'):
        data = {
            "id": b["data-id"],
            '_csrf': csrf,
        }
        r = g.post(g_url + "/user/settings/applications/oauth2/revoke", data=data, verify=certs)
        r.raise_for_status()

    #
    # Woodpecker login
    #
    woodpecker = requests.Session()
    woodpecker.url = f'https://woodpecker.{domain}'
    r = woodpecker.get(woodpecker.url + '/authorize',
                       allow_redirects=False,
                       verify=certs)
    assert 'login/oauth/authorize' in r.headers['Location']
    r.raise_for_status()

    #
    # Gitea OAuth confirmation page
    #
    r = g.get(r.headers['Location'],
              allow_redirects=False,
              verify=certs)
    r.raise_for_status()
    soup = BeautifulSoup(r.text, 'html.parser')
    data = {
        "redirect_uri": f"https://woodpecker.{domain}/authorize",
    }
    for input in soup.select('form[action="/login/oauth/grant"] input[type="hidden"]'):
        if input.get('name') is None or input.get('value') is None:
            continue
        data[input['name']] = input['value']
        # print(str(data))
        # print(soup.prettify())
    r = g.post(g_url + '/login/oauth/grant', data=data,
               allow_redirects=False,
               verify=certs)
    r.raise_for_status()
    assert 'authorize?code' in r.headers['Location']

    r = woodpecker.get(r.headers['Location'], allow_redirects=False, verify=certs)
    r.raise_for_status()

    #
    # Woodpecker CSRF
    #
    r = woodpecker.get(woodpecker.url + '/web-config.js',
                       allow_redirects=False,
                       verify=certs)
    r.raise_for_status()
    csrf = re.findall('window.WOODPECKER_CSRF = "(.*?)"', r.text)[0]

    #
    # Woodpecker token
    #
    r = woodpecker.post(woodpecker.url + '/api/user/token',
                        headers={'X-CSRF-TOKEN': csrf},
                        allow_redirects=False,
                        verify=certs)
    r.raise_for_status()
    return r.text


certs_volumes = ("/usr/local/share/ca-certificates/infrastructure:"
                 "/usr/local/share/ca-certificates/infrastructure:ro")

woodpecker_yml = f"""
clone:
 git:
   image: woodpeckerci/plugin-git
   volumes:
     - /etc/ssl/certs:/etc/ssl/certs:ro
     - {certs_volumes}

pipeline:
  something:
    image: golang
    volumes:
      - /tmp/out:/tmp/out
    commands:
      - touch /tmp/out/done
"""


def test_woodpecker_run(request, pytestconfig, host, tmpdir):
    certs = request.session.infrastructure.certs()
    domain = host.run("hostname -d").stdout.strip()

    #
    # Login Gitea
    #
    gitea = Gitea(f'https://gitea.{domain}')
    gitea.certs(certs)
    username = "root"
    password = "etquofEtseudett"
    gitea.authenticate(username=username, password=password)
    u = gitea.users.get("root")
    assert u.username == "root"
    #
    # Create project
    #
    gitea.projects.delete(username, "testproject")
    assert gitea.projects.get(username, "testproject") is None
    p = gitea.projects.create(username, "testproject")
    assert p.project == "testproject"
    #
    # Enable the project in Woodpecker
    #
    woodpecker_token = woodpecker_sign_in(request, pytestconfig, host)
    woodpecker = requests.Session()
    woodpecker.url = f'https://woodpecker.{domain}'
    woodpecker.headers = {'Authorization': f'Bearer {woodpecker_token}'}
    woodpecker.get(woodpecker.url + "/api/user/repos?all=true&flush=true",
                   verify=certs).raise_for_status()
    woodpecker.delete(woodpecker.url + f"/api/repos/{username}/testproject",
                      verify=certs).raise_for_status()
    woodpecker.post(woodpecker.url + f"/api/repos/{username}/testproject",
                    verify=certs).raise_for_status()
    #
    # Errors are not returned, they are in the logs
    # tests/run-tests.sh tests/ssh gitea gitea-host
    # sudo bash
    # cd /srv/woodpecker
    # docker-compose down
    # docker-compose up
    #
    woodpecker.patch(woodpecker.url + f"/api/repos/{username}/testproject",
                     json={
                         "trusted": True,
                     },
                     verify=certs).raise_for_status()

    #
    # Register SSH key
    #
    os.system(f"ssh-keygen -q -f {tmpdir}/key -N ''")
    key = open(f"{tmpdir}/key.pub").read()
    u.delete_key("woodpecker")
    u.create_key("woodpecker", key)
    #
    # Push to project
    #
    url = p.ssh_url_to_repo
    os.system(f"""
    set -ex
    cd {tmpdir}
    mkdir testproject
    cd testproject
    git init
    git config user.email "you@example.com"
    git config user.name "Your Name"
    git config http.sslVerify false
    git remote add origin {url}
    """)
    open(f"{tmpdir}/testproject/.woodpecker.yml", "w").write(woodpecker_yml)
    expected_file = "/tmp/out/done"
    with host.sudo():
        host.run(f"rm -f {expected_file}")
    ssh_command = (
        f"ssh -i {tmpdir}/key -o UserKnownHostsFile=/dev/null -o StrictHostKeyChecking=no"
    )
    os.system(f"""
    cd {tmpdir}/testproject
    git add .woodpecker.yml
    git commit -m 'test'
    export GIT_SSH_COMMAND="{ssh_command}"
    git push -u origin master
    """)

    @retry.retry(AssertionError, tries=7)
    def wait_for_expected_file():
        assert host.file(expected_file).exists
    wait_for_expected_file()
