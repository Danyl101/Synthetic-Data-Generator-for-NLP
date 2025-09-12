import logging

logging.basicConfig(
        filename="Logs/Flask.log",
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(message)s",
        filemode="w",
    )