# This file version is for Unix-like OS (Linux, macOS)

import os
import json
import pandas as pd
from dotenv import load_dotenv, set_key
from dataclasses import dataclass
from typing import List, Dict, Any

@dataclass
class ProjectConfig:
    """Base configuration class handling common project properties"""
    project_dir: str = os.path.dirname(__file__)
    project_name: str = os.path.basename(project_dir).strip()
    
    def __post_init__(self):
        """Initialize derived properties after dataclass setup"""
        self.project_env = os.path.join(self.project_dir, 'project.env')
        self.project_csv = os.path.join(self.project_dir, 'project.csv')
        self._setup_env_vars()
        
    def _setup_env_vars(self):
        """Initialize core environment variables"""
        os.environ.update({
            'ProjectName': self.project_name,
            'ProjectDir': self.project_dir,
            'ProjectEnv': self.project_env,
            'ProjectCsv': self.project_csv
        })
        
    def save_config(self):
        """Persist configuration to environment file"""
        load_dotenv(self.project_env)
        for key in ['ProjectName', 'ProjectDir', 'ProjectEnv', 'ProjectCsv']:
            set_key(self.project_env, key, os.environ[key])

class VSCodeConfigurator(ProjectConfig):
    """Handles VS Code workspace configuration"""
    def __init__(self):
        super().__init__()
        self.subfolders = [f.path for f in os.scandir(self.project_dir) if f.is_dir()]
        self.workspace_file = None
        # Define venv paths for Unix-like OS
        self.venv_bin_dir = os.path.join(self.project_dir, '.venv', 'bin')
        self.python_executable = os.path.join(self.venv_bin_dir, 'python')
        self.pytest_executable = os.path.join(self.venv_bin_dir, 'pytest')
        
    def configure_python_path(self):
        """Configure Python module search path"""
        os.environ['PYTHONPATH'] = self.project_dir
        set_key(self.project_env, "PYTHONPATH", self.project_dir)
        
    def create_debug_config(self) -> Dict[str, Any]:
        """Generate debug configuration for VS Code"""
        return {
            "name": f"Python: Module: {self.project_name}",
            "type": "debugpy",
            "request": "launch",
            "module": self.project_name,
            "env": {"PYTHONPATH": self.project_dir},
            "console": "integratedTerminal"
        }
    
    def create_my_first_tasks_config(self) -> Dict[str, Any]:
        """Generate a dummy tasks configuration for VS Code"""
        return {
                "label": "My Dummy Task",
                "command": "echo hello World",
                "type": "shell",
                "args": [],
                "problemMatcher": [
                    "$tsc"
                ],
                "presentation": {
                    "reveal": "always"
                },
                "group": "build"
        }
        
    def build_workspace(self):
        """Create and configure VS Code workspace file"""
        config = {
            "folders": [],
            "settings": {
                "terminal.integrated.env.windows": {"PATH": "${env:anaconda_environment};"},
                # Add terminal.integrated.env.linux for Unix-like OS
                "terminal.integrated.env.linux": {
                    "PATH": f"{self.venv_bin_dir}:${{env:PATH}}"
                },
                "terminal.integrated.cwd": self.project_dir,
                "workbench.editor.languageDetection": True,
                "files.autoSave": "afterDelay",
                "diffEditor.renderSideBySide": True,
                "breadcrumbs.enabled": True,
                "editor.minimap.enabled": True,
                # Set default interpreter path to venv python
                "python.defaultInterpreterPath": self.python_executable,
                "python.envFile": self.project_env,
                "python.experiments.enabled": True,
                "python.experiments.optInto": [],
                "python.experiments.optOutFrom": [],
                "python.globalModuleInstallation": False,
                "python.analysis.aiCodeActions": {},
                "python.analysis.extraPaths": [
                    os.path.join(self.project_dir, 'core'),
                    os.path.join(self.project_dir, 'features'),
                    os.path.join(self.project_dir, 'core/tests')
                ],
                # Set pytest path to venv pytest
                "python.testing.pytestPath": self.pytest_executable,
                "python.testing.pytestEnabled": True,
                "python.testing.unittestEnabled": False,
                "python.testing.pytestArgs": [  
                    "--maxfail=3", 
                    "-v",  
                    "--tb=short",
                    "-k", "run_test"
                ],
                "projectManager": {
                    "any": {"baseFolders": [self.project_dir]},
                    "git": {"baseFolders": [self.project_dir]},
                    "vscode": {"baseFolders": [self.project_dir]},
                    "tags": [
                        "Integration Project",
                        "Data Science",
                        "Web Development",
                        "Google SDK Python",
                        "Databases", 
                        "Industrial Automation",
                        "Industrial Control",
                        "Industrial Instrumentation",
                        "Industrial Application",
                        "IOT"
                        ]
                }
            },
            "launch": {"configurations": []},
            "tasks": {"version": "2.0.0", "tasks": []}
        }
        
        # Add debug configuration
        debug_config = json.dumps(self.create_debug_config())
        config["launch"]["configurations"].append(json.loads(debug_config))
        # Add a task configuration
        task_config = json.dumps(self.create_my_first_tasks_config())
        config["tasks"]["tasks"].append(json.loads(task_config))
        
        # Add folder paths
        config["folders"] = [{"path": os.path.basename(f)} for f in self.subfolders]
        
        # Save workspace file
        vscode_dir = os.path.join(self.project_dir, '.vscode')
        os.makedirs(vscode_dir, exist_ok=True)
        
        self.workspace_file = os.path.join(vscode_dir, f'{self.project_name}.code-workspace')
        with open(self.workspace_file, 'w') as f:
            json.dump(config, f, indent=4)
            
        os.environ['vscode_workspace'] = self.workspace_file
        set_key(self.project_env, "vscode_workspace", self.workspace_file)

