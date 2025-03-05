# Generate Documentation with Backtracking and Memorization using GenAI  

```
So, What I am thinking is when an user give the repo link and a brief description about the repo. Then we start our steps:
step1: get the file structure of the repo
Ex: if it is a react project repo on ecommerce  then structure will be:
xyz-ecommerce/
     node_modules
     public
     package.json
     index.html
     src/
       App.jsx
       App.css
       assets
        components/
            Navbar.jsx
            Navbar.css
            ItemCard.jsx
            ItemCard.css
            .... and so on
        pages/
             Home.jsx
              Home.css
              Products.jsx
              Products.css
              .... and so on
 
Step2: creating an json file which will have the paths and what it describes start from the leaf node (file) so that the parents nodes will make more sense because if we start with the leaf node and move we will have knowledge of what the data present inside so that makes it specific description than getting a general descripts in top-down approach.
example:
{
xyz-ecommerce:{
xyz-ecommerce-path: /  ,
description: <will be updated at the last in the bottom up approach because root node description>
sub-folders:{
  sub-folder1-path: /sub-folder1,
  description:< will be updated after all the childes completed>,
 sub-sub-folders:{},
files:[{filename:<name of the file with extension>,description: "description of the file"},{filename:<name of the file with extension>,description: "description of the file"},.. and so on]
}
}
files:[{filename:<name of the file with extension>,description: "description of the file"},{filename:<name of the file with extension>,description: "description of the file"},.. and so on]
}
```

## Example output Should looks like
```
json

{
  "xyz-ecommerce": {
    "xyz-ecommerce-path": "/",
    "description": "A full-stack eCommerce web application built using React, with a modular component-based structure.",
    "sub-folders": {
      "src": {
        "src-path": "/src",
        "description": "Contains the main React source code, including components, pages, and assets.",
        "sub-folders": {
          "components": {
            "components-path": "/src/components",
            "description": "Reusable UI components for the application.",
            "files": [
              {
                "filename": "Navbar.jsx",
                "description": "Navigation bar component that includes links to Home, Products, and Cart."
              },
              {
                "filename": "ItemCard.jsx",
                "description": "A card UI component displaying individual product details."
              }
            ]
          },
          "pages": {
            "pages-path": "/src/pages",
            "description": "Contains page-level React components representing different views in the application.",
            "files": [
              {
                "filename": "Home.jsx",
                "description": "Homepage component with featured products and promotional banners."
              },
              {
                "filename": "Products.jsx",
                "description": "Displays a list of products available in the eCommerce store."
              }
            ]
          }
        }
      }
    },
    "files": [
      {
        "filename": "package.json",
        "description": "Defines project dependencies, scripts, and metadata."
      },
      {
        "filename": "index.html",
        "description": "The main HTML entry point for the React application."
      }
    ]
  }
}


```


```
ChatGpt Insides

Step 1: Fetch Repository Structure

Use GitHub API (if the repo is hosted on GitHub) or local directory traversal (os.walk in Python) to get the structure.
Identify file types to determine what kind of content they hold (code, assets, configs, etc.).
Step 2: Generate Descriptions for Each File

GenAI-powered analysis for meaningful descriptions.
Use LLM models (GPT, Gemini, or Claude) to summarize each file's purpose.
For code files, extract:
Main functions/classes
Comments & Docstrings
API endpoints (if applicable)
For non-code files, determine their role (e.g., README.md, package.json, Dockerfile, etc.).
Step 3: Build JSON in Bottom-Up Manner

Start from files, generate descriptions.
Move up to directories, summarizing based on their child nodes.
The root directory will get a holistic description based on all its contents.



Let's break it down into implementation steps in Python. We'll use:

GitHub API / Local File System Traversal
LLM (GPT or Claude) for generating descriptions
Bottom-Up JSON Construction
Final Documentation Output (JSON or Markdown)
Step 1: Get Repository File Structure
If it's a local repo, we use os.walk().
If it's a GitHub repo, we use the GitHub API to fetch the file tree.
Step 2: Generate File Descriptions
Use GPT/Claude API to summarize files.
Identify file types (JSX, Python, JSON, Markdown, etc.).
Extract function names, class names, and docstrings for better descriptions.
Step 3: Bottom-Up JSON Construction
Traverse the tree from files (leaf nodes) upwards.
Store descriptions first at file level, then directory level.
Step 4: Generate Final Documentation
Save as JSON for structured data.
Optionally, convert to Markdown for human-readable documentation.


```

### 1. Get Repository File Structure
```
import os
import json

def get_repo_structure(repo_path):
    repo_dict = {}

    for root, dirs, files in os.walk(repo_path, topdown=False):  # Bottom-Up Traversal
        relative_path = os.path.relpath(root, repo_path)
        repo_dict[relative_path] = {
            "path": root,
            "sub-folders": {d: {"path": os.path.join(root, d)} for d in dirs},
            "files": [{"filename": f, "path": os.path.join(root, f)} for f in files]
        }

    return repo_dict

```

### 2. Generate Descriptions using LLM (OpenAI API)

```
import openai

openai.api_key = "your-api-key"

def generate_description(file_path, content=None):
    prompt = f"Describe the purpose of this file in a software project:\nFile: {file_path}\n"
    
    if content:
        prompt += f"Content: ```{content[:500]}```\n"  # Only first 500 chars to avoid cost

    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}]
    )

    return response["choices"][0]["message"]["content"].strip()

```

### 3. Process and Construct JSON (Bottom-Up Approach)
```
def build_json_with_descriptions(repo_dict):
    for key, value in repo_dict.items():
        for file in value.get("files", []):
            with open(file["path"], "r", encoding="utf-8", errors="ignore") as f:
                file_content = f.read()
                file["description"] = generate_description(file["filename"], file_content)
        
        value["description"] = "Contains " + ", ".join(f["filename"] for f in value.get("files", []))

    return repo_dict
 
```

### 4. Convert JSON to Markdown for Readable Docs
```
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

```

### Final Execution
```
repo_path = "path-to-your-repo"
repo_structure = get_repo_structure(repo_path)
repo_with_descriptions = build_json_with_descriptions(repo_structure)

# Save as JSON
with open("repo_documentation.json", "w") as f:
    json.dump(repo_with_descriptions, f, indent=4)

# Save as Markdown
md_content = json_to_markdown(repo_with_descriptions)
with open("repo_documentation.md", "w") as f:
    f.write(md_content)

print("📄 Documentation Generated Successfully!")

```