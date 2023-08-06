import os
import platform
import subprocess
import sys
from click_configfile import ConfigFileReader, Param, SectionSchema
from click_configfile import matches_section


def run_command(command):
    return subprocess.run(
        command,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )


def get_system():
    architecture, _ = platform.architecture()
    os_name = ""
    os_version = ""
    if os.path.exists("/etc/os-release"):
        with open("/etc/os-release") as f:
            for line in f:
                name = line.split("=")[0]
                value = line.split("=")[1].strip()
                if name == "PRETTY_NAME":
                    os_name = value.rstrip('"').lstrip('"')
                elif name == "VERSION_CODENAME":
                    os_version = value
    return {
        "os": platform.system(),
        "os_release": platform.release(),
        "os_name": os_name,
        "os_version": os_version,
        "machine": platform.machine(),
        "architecture": architecture,
    }


def get_packages():
    all_packages = {}
    for pkgmgr in ["apt", "brew", "poetry"]:
        which_cmd = run_command(["which", pkgmgr])
        if which_cmd.returncode < 1:
            if pkgmgr == "apt":
                pkgs = run_command(["apt-mark", "showmanual"])
            if pkgmgr == "brew":
                pkgs = run_command(["brew", "leaves"])
            if pkgmgr == "poetry":
                pkgs = run_command(["poetry", "show"])
            all_packages[pkgmgr] = pkgs.stdout.decode().splitlines()
    return all_packages


class LocalEnv:
    def __init__(self):
        self.system = get_system()
        self.packages = None
        pass

    def get(self):
        if self.packages is None:
            self.packages = get_packages()

        return {
            "system": self.system,
            "packages": self.packages,
        }


le = LocalEnv()


class ConfigSectionSchema(object):
    """Describes all config sections of this configuration file."""

    @matches_section("profile")
    class Profile(SectionSchema):
        name = Param(type=str)
        email = Param(type=str)
        git_provider = Param(type=str)
        config_repo = Param(type=str)


class ConfigFileProcessor(ConfigFileReader):
    home = os.getenv("HOME")
    config_files = [f"{home}/.lfntrc"]
    config_section_schemas = [
        ConfigSectionSchema.Profile,
    ]


CONTEXT_SETTINGS = dict(default_map=ConfigFileProcessor.read_config())


class DigestiveSystem:
    def __init__(self):
        pass

    def get(self):
        return CONTEXT_SETTINGS

    def dump(self):
        return {
            "profile": CONTEXT_SETTINGS["default_map"],
            "environment": le.get(),
        }
