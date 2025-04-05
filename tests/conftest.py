import sys
import os

# Add the project root directory (one level up from 'tests') to the Python path
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if project_root not in sys.path:
    # Insert at the beginning to ensure it's checked first
    sys.path.insert(0, project_root)

# Also add the backend directory so relative imports work
backend_dir = os.path.join(project_root, "backend")
if backend_dir not in sys.path:
    sys.path.insert(0, backend_dir)
    
print(f"--- Added to sys.path by conftest.py: {project_root} ---") # Optional: for debugging