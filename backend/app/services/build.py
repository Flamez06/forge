from pathlib import Path

from .git import clone_repository
from .docker import build_image, push_image

def build_application(repository_url: str, commit_sha: str, build_directory: Path, application_id: int, registry_username: str):
    resolved_sha = clone_repository(
        repository_url,
        build_directory,
        commit_sha
    )
    image_name = f"forge/app-{application_id}:{resolved_sha}"
    registry_image = f"{registry_username}/forge-app:{resolved_sha}"
    build_image(
        build_directory,
        image_name
    )
    push_image(image_name, registry_image)
    return resolved_sha, registry_image