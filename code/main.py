import os
import json
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
load_dotenv()

def get_repo_structure(repo_path, exclude_dirs={".git", ".github", "node_modules"}, exclude_files={".gitignore",".gif",".png",".jpg",".jpeg"}):
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





def generate_description(file_path, content=None):
    prompt = f"Describe the purpose of this file in a software project:\nFile: {file_path}\n"
    
    if content:
        prompt += f"Content: ```{content[:500]}```\n"  # Only first 500 chars to avoid cost

    chat = ChatOpenAI(model="gpt-4o-mini")
    response=chat.invoke(("user", prompt))
    print(response.content)
    return response.content


def build_json_with_descriptions(repo_dict):
    for key, value in repo_dict.items():
        for file in value.get("files", []):
            with open(file["path"], "r", encoding="utf-8", errors="ignore") as f:
                file_content = f.read()
                file["description"] = generate_description(file["filename"], file_content)
        
        value["description"] = "Contains " + ", ".join(f["filename"] for f in value.get("files", []))

    return repo_dict



def json_to_markdown(repo_dict):
    md = "# Repository Documentation\n\n"

    for folder, data in repo_dict.items():
        md += f"## 📁 {folder}\n"
        md += f"- **Path:** `{data['path']}`\n"
        md += f"- **Description:** {data['description']}\n\n"

        for file in data.get("files", []):
            md += f"### 📄 {file['filename']}\n"
            md += f"- **Path:** `{file['path']}`\n"
            md += f"- **Description:** {file.get('description', 'No description available.')}\n\n"

    return md

if __name__=="__main__":
    repo_path = "./angular-ecommerce-app"
    repo_structure = get_repo_structure(repo_path)
    repo_with_descriptions = build_json_with_descriptions(repo_structure)

    # Save as JSON
    with open("repo_documentation.json", "w",encoding="utf-8") as f:
        json.dump(repo_with_descriptions, f,ensure_ascii=False, indent=4)

    # Save as Markdown
    md_content = json_to_markdown(repo_with_descriptions)
    with open("repo_documentation.md", "w",encoding="utf-8") as f:
        f.write(md_content)

    print("📄 Documentation Generated Successfully!")
