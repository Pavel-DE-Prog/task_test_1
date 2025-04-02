import psycopg2
import csv
import logging
from config import host, user, password, db_name

# Настройка логирования
logging.basicConfig(filename='db_operations.log', level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

cleaned_file_path = r'C:\Users\Lenovo\Desktop\dataset_from_Kaggle\data\cleaned_data.csv'  # Объявляем путь к файлу

try:
    # Подключение к существующей базе данных
    connection = psycopg2.connect(
        host=host,
        user=user,
        password=password,
        database=db_name
    )
    connection.autocommit = True

    # Курсор для выполнения операций с базой данных
    with connection.cursor() as cursor:
        # Проверка версии сервера
        cursor.execute("SELECT version();")
        server_version = cursor.fetchone()
        logging.info(f"Server version: {server_version}")

        # Открытие очищенного CSV файла и вставка данных с помощью COPY
        with open(cleaned_file_path, 'r', newline='') as csvfile:
            next(csvfile)  # Пропуск заголовков

            try:
                cursor.copy_expert("COPY trees FROM STDIN WITH CSV", csvfile)
                logging.info("Data successfully copied from CSV to the database.")
            except Exception as copy_error:
                logging.error(f"An error occurred while copying data: {copy_error}")

except Exception as e:
    logging.error(f"An error occurred: {e}")

finally:
    # Закрытие соединения
    if 'connection' in locals():
        connection.close()