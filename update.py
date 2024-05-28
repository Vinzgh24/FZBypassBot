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

if not os.path.exists("config.env"):
    CONFIG_FILE_URL = os.environ.get("CONFIG_FILE_URL", "")
    if len(CONFIG_FILE_URL) != 0:
        LOGGER.info("CONFIG_FILE_URL is found! Downloading CONFIG_FILE_URL...")
        r = requests.get(
            CONFIG_FILE_URL
        )
        
        if not r.ok:
            LOGGER.error(f"Failed to download config.env! ERROR: [{r.status_code}] {r.text}")
    
        with open("config.env", "wb+") as file:
            file.write(r.content)
    else:
        LOGGER.warning("CONFIG_FILE_URL is not found! Using local config.env instead...")
            
load_dotenv("config.env", override=True)

BOT_TOKEN = os.environ.get("BOT_TOKEN", "")
if len(BOT_TOKEN) == 0:
    LOGGER.error("BOT_TOKEN is not found!")
    exit(1)

bot_id = BOT_TOKEN.split(":", 1)[0]

UPSTREAM_REPO = os.environ.get("UPSTREAM_REPO", None)
if (
    UPSTREAM_REPO is not None
    and UPSTREAM_REPO.startswith("#")
):
    UPSTREAM_REPO = None

UPSTREAM_BRANCH = os.environ.get("UPSTREAM_BRANCH", None)
if UPSTREAM_BRANCH is None:
    UPSTREAM_BRANCH = "master"
    
if UPSTREAM_REPO is not None:
    if os.path.exists(".git"):
        subprocess.run(
            [
                "rm -rf .git"
            ], shell=True
        )

    process = subprocess.run(
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

    if process.returncode == 0:
        LOGGER.info("Successfully updated with latest commit from UPSTREAM_REPO!")
    else:
        LOGGER.error(
            "Something wrong while updating! Check UPSTREAM_REPO if valid or not!")

else:
    LOGGER.warning("UPSTREAM_REPO is not found!")
