import os
import re
from dotenv import load_dotenv
import subprocess

load_dotenv()

BOT_PATH = r"social\bot_instagram.php"

# Load values from .env
USER_TOKEN = os.getenv("IG_ACCESS_TOKEN")
PAGE_ID = os.getenv("PAGE_ID")
IG_BUSINESS_ID = os.getenv("IG_BUSINESS_ID")

print("Injecting tokens...")

with open(BOT_PATH, "r", encoding="utf-8") as f:
    original_content = f.read()

bot_content = original_content
bot_content = re.sub(r'\$USER_TOKEN = ".*?";', f'$USER_TOKEN = "{USER_TOKEN}";', bot_content)
bot_content = re.sub(r'\$PAGE_ID = ".*?";', f'$PAGE_ID = "{PAGE_ID}";', bot_content)
bot_content = re.sub(r'\$IG_BUSINESS_ID = ".*?";', f'$IG_BUSINESS_ID = "{IG_BUSINESS_ID}";', bot_content)

with open(BOT_PATH, "w", encoding="utf-8") as f:
    f.write(bot_content)

print("Deploying...")
subprocess.run(["python", "-m", "social.deploy_bot"])

print("Restoring placeholders to prevent git tracking of secrets...")
with open(BOT_PATH, "w", encoding="utf-8") as f:
    f.write(original_content)

print("Done!")
