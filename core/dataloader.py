from pathlib import Path
import pandas as pd
from sklearn.preprocessing import StandardScaler

def load_data(data_path: Path) -> pd.DataFrame:
    data = pd.read_csv(data_path.absolute())
    data['date'] = pd.to_datetime(data['date']) # Приводим дату к правильному формату
    return data


def transform_data(data: pd.DataFrame) -> pd.DataFrame:
    # Убираем признаки в которых много пропущенных значений
    feature_list = []
    for column in data.columns:
        if (data[column].nunique() >= 1) & (data[column].notnull().sum() > 0.01 * data.shape[0]):
            feature_list.append(column)
    data = data[feature_list]

    # Оставляем только нормализованные фичи и строим по ним EMA (экспоненциальное скользящее среднее)
    smart_features = []
    base_features = []
    for column in data.columns:
        if column[-10:] != 'normalized' and column[:5] == 'smart':
            smart_features.append(column)
        elif column[-10:] != 'normalized':
            base_features.append(column)
    data = data[base_features + smart_features]
    scaler = StandardScaler()
    data[smart_features] = scaler.fit_transform(data[smart_features])

    # Вычисление скользящего среднего
    window_size = 21
    for feature in smart_features:
        data[feature+'_ema'] = data.groupby('serial_number')[feature].transform(lambda x: x.ewm(span=window_size, adjust=False).mean())
   

    # Посчитаем изменения в процентах показателей за 7 дней
    size = 7
    new_columns = []
    for i in range(size, size+1):
        print(i)
        for feature in smart_features:
            new_col_name = f'{feature}_chg_{i}'
            new_col_data = (data[feature] /  data.groupby('serial_number')[feature].shift(i)) - 1
            new_columns.append(pd.Series(new_col_data, name=new_col_name))
            
            new_col_name = f'{feature}_ema_chg_{i}'
            new_col_data = (data[feature+'_ema'] /  data.groupby('serial_number')[feature+'_ema'].shift(i)) - 1
            new_columns.append(pd.Series(new_col_data, name=new_col_name))
            
    data = pd.concat([data] + new_columns, axis=1)

    # Применяем функцию к каждой строке DataFrame. Получаем столбец показывающий количество отказов в текущем vault_id
    data['failure_count'] = data.groupby(['date', 'vault_id'])['failure'].transform(lambda x: (x == 1).sum())

    return data


