import importlib.util
from pathlib import Path

ROOT = Path(__file__).parents[2]
SCRIPT = ROOT / "skills" / "brg-methods" / "scripts" / "copy_example.py"

spec = importlib.util.spec_from_file_location("copy_example", SCRIPT)
copy_example = importlib.util.module_from_spec(spec)
spec.loader.exec_module(copy_example)


def test_every_example_page_has_a_name_and_code():
    pages = [path for path in (ROOT / "server" / "src" / "brg_mcp").glob("*/*_compas/*.md")]
    assert pages
    for path in pages:
        name = copy_example.name_of(path.relative_to(ROOT).as_posix())
        assert name and "{}.py".format(name) in path.read_text()
        assert copy_example.code_of(path.read_text()).startswith(("import", "from"))


def test_other_files_are_not_examples():
    assert copy_example.name_of("server/src/brg_mcp/fd/01_algorithm.md") is None
