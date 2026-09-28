import subprocess
import os
from pathlib import Path

def authenticate():
    subprocess.run(
    ["docker", "login", "-u", os.environ["DOCKER_USERNAME"],
    "--password-stdin"],
    input=os.environ["DOCKER_PASSWORD"],
    text=True,
    check=True
)

def build_image(source_directory: Path, image_name: str):
    subprocess.run(["docker","build","-t",image_name,str(source_directory)],check=True)
    
def push_image(image_name: str, registry_image: str):
    subprocess.run(
        ["docker", "tag", image_name, registry_image],
        check=True
    )
    subprocess.run(
        ["docker", "push", registry_image],
        check=True
    )