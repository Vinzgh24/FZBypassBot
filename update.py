from os import path as opath, getenv
from logging import (
    StreamHandler,
    INFO,
    basicConfig,
    error as log_error,
    info as log_info,
)
from logging.handlers import RotatingFileHandler
from subprocess import run as srun
from dotenv import load_dotenv

basicConfig(
    level=INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s [%(filename)s:%(lineno)d]",
    datefmt="%d-%b-%y %I:%M:%S %p",
    handlers=[
        RotatingFileHandler("log.txt", maxBytes=50000000, backupCount=10),
        StreamHandler(),
    ],
)
load_dotenv("config.env", override=True)
       
BOT_TOKEN = getenv("BOT_TOKEN", "")
if len(BOT_TOKEN) == 0:
    LOGGER.error("BOT_TOKEN is not found!")
    exit(1)

bot_id = BOT_TOKEN.split(":", 1)[0]

UPSTREAM_REPO = getenv("UPSTREAM_REPO", None)
if (
    UPSTREAM_REPO is not None
    and UPSTREAM_REPO.startswith("#")
):
    UPSTREAM_REPO = None

UPSTREAM_BRANCH = getenv("UPSTREAM_BRANCH", None)
if UPSTREAM_BRANCH is None:
    UPSTREAM_BRANCH = "master"
    
if UPSTREAM_REPO is not None:
    if opath.exists(".git"):
        update = srun(
            [
                "rm -rf .git"
            ], shell=True
        )

    update = srun(
        [
            f"git init -q \
            && git config --global user.email ryuzakinear108@gmail.com \
            && git config --global user.name vinzgh24 \
            && git add . \
            && git commit -sm update -q \
            && git remote add origin {UPSTREAM_REPO} \
            && git fetch origin -q \
            && git reset --hard origin/{UPSTREAM_BRANCH} -q"
        ], shell=True
    )

    if update.returncode == 0:
        log_info("Successfully updated with latest commit from UPSTREAM_REPO!")
    else:
        log_info(
            "Something wrong while updating! Check UPSTREAM_REPO if valid or not!")

else:
    log_info.warning("UPSTREAM_REPO is not found!")
