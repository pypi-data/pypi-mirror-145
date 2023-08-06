from ._internal import RootCommand, parameter


class Protoc(RootCommand):
    """

    protoc --go_out=. --go_opt=paths=source_relative --go-grpc_out=. --go-grpc_opt=paths=source_relative browser.proto
    """
    __name__ = 'protoc'
    globals = globals()

    @parameter()
    def go_out(self):
        """指定pb文件所在生成目录"""

    @parameter(default="paths=source_relative")
    def go_opt(self):
        """固定值"""

    @parameter(long="--go-grpc_out", default="指定grpc pb文件所在生成目录")
    def go_grpc_out(self):
        """指定grpc pb文件所在生成目录"""

    @parameter(long="--go-grpc_opt", default="paths=source_relative")
    def go_grpc_out(self):
        """固定值"""


protoc = Protoc()