import os

from compas_invocations2 import build
from compas_invocations2 import style
from compas_invocations2 import tests
from invoke.collection import Collection

ns = Collection(
    style.check,
    style.lint,
    style.format,
    tests.test,
    build.prepare_changelog,
    build.clean,
    build.release,
)
ns.configure({"base_folder": os.path.dirname(__file__)})
