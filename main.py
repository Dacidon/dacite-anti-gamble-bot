import asyncio
import logging
import sys

import handlers.user_handlers

from utils.db import check_db
from utils.loader import dp, bot

async def main() -> None:
    await dp.start_polling(bot)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    check_db()
    asyncio.run(main())