from ._internal import SubCommand, RootCommand, parameter

__all__ = ["docker",
           ]


class Ps(SubCommand):
    __name__ = "ps"

    @parameter()
    def all(self):
        """显示所有容器"""

    @parameter()
    def quiet(self):
        """只显示容器ID"""


class Rm(SubCommand):
    __name__ = "rm"


class Rmi(SubCommand):
    """移除一个或者多个镜像"""
    __name__ = "rmi"


class Diff(SubCommand):
    """显示了镜像被实例化成一个容器以来哪些文件受到了影响

    https://docs.docker.com/engine/reference/commandline/diff/
    """
    __name__ = "diff"


class Tag(SubCommand):
    """给一个Docker镜像打标签"""
    __name__ = "tag"


class Stop(SubCommand):
    """干净地终结容器"""
    __name__ = "stop"


class Logs(SubCommand):
    """抓取容器的日志

    源码: https://github.com/docker/compose/blob/v2/cmd/compose/logs.go
    """
    __name__ = "logs"


class Exec(SubCommand):
    """在容器执行bash命令"""
    __name__ = "exec"


class Images(SubCommand):
    """列出所有镜像"""
    __name__ = "images"


class Restart(SubCommand):
    """重启一个或多个容器"""
    __name__ = "restart"


class Version(SubCommand):
    __name__ = "version"


class Start(SubCommand):
    """启动一个或多个停止状态的容器"""
    __name__ = "start"


class Commit(SubCommand):
    """将一个Docker容器作为一个镜像提交"""
    __name__ = "commit"


class Docker(RootCommand):
    __name__ = 'docker'
    globals = globals()
    subcommands = [
            Ps,
            Rm,
            Rmi,
            Tag,
            Stop,
            Diff,
            Logs,
            Exec,
            Start,
            Images,
            Commit,
            Restart,
            Version,
        ]


@Docker.subcommand
class Pull(SubCommand):
    """拉取镜像

    https://docs.docker.com/engine/reference/commandline/pull/
    """
    __name__ = "pull"


@Docker.subcommand
class Search(SubCommand):
    """检索Docker Hub镜像

    Docker实践(第2版) 第95页
    """
    __name__ = "search"


@Docker.subcommand
class Inspect(SubCommand):
    """显示容器的信息

    Return low-level information on Docker objects

    Docker实践(第2版) 技巧30

    https://docs.docker.com/engine/reference/commandline/inspect/
    """
    __name__ = "inspect"

    @parameter(short="-f")
    def format(self):
        """使用Go模板格式化输出

        使用format标志的例子: https://docs.docker.com/engine/reference/commandline/inspect/#examples
        """

    def get_instance_IP_address(self, obj):
        """https://docs.docker.com/engine/reference/commandline/inspect/#get-an-instances-ip-address

        单个使用{{.NetworkSettings.IPAddress}}
        """
        self.format("'{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}'")(obj)

    def get_instance_MAC_address(self, obj):
        """https://docs.docker.com/engine/reference/commandline/inspect/#get-an-instances-mac-address"""

    def get_instance_log_path(self, obj):
        """https://docs.docker.com/engine/reference/commandline/inspect/#get-an-instances-log-path"""
        self.format("'{{.LogPath}}'")(obj)

    def get_instance_image_name(self, obj):
        """https://docs.docker.com/engine/reference/commandline/inspect/#get-an-instances-image-name"""
        self.format("'{{.Config.Image}}'")(obj)

    def list_all_port_bindings(self, obj):
        """https://docs.docker.com/engine/reference/commandline/inspect/#list-all-port-bindings"""
        self.format("'{{range $p, $conf := .NetworkSettings.Ports}} {{$p}} -> {{(index $conf 0).HostPort}} {{end}}'")(obj)

    def get_subsection_in_JSON_format(self, obj):
        """https://docs.docker.com/engine/reference/commandline/inspect/#get-a-subsection-in-json-format"""
        self.format("'{{json .Config}}'")(obj)


@Docker.subcommand
class Run(SubCommand):
    """以容器形式运行一个Docker镜像

    源码: https://github.com/docker/compose/blob/v2/cmd/compose/run.go
    """
    __name__ = "run"

    @parameter(short="-i")
    def interactive(self):
        """保持STDIN打开, 用于控制台交互"""

    @parameter(short="-t")
    def tty(self):
        """分配TTY设备, 可以支持终端登录"""

    @parameter(short="-p")
    def publish(self):
        """指定容器包路的端口"""

    @parameter()
    def name(self):
        """分配容器的名称"""

    @parameter(short="-d")
    def detach(self):
        """在后台运行容器和打印容器id"""

    @parameter(short="-l")
    def label(self):
        """设置LABEL元数据"""

    @parameter(short="-v")
    def volume(self):
        """挂载卷, 格式 本地目录:远程目录"""

    # ============= 以下参数不常用 =============================
    @parameter()
    def restart(self):
        """设置重启策略, 默认值'no'。

        策略:

        * no:容器退出时不重启;
        * always:容器退出时总是重启;
        * unless-stopped:总是重启, 不过显示停止除外
        * on-failure[:max-retry]:只在失败时重启
        """

    @parameter(long="--volumes-from")
    def volumes_from(self):
        """挂载指定的数据容器

        Docker实践(第2版) 技巧37
        """


@Docker.subcommand
class Build(SubCommand):
    """构建一个Docker镜像

    文档: https://docs.docker.com/engine/reference/commandline/build/
    """
    __name__ = "build"

    @parameter(short="-t")
    def tag(self):
        """打标签, 格式: 'name:tag'"""

    @parameter(long="--build-arg")
    def build_arg(self):
        """设置运行时的变量值(ARG)"""

    # ======== 以下参数不常用 ========================
    @parameter(long="--no-cache")
    def no_cache(self):
        """构建时不使用缓存"""


docker = Docker()
