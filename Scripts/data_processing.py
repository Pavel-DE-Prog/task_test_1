import pandas as pd

# Загрузка данных из CSV файла
file_path = r'C:\Users\Lenovo\Desktop\dataset_from_Kaggle\2015-street-tree-census-tree-data.csv'
data = pd.read_csv(file_path)

# Просмотр первых нескольких строк данных
print(data.head())

# Проверка названий и типов столбцов
print("Названия столбцов:")
print(data.columns)
print("Типы данных:")
print(data.dtypes)

# Анализ качества данных
print("Пропущенные значения:")
print(data.isnull().sum())
print(f"Количество дублированных записей: {data.duplicated().sum()}")

# Обработка пропущенных значений
if 'tree_dbh' in data.columns:
    data['tree_dbh'] = data['tree_dbh'].fillna(data['tree_dbh'].mean())  # Заполнение средним значением

if 'stump_diam' in data.columns:
    data['stump_diam'] = data['stump_diam'].fillna(0)  # Замена пропущенных значений на 0

# Приведение типов данных
if 'created_at' in data.columns:
    data['created_at'] = pd.to_datetime(data['created_at'], errors='coerce')

# Удаление дубликатов
data.drop_duplicates(inplace=True)

# Преобразование типов данных
data['block_id'] = data['block_id'].astype(int)
data['latitude'] = data['latitude'].astype(float)
data['longitude'] = data['longitude'].astype(float)

# Проверка на наличие некорректных значений (например, отрицательные значения)
if 'tree_dbh' in data.columns:
    invalid_dbh_count = (data['tree_dbh'] < 0).sum()
    if invalid_dbh_count > 0:
        print(f"Обнаружено {invalid_dbh_count} некорректных значений в tree_dbh.")
        # Удаление некорректных записей (если необходимо)
        data = data[data['tree_dbh'] >= 0]

# Проверка на наличие пропущенных значений после обработки
print("Пропущенные значения после обработки:")
print(data.isnull().sum())

# Удаление дубликатов (если не было удалено на предыдущем этапе)
data.drop_duplicates(inplace=True)

# Сохранение очищенных данных
output_path = r'C:\Users\Lenovo\Desktop\dataset_from_Kaggle\data\cleaned_data.csv'
data.to_csv(output_path, index=False)

print("Очищенные данные были успешно сохранены в cleaned_data.csv")