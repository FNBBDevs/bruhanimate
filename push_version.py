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