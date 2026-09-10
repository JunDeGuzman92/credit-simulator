"""Production entrypoint: start uvicorn on the port the platform assigns.

Railway/Render inject a PORT environment variable. Reading it in Python
avoids any shell-expansion issues with "$PORT" in start commands.
"""

import os
import sys
from pathlib import Path

# Ensure the project root (the folder containing the "backend" package)
# is importable, regardless of where this script is invoked from.
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import uvicorn

if __name__ == "__main__":
    port = int(os.environ.get("PORT", "8000"))
    uvicorn.run(
        "backend.api:app",
        host="0.0.0.0",
        port=port,
    )
