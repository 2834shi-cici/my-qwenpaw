"""Tests for Docker deployment brand replacement (issue #4).

Verifies that Docker deployment files use the ``cici-workbench`` brand
instead of the upstream ``QwenPaw`` brand, while keeping internal
identifiers (``QWENPAW_*`` env vars, ``src/qwenpaw/`` paths, etc.)
intact per the rebrand PRD.

Seam (per issue PRD 绑定): ``docker-compose.yml`` + ``deploy/Dockerfile``
+ ``deploy/entrypoint.sh``.
"""

from __future__ import annotations

import shutil
import subprocess
from pathlib import Path

import pytest
import yaml

REPO_ROOT = Path(__file__).resolve().parents[3]
COMPOSE_FILE = REPO_ROOT / "docker-compose.yml"
DOCKERFILE = REPO_ROOT / "deploy" / "Dockerfile"
ENTRYPOINT = REPO_ROOT / "deploy" / "entrypoint.sh"
SUPERVISORD = REPO_ROOT / "deploy" / "config" / "supervisord.conf.template"

# Internal identifiers that are intentionally kept (lowercase / uppercase,
# not the capitalized brand display name "QwenPaw").
INTERNAL_PATTERNS = (
    "io.qwenpaw",          # Docker LABEL namespace
    "/opt/qwenpaw-python", # internal python runtime path
    "src/qwenpaw",         # internal python package path
    "qwenpawmail",         # internal mcp package name
    "QWENPAW_",            # environment variable prefix
)


def _read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def _brand_display_hits(text: str) -> list[str]:
    """Return lines containing the user-visible brand display name 'QwenPaw'.

    Internal identifiers (lowercase ``qwenpaw`` paths, uppercase
    ``QWENPAW_`` env vars) are excluded because they are not the
    capitalized brand display name.
    """
    hits = []
    for line in text.splitlines():
        if "QwenPaw" in line:
            hits.append(line.strip())
    return hits


# ---------------------------------------------------------------------------
# docker-compose.yml
# ---------------------------------------------------------------------------

@pytest.fixture(scope="module")
def compose() -> dict:
    with COMPOSE_FILE.open(encoding="utf-8") as f:
        return yaml.safe_load(f)


def test_compose_image_is_cici_workbench(compose: dict) -> None:
    """Acceptance criterion 1: image is cici/cici-workbench:latest."""
    services = compose["services"]
    assert "cici-workbench" in services
    assert services["cici-workbench"]["image"] == "cici/cici-workbench:latest"


def test_compose_volumes_are_cici_workbench(compose: dict) -> None:
    """Acceptance criterion 2: volume names are cici-workbench-*."""
    volumes = compose.get("volumes", {})
    expected = {"cici-workbench-data", "cici-workbench-secrets", "cici-workbench-backups"}
    assert set(volumes.keys()) == expected
    for name in expected:
        assert volumes[name]["name"] == name


def test_compose_service_and_container_name(compose: dict) -> None:
    """Acceptance criterion 3: service name and container_name are cici-workbench."""
    services = compose["services"]
    assert "cici-workbench" in services
    assert services["cici-workbench"]["container_name"] == "cici-workbench"


# ---------------------------------------------------------------------------
# deploy/Dockerfile & deploy/entrypoint.sh — string scan seam
# ---------------------------------------------------------------------------

def test_dockerfile_has_no_user_visible_qwenpaw_brand() -> None:
    """Acceptance criterion 4: Dockerfile has no 'QwenPaw' brand display name.

    Internal lowercase/uppercase identifiers (paths, env vars, labels) are
    allowed; only the capitalized brand display name must be absent.
    """
    text = _read(DOCKERFILE)
    hits = _brand_display_hits(text)
    assert not hits, (
        "Dockerfile still contains user-visible 'QwenPaw' brand display name:\n"
        + "\n".join(hits)
    )


def test_entrypoint_has_no_user_visible_qwenpaw_brand() -> None:
    """Acceptance criterion 4: entrypoint.sh has no 'QwenPaw' brand display name."""
    text = _read(ENTRYPOINT)
    hits = _brand_display_hits(text)
    assert not hits, (
        "entrypoint.sh still contains user-visible 'QwenPaw' brand display name:\n"
        + "\n".join(hits)
    )


def test_dockerfile_keeps_internal_identifiers() -> None:
    """Internal identifiers (paths, env vars, labels) must remain intact."""
    text = _read(DOCKERFILE)
    for pattern in INTERNAL_PATTERNS:
        assert pattern in text, f"Internal identifier '{pattern}' was removed from Dockerfile"


def test_entrypoint_uses_cici_init_command() -> None:
    """entrypoint.sh must use the 'cici' CLI command for initialization."""
    text = _read(ENTRYPOINT)
    assert "cici init" in text
    assert "qwenpaw init" not in text


# ---------------------------------------------------------------------------
# supervisord.conf.template — CLI command consistency
# ---------------------------------------------------------------------------

def test_supervisord_uses_cici_app_command() -> None:
    """The app service must start via the 'cici' CLI command (not 'qwenpaw').

    The ``qwenpaw`` console script no longer exists (only ``cici`` and
    ``copaw`` are defined in pyproject.toml), so ``qwenpaw app`` would fail
    to start the container.
    """
    text = _read(SUPERVISORD)
    assert "cici app" in text
    assert "qwenpaw app" not in text


# ---------------------------------------------------------------------------
# docker compose config — end-to-end validation
# ---------------------------------------------------------------------------

def test_docker_compose_config_has_no_qwenpaw() -> None:
    """Acceptance criterion 5: ``docker compose config`` output has no 'qwenpaw'.

    Skipped when docker is not available.
    """
    if shutil.which("docker") is None:
        pytest.skip("docker not available")
    result = subprocess.run(
        ["docker", "compose", "-f", str(COMPOSE_FILE), "config"],
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, (
        f"docker compose config failed:\n{result.stderr}"
    )
    output = result.stdout.lower()
    assert "qwenpaw" not in output, (
        "docker compose config output still contains 'qwenpaw'"
    )
