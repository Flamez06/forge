from pathlib import Path
from backend.app.services.build import build_application

sha, image = build_application("https://github.com/datawire/hello-world",
    "3a82889", Path("./tests/test-build"), 2, "flamez06")

print(sha)
print(image)