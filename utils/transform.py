from utils.logger import Logger
import pandas as pd
import uuid


def flatten(json_obj, parent_key='', separator='_'):
    try:
        items = {}
        for k, v in json_obj.items():
            new_key = f"{parent_key}{separator}{k}" if parent_key else k
            if isinstance(v, dict):
                items.update(flatten(v, new_key))
            elif isinstance(v, list):
                for i, item in enumerate(v):
                    items.update(flatten(item, f"{new_key}"))
            else:
                items[new_key] = v
        return items
    
    except Exception as e:
        Logger.log_error(e)


def json_to_df(json):
    try:
        flat_list = flatten(json)
        flat_list2 = [flat_list]
        df = pd.DataFrame(flat_list2)
        df['uuid'] = [uuid.uuid4() for _ in range(len(df))]
        insert_cols = {'updates': [], 'insert_datetime': []}
        df_inserts = pd.DataFrame(insert_cols)
        if '[wind_gust]' not in df.columns:
            df_inserts['wind_gust'] = None
        return df
    
    except Exception as e:
        Logger.log_error(e)

