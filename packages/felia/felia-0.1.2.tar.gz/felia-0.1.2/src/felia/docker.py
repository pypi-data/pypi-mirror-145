from ._internal import SubCommand, RootCommand, parameter

__all__ = ["docker",
           ]


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


class Images(SubCommand):
    """https://docs.docker.com/engine/reference/commandline/images/

    列出所有镜像"""
    __name__ = "images"

    @parameter(short="-a")
    def all(self):
        """返回所有镜像层的列表

        Docker实践(第2版) —— 技巧46
        """


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
            Rmi,
            Tag,
            Stop,
            Diff,
            Logs,
            Start,
            Images,
            Commit,
            Restart,
            Version,
        ]


@Docker.subcommand
class Ps(SubCommand):
    __name__ = "ps"

    @parameter()
    def all(self):
        """显示所有容器"""

    @parameter()
    def quiet(self):
        """只显示容器ID"""

    @parameter()
    def filter(self):
        """过滤输出结果

        输出退出状态的容器ID
        docker ps -a -q --filter status=exited
        删除所有已经退出的容器
        docker ps -a -q --filter status=exited | xargs --no-run-if-empty docker rm -f
        """


@Docker.subcommand
class Rm(SubCommand):
    __name__ = "rm"

    @parameter(short="-v")
    def volumes(self):
        """删除跟容器关联的匿名卷

        卷的删除还可以使用docker volume —— Docker实践(第2版) 技巧43
        """


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

    @parameter()
    def rm(self):
        """退出容器时自动删除"""

    @parameter(short="-w")
    def workdir(self):
        """切换当前目录"""

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
class Exec(SubCommand):
    """https://docs.docker.com/engine/reference/commandline/exec/

    在容器执行bash命令

    Docker实践(第2版) —— 技巧47

    三种模式

    * 基本: 在命令行上对容器同步地执行命令
    * 守护进程: 在容器的后台执行命令
    * 交互: 执行命令并允许用户与其交互
    """
    __name__ = "exec"

    @parameter(short="-d")
    def detach(self):
        """在容器后台执行命令"""

    @parameter(short="-i", use_shell=True)
    def interactive(self):
        """可交互的"""

    @parameter(short="-t")
    def tty(self):
        """设置一个TTY设备, 一般跟-i一起使用"""

    def bash(self, container):
        """docker exec -it container /bin/bash"""
        return self.interactive().tty()(container, "/bin/bash")


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


@Docker.subcommand
class Push(SubCommand):
    """https://docs.docker.com/engine/reference/commandline/push/

    Docker实践(第2版) 技巧17

    假设在Docker Hub上的用户名是adev, 本地有一个core-dev的镜像

    docker tag core-dev:latest /adevcore-dev:latest
    docker push adev/core-dev:latest
    """
    __name__ = "push"


@Docker.subcommand
class Login(SubCommand):
    """https://docs.docker.com/engine/reference/commandline/login/

    登录注册中心
    """
    __name__ = "login"
    use_shell = True


@Docker.subcommand
class Export(SubCommand):
    """https://docs.docker.com/engine/reference/commandline/export/

    导出镜像文件

    Docker实践(第2版) —— 技巧52
    """
    __name__ = "export"


@Docker.subcommand
class Import(SubCommand):
    """https://docs.docker.com/engine/reference/commandline/import/

    导入镜像文件

    Docker实践(第2版) —— 技巧52
    """
    __name__ = "import"


@Docker.subcommand
class History(SubCommand):
    """https://docs.docker.com/engine/reference/commandline/history/

    显式镜像的历史信息

    Docker实践(第2版) —— 技巧52
    """
    __name__ = "history"

# ====================== Management Commands: ===============================


@Docker.subcommand
class Volume(SubCommand):
    """https://docs.docker.com/engine/reference/commandline/volume_create/"""
    __name__ = "volume"

    @parameter()
    def ls(self):
        """https://docs.docker.com/engine/reference/commandline/volume_ls/

        列出所有卷"""

    @parameter(use_shell=True)
    def prune(self):
        """https://docs.docker.com/engine/reference/commandline/volume_prune/

        删除所有未使用的本地卷
        """

    def prune_f(self):
        """跳过确认步骤"""
        return self.prune("-f")


docker = Docker()
