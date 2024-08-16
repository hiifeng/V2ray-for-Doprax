import logging
from concurrent.futures import ThreadPoolExecutor

# Constants
ADMIN_CHAT_ID = 428618726  # Replace with actual admin chat ID
BOT_TOKEN = "7481231141:AAFPNAXqj_9krUuN3wr548bu9bodACkyDOc"
CHOOSING, PAYMENT, CONFIRMING, BUYING_CONFIG, ADDING_CONFIG, ADDING_CONFIG_DETAILS = range(6)

# Logging setup
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# ThreadPoolExecutor for running database operations
executor = ThreadPoolExecutor(max_workers=5)
