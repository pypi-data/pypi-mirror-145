from ._internal import SubCommand, RootCommand

__all__ = ["npm",
           "npm_run"]


class Npm(RootCommand):
    """https://docs.npmjs.com/about-npm"""
    globals = globals()


@Npm.subcommand
class Run(SubCommand):
    """https://docs.npmjs.com/cli/v8/commands/npm-run-script"""


npm = Npm()
npm_run = getattr(npm, "run")