class CommentHandler(ProjectConfig):
    """Handles insertion of documentation comments in workspace file"""
    COMMENT_TEMPLATE = {
        "settings": "// Controls the settings that apply to all profiles",
        "launch": "// Add debugging configurations to project",
        "tasks": "// Automate project tasks"
    }

    def __init__(self):
        super().__init__()
        self.workspace_file = os.getenv("vscode_workspace")

    def add_comments(self):
        """Insert documentation comments at appropriate locations in workspace file"""
        try:
            with open(self.workspace_file, 'r+', encoding='utf-8') as f:
                content = f.read()
                
                # Insert comments before each section
                for section, comment in self.COMMENT_TEMPLATE.items():
                    insert_pos = content.find(f'"{section}":')
                    if insert_pos != -1:
                        content = content[:insert_pos] + f'// {comment}\n' + content[insert_pos:]

                # Write updated content back to file
                f.seek(0)
                f.write(content)
                f.truncate()

        except (OSError, FileNotFoundError) as e:
            print(f"Error updating workspace comments: {str(e)}")

class ProjectMetadataHandler(ProjectConfig):
    """Handles project metadata generation and storage"""
    METADATA_TEMPLATE = {
        "ProjectName": ["CodeProjectTemplate"],
        "LinkProjectRepo": ["https://github.com/Wema-Digital/code-project-templates"],
        "ImageName": ["CodeProjectTemplate.png"],
        "LinkImageRepo": ["https://github.com/Wema-Digital/code-project-templates/docs/media"],
        "Category": ["Coding-Project-Template"],
        "ProjectAbout": ["Windows and Linux, vscode-optimized project template and tools emphasizing maintainability and collaboration."]
    }

    def __init__(self):
        super().__init__()
        self.df = pd.DataFrame(self.METADATA_TEMPLATE)

    def generate_metadata(self):
        """Generate and save project metadata to CSV file"""
        try:
            self.df.to_csv(self.project_csv, index=False)
            set_key(self.project_env, "ProjectCsv", self.project_csv)
        except (FileNotFoundError, PermissionError) as e:
            print(f"Metadata generation failed: {str(e)}")

class ProjectDataHandler(ProjectConfig):
    """Handles project data generation and storage for docs folder"""
    DATA_TEMPLATE = {
        "Attribute": [
            "ProjectName", 
            "ProjectRepo", 
            "ProjectAbout", 
            "WhyProject", 
            "medialink_1", 
            "medialink_2", 
            "medialink_3", 
            "feature_1", 
            "feature_2", 
            "feature_3", 
            "email",
            "LicenceName"],
        "Value": [
            "CodeProjectTemplate", 
            "https://github.com/Wema-Digital/code-project-templates", 
            "A well-structured, VSCode-optimized Python and javascript project template. Designed to be intuitive and easy to navigate, promoting better maintainability and seamless collaboration.", 
            "This project setup enables developers to efficiently create a VSCode workspace, integrating project data with documentation and GitHub attributes.", 
            "https://github.com/Wema-Digital/code-project-templates/docs/media/screenshot-1.png", 
            "https://github.com/Wema-Digital/code-project-templates/docs/media/screenshot-2.png", 
            "https://github.com/Wema-Digital/code-project-templates/docs/media/screenshot-3.png", 
            "Seamless Exploration", 
            "Maintains clear separation of concerns.", 
            "Bilingual documentation (Spanish and English).", 
            "wema.digital.mail@gmail.com",
            "MIT license"]
    }
    def __init__(self):
        super().__init__()
        self.df = pd.DataFrame(self.DATA_TEMPLATE)
        self.en_data_csv_path = os.path.join(self.project_dir, 'docs/readme_en/data.csv')
        self.es_data_csv_path = os.path.join(self.project_dir, 'docs/readme_es/data.csv')

    def generate_data(self):
        """Generate and save project data to CSV file"""
        try:
            self.df.to_csv(self.en_data_csv_path, index=False)
            self.df.to_csv(self.es_data_csv_path, index=False)
        except (FileNotFoundError, PermissionError) as e:
            print(f"Data generation failed: {str(e)}")



if __name__ == "__main__":
    # Initialize configuration
    config = ProjectConfig()
    config.save_config()

    # Configure VS Code workspace
    vs_config = VSCodeConfigurator()
    vs_config.configure_python_path()
    vs_config.build_workspace()

    # Add documentation comments
    comment_handler = CommentHandler()
    comment_handler.add_comments()

    # Generate project metadata
    metadata_handler = ProjectMetadataHandler()
    metadata_handler.generate_metadata()

    # Generate project data
    data_handler = ProjectDataHandler()
    data_handler.generate_data()
