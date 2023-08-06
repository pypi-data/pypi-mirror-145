from ._internal import RootCommand, parameter


class SSH(RootCommand):
    __name__ = 'ssh'
    globals = globals()

    @parameter(long="-T")
    def T(self):
        """测试连通性

        ssh -T git@github.com
        """

    def t_github(self):
        self.T().execute("git@github.com")


class SSHKeygen(RootCommand):
    """

    install: apt-get install ssh
    重启ssh服务: /etc/init.d/ssh restart
    """
    __name__ = 'ssh-keygen'
    globals = globals()
    use_shell = True

    @parameter(long="-t")
    def t(self):
        """[dsa | ecdsa | ecdsa-sk | ed25519 | ed25519-sk | rsa]"""


ssh = SSH()
ssh_keygen = SSHKeygen()
