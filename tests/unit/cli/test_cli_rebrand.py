# -*- coding: utf-8 -*-
"""Tests for the cici-workbench CLI rebrand (Issue #3).

Verifies that the Python distribution package name and CLI entry points
match the rebrand decisions: package name ``cici-workbench``, primary
CLI command ``cici``, and backward-compatible alias ``copaw``.
"""

from __future__ import annotations

import subprocess
import sys
import tomllib
from pathlib import Path


def _load_pyproject() -> dict:
    pyproject_path = Path(__file__).parents[3] / "pyproject.toml"
    return tomllib.loads(pyproject_path.read_text(encoding="utf-8"))


def test_distribution_package_name_is_cici_workbench() -> None:
    """[project] name must be cici-workbench.

    PRD 依据: PRD 实现决策 › 品牌标识映射 / 英文 slug
    """
    data = _load_pyproject()
    assert data["project"]["name"] == "cici-workbench"


def test_cici_cli_entry_points_to_click_group() -> None:
    """[project.scripts] must expose cici -> qwenpaw.cli.main:cli.

    PRD 依据: PRD 实现决策 › 品牌标识映射 / CLI 命令; 用户故事 US-5
    """
    data = _load_pyproject()
    scripts = data["project"]["scripts"]
    assert scripts["cici"] == "qwenpaw.cli.main:cli"


def test_copaw_alias_points_to_same_entry_as_cici() -> None:
    """[project.scripts] must keep copaw as a backward-compatible alias.

    PRD 依据: PRD 实现决策 › 品牌标识映射 / CLI 命令
    """
    data = _load_pyproject()
    scripts = data["project"]["scripts"]
    assert "copaw" in scripts
    assert scripts["copaw"] == scripts["cici"] == "qwenpaw.cli.main:cli"


def test_cici_help_runs_successfully() -> None:
    """After pip install -e ., `cici --help` must print usage and exit 0.

    PRD 依据: PRD 测试决策 › 字符串扫描 seam; 用户故事 US-5
    """
    result = subprocess.run(
        [sys.executable, "-m", "pip", "show", "cici-workbench"],
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, "cici-workbench must be installed"

    help_result = subprocess.run(
        ["cici", "--help"],
        capture_output=True,
        text=True,
    )
    assert help_result.returncode == 0
    assert "Usage: cici" in help_result.stdout


def test_copaw_help_runs_successfully() -> None:
    """After pip install -e ., `copaw --help` must print usage and exit 0.

    PRD 依据: PRD 实现决策 › 品牌标识映射 / CLI 命令
    """
    help_result = subprocess.run(
        ["copaw", "--help"],
        capture_output=True,
        text=True,
    )
    assert help_result.returncode == 0
    assert "Usage: copaw" in help_result.stdout
