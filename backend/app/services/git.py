import subprocess
from pathlib import Path

def clone_repository(repository_url: str,destination: Path,commit_sha: str):
    subprocess.run(["git", "clone", repository_url, str(destination)],check=True)
    subprocess.run(["git", "-C", str(destination), "checkout", commit_sha],check=True)
    
    result = subprocess.run(
        ["git", "-C", str(destination), "rev-parse", "HEAD"],
        check=True,
        capture_output=True,
        text=True
    )
    return result.stdout.strip()
    
    
    
