import importlib.metadata

from brg_framework import PACKAGES
from brg_framework import __version__
from brg_framework.cli import install
from brg_framework.cli import main
from brg_framework.cli import skill_folder


def test_version_matches_the_installed_metadata():
    assert __version__ == importlib.metadata.version("brg_framework")


def test_every_brg_package_is_installed():
    for name in PACKAGES:
        assert importlib.metadata.version(name)


def test_the_skill_is_found():
    folder = skill_folder()
    assert (folder / "SKILL.md").exists()
    assert (folder / "scripts" / "copy_example.py").exists()


def test_install_copies_the_skill_into_every_agent_folder(tmp_path):
    written = install(tmp_path)
    assert len(written) == 2
    for target in written:
        assert (target / "SKILL.md").read_text() == (skill_folder() / "SKILL.md").read_text()
    assert install(tmp_path) == written


def test_version_command_lists_the_packages(capsys):
    assert main(["version"]) == 0
    output = capsys.readouterr().out
    assert all(name in output for name in PACKAGES)
