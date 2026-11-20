import os

from compas_invocations2 import build
from compas_invocations2 import style
from compas_invocations2 import tests
from invoke.collection import Collection
from invoke.tasks import task


@task
def typecheck(ctx):
    """Check the types."""
    ctx.run("pyright")


ns = Collection(
    style.check,
    style.lint,
    style.format,
    tests.test,
    typecheck,
    build.prepare_changelog,
    build.clean,
    build.release,
)
ns.configure({"base_folder": os.path.dirname(__file__)})
