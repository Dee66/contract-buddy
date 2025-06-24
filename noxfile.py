# 🟪 ARCH: Noxfile entrypoint for all sessions. Clean, production-grade import order and explicit imports.
import os
import sys

nox_dir = os.path.join(os.path.dirname(__file__), "nox")
if nox_dir not in sys.path:
    sys.path.insert(0, nox_dir)
