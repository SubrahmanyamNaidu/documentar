import os
import json

def get_repo_structure(repo_path, exclude_dirs={".git", ".github", "node_modules"}, exclude_files={".gitignore"}):
    repo_dict = {}

    for root, dirs, files in os.walk(repo_path, topdown=False):  # Bottom-Up Traversal
        relative_path = os.path.relpath(root, repo_path)

        # Skip paths containing .git or other excluded directories
        if any(excluded in root.split(os.sep) for excluded in exclude_dirs):
            continue

        # Remove excluded directories from traversal
        dirs[:] = [d for d in dirs if d not in exclude_dirs and not d.startswith(".")]

        repo_dict[relative_path] = {
            "path": root,
            "sub-folders": {d: {"path": os.path.join(root, d)} for d in dirs},
            "files": [
                {"filename": f, "path": os.path.join(root, f)}
                for f in files if f not in exclude_files and not f.startswith(".")
            ]
        }

    return repo_dict

repo_path = "./angular-ecommerce-app"
repo_structure = get_repo_structure(repo_path)

# Save as JSON
with open("repo_structure.json", "w") as f:
    json.dump(repo_structure, f, indent=4)

print("✅ Repo structure saved! `.git` and unwanted files are completely removed.")
