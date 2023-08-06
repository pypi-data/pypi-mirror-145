import os
import sys
import shlex
import shutil
import logging
import platform
import subprocess
import tarfile
from tempfile import TemporaryDirectory

logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s %(levelname)-7s] %(message)s"
)

PYPI = [
    ("ricequant", "RiceQuant77", "https://pypi.ricequant.com:8080"),
    ("ricequant", "Ricequant123", " https://pypi2.ricequant.com")
]


def _run_command(command):
    logging.debug(command)
    proc = subprocess.run(
        command if platform.system() == "Windows" else shlex.split(command),
        stdout=subprocess.PIPE, stderr=subprocess.STDOUT
    )
    if proc.returncode != 0:
        raise RuntimeError(f"command failed: {command}\n{proc.stdout}")
    else:
        logging.debug(f"\n{proc.stdout}")


def _run_python_command(command):
    _run_command(f"{sys.executable} {command}")


def _pip_install(pkg_name):
    logging.info(f"installing {pkg_name}...")
    _run_python_command(f"-m pip install -i https://pypi.douban.com/simple {pkg_name}")


def build(requirements_txt: str):
    if platform.system() == "Linux":
        _pip_install("auditwheel")
    elif platform.system() == "Darwin":
        _pip_install("delocate")
    _pip_install("twine")

    pkg_dir_obj, source_dir_obj, whl_dir_obj = TemporaryDirectory(), TemporaryDirectory(), TemporaryDirectory()
    pkg_dir, source_dir, whl_dir = pkg_dir_obj.name, source_dir_obj.name, whl_dir_obj.name
    try:
        logging.info("downloading pkgs...")
        _run_python_command(f"-m pip download -i https://pypi.douban.com/simple --extra-index-url https://rquser:Ricequant8@pypi2.ricequant.com/simple/ --progress-bar off -r {requirements_txt} -d {pkg_dir} --no-deps")
        for file in os.listdir(pkg_dir):
            if file.endswith(".whl"):
                logging.info(f"copying {file}...")
                shutil.copy(os.path.join(pkg_dir, file), whl_dir)
                continue
            if not file.endswith(".tar.gz"):
                raise NotImplementedError(f"unsupported file format: {file}")
            logging.info(f"decompressing {file}...")
            with tarfile.open(os.path.join(pkg_dir, file)) as f:
                f.extractall(source_dir)
        for dir in os.listdir(source_dir):
            logging.info(f"building {dir}...")
            os.chdir(os.path.join(source_dir, dir))
            _run_python_command(f"setup.py bdist_wheel")
            for whl_file in os.listdir("dist"):
                whl_file = os.path.join("dist", whl_file)
                if platform.system() == "Darwin":
                    _run_command(f"delocate-wheel -w {whl_dir} {whl_file}")
                elif platform.system() == "Linux":
                    _run_command(f"auditwheel repair -w {whl_dir} {whl_file} --plat linux_x86_64")
                else:
                    shutil.copy(whl_file, whl_dir)

        for file in os.listdir(whl_dir):
            for username, password, url in PYPI:
                logging.info(f"uploading {file} to {url}...")
                _run_command("twine upload --repository-url {} -u {} -p {} --skip-existing {}".format(
                    url, username, password, os.path.join(whl_dir, file)
                ))
    finally:
        for dir in [pkg_dir_obj, source_dir_obj, whl_dir_obj]:
            try:
                dir.cleanup()
            except:
                continue


if __name__ == "__main__":
    build(os.path.join(os.path.dirname(__file__), "requirements.txt"))
