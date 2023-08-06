"""
Managing the cmd5 system installation and package distribution
"""
import os
import shutil
from distutils.dir_util import copy_tree
from pathlib import Path
from pprint import pprint

from cloudmesh.common.Shell import Shell
from cloudmesh.common.console import Console
from cloudmesh.common.util import banner
from cloudmesh.common.util import readfile
from cloudmesh.common.util import writefile
import textwrap
# from cloudmesh.sys.__version__ import version

version = "4.3.1"

class Command(object):
    """
    Class to generate cmd5 command templates
    """

    @classmethod
    def generate(cls, name):
        """
        Generate a command template with the given name
        :param name: the name of the command
        :return:
        """

        command = name
        package = "cloudmesh-{}".format(name)
        Command = name.capitalize()

        print(command)
        print(package)
        print(command)

        # os.system("rm -rf  cloudmesh-gregor")
        # noinspection PyUnusedLocal,PyBroadException
        try:
            shutil.rmtree("cloudmesh-bar")
        except:
            pass
        try:
            os.system("git clone https://github.com/cloudmesh/cloudmesh-bar")
        except Exception as e:  # noqa: F841
            pass

        if os.path.isdir(f"{package}/cloudmesh/{command}"):
            # noinspection PyPep8
            Console.error(
                f'The command directory "{package}/cloudmesh/{command}" already exists')
            return ""

        def generate_bumpversion(version="4.3.1", command="bar"):
            script = textwrap.dedent(f"""
            [bumpversion]
            current_version = {version}
            commit = True
            tag = False
            [bumpversion:file:VERSION]
            [bumpversion:file:./cloudmesh/{command}/__version__.py]
            [bumpversion:file:./cloudmesh/{command}/__init__.py]
            """) + \
            textwrap.dedent("""
            search = version: {current_version}
            replace = {new_version}""")
            return script

        def replace_in_file(filename, old_text, new_text):
            content = readfile(filename)
            content = content.replace(old_text, new_text)
            writefile(filename, content)

        def delete(path, pattern):
            files = Path(path).glob(pattern)
            for file in files:
                file.unlink()

        for pattern in ["*.zip",
                        "*.egg-info",
                        "*.eggs",
                        "build",
                        "dist",
                        ".tox",
                        "*.whl",
                        "**/__pycache__",
                        "**/*.pyc",
                        "**/*.pye"]:
            delete("./cloudmesh-bar/", pattern)

        #
        # os.system("cd cloudmesh-bar; make clean")
        #
        # clean = """
        # rm -rf cloudmesh-bar/*.zip
        # rm -rf cloudmesh-bar/*.egg-info
        # rm -rf cloudmesh-bar/*.eggs
        # rm -rf cloudmesh-bar/docs/build
        # rm -rf cloudmesh-bar/build
        # rm -rf cloudmesh-bar/dist
        # rm -rf cloudmesh-bar/.tox
        # rm -f cloudmesh-bar/*.whl
        # find cloudmesh-bar -type d -name __pycache__ -delete
        # find cloudmesh-bar -name '*.pyc' -delete
        # find cloudmesh-bar -name '*.pye' -delete
        # """
        # for line in clean.splitlines():
        #     try:
        #         r = os.system(line.strip())
        #     except:
        #         pass
        #     print (line.strip())

        path = Path("cloudmesh-bar/.git").resolve()
        Shell.rmdir(path)

        copy_tree("cloudmesh-bar", f"{package}")

        path = Path(f"{package}/.git").resolve()
        Shell.rmdir(path)

        replace_in_file(f"{package}/setup.py",
                        "bar",
                        f"{command}")

        os.rename(f"{package}/cloudmesh/bar/command/bar.py",
                  f"{package}/cloudmesh/bar/command/{command}.py")
        os.rename(f"{package}/cloudmesh/bar",
                  f"{package}/cloudmesh/{command}")

        shutil.rmtree(f'{package}/cloudmesh/foo')
        shutil.rmtree(f'{package}/cloudmesh/plugin')

        replace_in_file(
            f"{package}/cloudmesh/{command}/command/{command}.py",
            "Bar",
            f"{Command}")

        replace_in_file(
            f"{package}/cloudmesh/{command}/command/{command}.py",
            "bar",
            f"{command}")

        replace_in_file(f"{package}/Makefile", "bar", f"{command}")
        replace_in_file(f"{package}/README.md", "bar", f"{command}")

        writefile(f"{package}/.bumpversion.cfg",
                  generate_bumpversion(version=version, command=command))


        delete(f"{package}", "Makefilee")
        delete(f"{package}", "setup.pye")

        shutil.rmtree("cloudmesh-bar")


class Git(object):
    """
    Git management for the preparation to upload the code to pypi
    """

    pypis = ["cloudmesh-common",
             "cloudmesh-cmd5",
             "cloudmesh-sys",
             "cloudmesh-comet",
             "cloudmesh-openapi"]
    commits = pypis + ["cloudmesh-bar"]

    # , "cloudmesh-rest"]
    # "cloudmesh-robot"]

    @classmethod
    def upload(cls):
        """
        upload the code to pypi
        :return:
        """

        banner("CREATE DIST")
        for p in cls.pypis:
            try:
                os.system(f"cd {p}; make dist")
            except Exception as e:
                Console.error("can not create dist " + p)
                print(e)

        banner("UPLOAD TO PYPI")
        for p in cls.pypis:
            try:
                os.system(f"cd {p}; make upload")
            except Exception as e:
                Console.error("can upload " + p)
                print(e)

    @classmethod
    def commit(cls, msg):
        """
        commit the current code to git
        :param msg:
        :return:
        """

        banner("COMMIT " + msg)
        for p in cls.commits:
            banner("repo " + p)
            os.system(f'cd {p}; git commit -a -m "{msg}"')
            os.system(f'cd {p}; git push')


class Version(object):
    """
    set the version number of all base packages
    """

    @classmethod
    def set(cls, version):
        """
        set the version number
        :param version: the version as text string
        :return:
        """
        for repo in Git.commits:
            print(repo, "->", version)
            writefile(os.path.join(repo, "VERSION"), version)
