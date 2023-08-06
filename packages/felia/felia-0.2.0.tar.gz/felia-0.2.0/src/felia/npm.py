from ._internal import SubCommand, RootCommand


class Npm(RootCommand):
    """https://docs.npmjs.com/about-npm"""
    globals = globals()


@Npm.subcommand
class Run(SubCommand):
    """https://docs.npmjs.com/cli/v8/commands/npm-run-script"""


npm = Npm()