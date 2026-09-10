"""crew_tick must import without pydantic / settle / paper_book."""

from __future__ import annotations

import ast
import os
import subprocess
import sys
from pathlib import Path

CREW_TICK = (
    Path(__file__).resolve().parents[1]
    / "src"
    / "golf_offshoot"
    / "learning_lane_15m"
    / "crew_tick.py"
)


def test_crew_tick_source_does_not_import_settle_or_observability():
    tree = ast.parse(CREW_TICK.read_text(encoding="utf-8"))
    imported: list[str] = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            imported.extend(alias.name for alias in node.names)
        elif isinstance(node, ast.ImportFrom) and node.module:
            imported.append(node.module)
    joined = " ".join(imported)
    assert "golf_offshoot.learning_lane_15m.settle" not in imported
    assert "golf_offshoot.strategy.paper_book" not in imported
    assert "golf_offshoot.operator_surface.observability" not in imported
    assert "pydantic" not in joined
    assert "golf_offshoot.repo_paths" in imported


def test_fresh_import_does_not_load_settle_or_paper_book():
    src = Path(__file__).resolve().parents[1] / "src"
    script = (
        "import importlib, sys\n"
        "class _Block:\n"
        "    def find_spec(self, name, path, target=None):\n"
        "        if name == 'pydantic' or (name and name.startswith('pydantic.')):\n"
        "            raise ModuleNotFoundError('pydantic blocked')\n"
        "        return None\n"
        "sys.meta_path.insert(0, _Block())\n"
        "importlib.import_module('golf_offshoot.learning_lane_15m.crew_tick')\n"
        "from golf_offshoot.learning_lane_15m.crew_tick import stamp_cos_closeout\n"
        "from golf_offshoot.learning_lane_15m.paths import set_15m_root_override\n"
        "from pathlib import Path\n"
        "import tempfile\n"
        "set_15m_root_override(Path(tempfile.mkdtemp()))\n"
        "assert stamp_cos_closeout(commit='testhash') is None\n"
        "assert 'golf_offshoot.learning_lane_15m.settle' not in sys.modules\n"
        "assert 'golf_offshoot.strategy.paper_book' not in sys.modules\n"
        "print('ok')\n"
    )
    env = os.environ.copy()
    env["PYTHONPATH"] = str(src)
    proc = subprocess.run(
        [sys.executable, "-c", script],
        cwd=str(src.parent),
        env=env,
        capture_output=True,
        text=True,
        check=False,
    )
    assert proc.returncode == 0, proc.stdout + proc.stderr
    assert "ok" in proc.stdout
