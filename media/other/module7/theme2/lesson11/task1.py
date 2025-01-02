import logging

# ваш код здесь
logging.basicConfig(
    level=logging.INFO,
    filename='main.log', 
    format='%(asctime)s, %(levelname)s, %(message)s, %(name)s'
)