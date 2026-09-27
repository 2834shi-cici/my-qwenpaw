# -*- coding: utf-8 -*-
"""Design input state verification for the cici的工作台 rebrand.

Issue #2 (``#D-global``) is a ``design-input`` acceptance-closure issue:
the PRD explicitly declares that this rebrand reuses the existing Console
design system and does **not** introduce a ``docs/design/DESIGN.md``, a
``platforms.md`` multi-platform spec, or ``references/`` mockup PNGs.

These tests guard that contract so an accidental ``docs/design/`` creation
is caught by CI. See ``docs/prd/rebrand-cici-workbench.md`` PRD 末尾摘要.
"""

from __future__ import annotations

from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[2]
DESIGN_DIR = REPO_ROOT / "docs" / "design"
PRD_PATH = REPO_ROOT / "docs" / "prd" / "rebrand-cici-workbench.md"


def _read_prd() -> str:
    return PRD_PATH.read_text(encoding="utf-8")


def test_design_md_does_not_exist() -> None:
    """PRD 末尾摘要声明 ``docs/design/DESIGN.md`` 不存在（本 PRD 不涉及新设计系统）。"""
    design_md = DESIGN_DIR / "DESIGN.md"
    assert not design_md.exists(), (
        f"{design_md.relative_to(REPO_ROOT)} 不应存在；"
        "PRD 声明本品牌替换沿用现有设计系统，无需新建 DESIGN.md"
    )


def test_no_platforms_md() -> None:
    """单端 ``default``，无 ``docs/design/platforms.md``。"""
    platforms_md = DESIGN_DIR / "platforms.md"
    assert not platforms_md.exists(), (
        f"{platforms_md.relative_to(REPO_ROOT)} 不应存在；"
        "本品牌替换为单端 default，无多端 platforms.md"
    )


def test_no_references_png() -> None:
    """spec-driven，无 ``docs/design/references/`` mockup PNG。"""
    references_dir = DESIGN_DIR / "references"
    if not references_dir.exists():
        return
    png_files = list(references_dir.glob("*.png"))
    assert not png_files, (
        f"{references_dir.relative_to(REPO_ROOT)} 下不应存在 PNG mockup；"
        f"本品牌替换为 spec-driven，发现: {[p.name for p in png_files]}"
    )


def test_prd_declares_no_design_md() -> None:
    """PRD 末尾摘要须声明 ``docs/design/DESIGN.md`` 不存在。"""
    prd = _read_prd()
    assert "docs/design/DESIGN.md" in prd, (
        "PRD 应提及 docs/design/DESIGN.md"
    )
    assert "不存在" in prd, (
        "PRD 末尾摘要应声明 docs/design/DESIGN.md 不存在"
    )


def test_prd_declares_no_design_extensions() -> None:
    """PRD 摘要中「待扩展 DESIGN §5」项应为无。"""
    prd = _read_prd()
    assert "待扩展 DESIGN" in prd, (
        "PRD 应包含「待扩展 DESIGN §5」声明"
    )
    # The summary must state the design-extension section is empty.
    summary_marker = "待扩展 DESIGN"
    idx = prd.find(summary_marker)
    following = prd[idx: idx + 80]
    assert "无" in following, (
        "PRD「待扩展 DESIGN §5」应声明为「无」（沿用现有组件）"
    )
