"""
Copyright 2023 Ethan Christensen

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""

import toml
from typing import Tuple

def increment_version(version: str) -> str:
    """Increment the patch version number."""
    major, minor, patch = map(int, version.split("."))
    return f"{major}.{minor}.{patch + 1}"

def read_file(file_path: str) -> Tuple[list, bool]:
    """Read the contents of a file."""
    try:
        with open(file_path, "r") as file:
            return file.readlines(), True
    except FileNotFoundError:
        print(f"Error: {file_path} not found.")
        return [], False
    except IOError as e:
        print(f"IOError for {file_path}: {e}")
        return [], False

def write_file(file_path: str, contents: list) -> bool:
    """Write contents to a file."""
    try:
        with open(file_path, "w") as file:
            file.writelines(contents)
        return True
    except IOError as e:
        print(f"IOError for {file_path}: {e}")
        return False

def update_version_string(version_line: str) -> Tuple[str, str]:
    """Extract and update the version in a version line."""
    old_version = version_line.split("=")[1].strip().strip('"')
    new_version = increment_version(old_version)
    return old_version, new_version

def update_init_file() -> None:
    """Update the version in the __init__.py file."""
    init_path = "bruhanimate/__init__.py"
    contents, success = read_file(init_path)
    if not success:
        return

    for idx, line in enumerate(contents):
        if line.startswith("__version__"):
            old_version, new_version = update_version_string(line)
            contents[idx] = f'__version__ = "{new_version}"\n'
            print(f"Updated __init__.py: {old_version} --> {new_version}")
            if write_file(init_path, contents):
                break

def update_pyproject_file() -> None:
    """Update the version in the pyproject.toml file."""
    pyproject_path = "pyproject.toml"
    try:
        with open(pyproject_path, "r") as file:
            pyproject_data = toml.load(file)
    except (FileNotFoundError, toml.TomlDecodeError) as e:
        print(f"Error reading {pyproject_path}: {e}")
        return

    old_version = pyproject_data['tool']['poetry'].get('version')
    if old_version:
        new_version = increment_version(old_version)
        pyproject_data['tool']['poetry']['version'] = new_version
        print(f"Updated pyproject.toml: {old_version} --> {new_version}")

        try:
            with open(pyproject_path, "w") as file:
                toml.dump(pyproject_data, file)
        except IOError as e:
            print(f"Error writing {pyproject_path}: {e}")

def main() -> None:
    """Main function to update version numbers."""
    update_init_file()
    update_pyproject_file()

if __name__ == "__main__":
    main()
