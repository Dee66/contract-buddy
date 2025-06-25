from pathlib import Path
import nox
from utils import ensure_bootstrap, nox_logger


@nox.session
def docker_compose_up(session):
    """Spin up all services using Docker Compose (local integration test)."""
    ensure_bootstrap(session)
    if not Path("docker-compose.yml").exists():
        return
    nox_logger.info("🟦 NOTE: Starting Docker Compose services.")
    session.run("docker-compose", "up", "-d", external=True)


@nox.session
def docker_compose_down(session):
    """Tear down Docker Compose services."""
    ensure_bootstrap(session)
    if not Path("docker-compose.yml").exists():
        return
    nox_logger.info("🟦 NOTE: Stopping Docker Compose services.")
    session.run("docker-compose", "down", external=True)


@nox.session
def docker_build_all(session):
    """
    Build all Docker images for all environments, skipping if image exists
    and is up-to-date with its Dockerfile/context hash.
    🟨 CAUTION: Fails fast if any Docker build fails, logs error output for diagnosis.
    🟦 NOTE: Optimized for minimal rebuilds and bandwidth usage.
    🟪 ARCH: Ensures build context and environment match manual builds for reproducibility.
    """
    ensure_bootstrap(session)
    import hashlib
    import os
    import subprocess

    nox_logger.info(f"🟦 NOTE: Nox working directory: {os.getcwd()}")

    def context_hash(dockerfile, context_dir="."):
        sha = hashlib.sha256()
        dockerfile_path = Path(dockerfile)
        if not dockerfile_path.exists():
            return None
        sha.update(dockerfile_path.read_bytes())
        dockerignore = Path(context_dir) / ".dockerignore"
        ignore_patterns = set()
        if dockerignore.exists():
            for line in dockerignore.read_text().splitlines():
                line = line.strip()
                if line and not line.startswith("#"):
                    ignore_patterns.add(line)
        for root, _, files in os.walk(context_dir):
            for fname in sorted(files):
                fpath = Path(root) / fname
                rel_path = fpath.relative_to(context_dir)
                if any(rel_path.match(pattern) for pattern in ignore_patterns):
                    continue
                sha.update(str(rel_path).encode())
                sha.update(fpath.read_bytes())
        return sha.hexdigest()[:12]

    project_root = Path(__file__).parent.resolve()
    os.chdir(project_root)
    nox_logger.info(
        f"🟦 NOTE: Changed working directory to project root: {os.getcwd()}"
    )

    dockerfiles = [
        ("Dockerfile.api", "codecraft-ai-api"),
        ("Dockerfile.ingestion", "codecraft-ai-ingestion"),
    ]
    for dockerfile, base_tag in dockerfiles:
        if not Path(dockerfile).exists():
            nox_logger.warning(
                f"🟨 CAUTION: {dockerfile} not found, skipping build for {base_tag}."
            )
            continue
        hash_tag = context_hash(dockerfile)
        if not hash_tag:
            nox_logger.error(
                f"🟥 CRITICAL: Could not compute context hash for {dockerfile}."
            )
            session.error(
                f"🟥 CRITICAL: Could not compute context hash for {dockerfile}."
            )
        full_tag = f"{base_tag}:{hash_tag}"
        result = session.run(
            "docker",
            "images",
            "-q",
            full_tag,
            silent=True,
            external=True,
            success_codes=[0, 1],
        )
        if result and result.strip():
            nox_logger.info(
                f"Docker image '{full_tag}' already exists, skipping build."
            )
            continue
        nox_logger.info(
            f"🟦 NOTE: Building Docker image '{full_tag}' from {dockerfile}."
        )
        try:
            build_cmd = [
                "docker",
                "build",
                "--progress=plain",
                "--build-arg",
                "BUILDKIT_INLINE_CACHE=1",
                "-f",
                dockerfile,
                "-t",
                full_tag,
                ".",
            ]
            nox_logger.info(f"🟦 NOTE: Running: {' '.join(build_cmd)}")
            result = subprocess.run(
                build_cmd,
                cwd=os.getcwd(),
                env=os.environ,
                text=True,
                capture_output=False,
                check=False,
            )
            if result.returncode != 0:
                nox_logger.error(
                    f"🟥 CRITICAL: Docker build failed for {dockerfile} ({full_tag}):\n"
                    f"Exit code: {result.returncode}\n"
                    "🟨 CAUTION: See the full Docker build output above for the real error."
                )
                session.error(
                    f"🟥 CRITICAL: Docker build failed for {dockerfile} ({full_tag}):\n"
                    f"Exit code: {result.returncode}\n"
                    "🟨 CAUTION: See the full Docker build output above for the real error."
                )
        except Exception as e:
            nox_logger.error(
                f"🟥 CRITICAL: Docker build failed for {dockerfile} ({full_tag}): {e}\n"
                "🟨 CAUTION: Check the Docker build output above for details.",
                exc_info=True,
            )
            session.error(
                f"🟥 CRITICAL: Docker build failed for {dockerfile} ({full_tag}): {e}\n"
                "🟨 CAUTION: Check the Docker build output above for details."
            )


@nox.session
def docker_clean(session):
    """Remove all dangling Docker images and stopped containers."""
    ensure_bootstrap(session)
    session.run("docker", "system", "prune", "-f", external=True)
