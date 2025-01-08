import os
import sys
from pathlib import Path

# Get the absolute path to the project root directory
project_root = Path(__file__).parent.parent

# Add the src directory to the Python path
sys.path.append(str(project_root))
sys.path.append(str(project_root / "src"))
