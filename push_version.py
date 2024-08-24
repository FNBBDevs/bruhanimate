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

def push_init():
    init_contents = None
    new_line = None

    with open("bruhanimate/__init__.py", "r") as file:
        init_contents = file.readlines()
        
    for idx, line in enumerate(init_contents):
        if line.startswith("__version__"):
            version_raw = line.split("=")[1].strip()[1:-1].split(".")
            a, b, c = (int(v) for v in version_raw)
            old_version = f"{a}.{b}.{c}"
            new_version = f"{a}.{b}.{c+1}"
            print(f"__init__.py: {old_version} --> {new_version}")
            new_line = f"__version__ = \"{new_version}\"\n"
            init_contents[idx] = new_line
            break

    with open("bruhanimate/__init__.py", "w") as file:
        file.writelines(init_contents)

def push_setup():
    setup_contents = None
    new_line = None

    with open("setup.py", "r") as file:
        setup_contents = file.readlines()
        
    for idx, line in enumerate(setup_contents):
        if line.startswith("VERSION"):
            
            version_raw = line.split("=")[1].strip()[1:-1].split(".")
            a, b, c = (int(v) for v in version_raw)
            old_version = f"{a}.{b}.{c}"
            new_version = f"{a}.{b}.{c+1}"
            print(f"setup.py: {old_version} --> {new_version}")
            new_line = f"VERSION = \"{new_version}\"\n"
            setup_contents[idx] = new_line
            break

    with open("setup.py", "w") as file:
        file.writelines(setup_contents)


if __name__ == "__main__":
    push_init()
    push_setup()