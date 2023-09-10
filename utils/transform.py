from utils.logger import Logger
import pandas as pd
import uuid


class JsonFlattener:
    def __init__(self, separator='_'):
        self.separator = separator

    def flatten(self, json_obj, parent_key=''):
        try:
            items = {}
            for k, v in json_obj.items():
                new_key = f"{parent_key}{self.separator}{k}" if parent_key else k
                if isinstance(v, dict):
                    items.update(self.flatten(v, new_key))
                elif isinstance(v, list):
                    for i, item in enumerate(v):
                        items.update(self.flatten(item, f"{new_key}"))
                else:
                    items[new_key] = v

            Logger.log_info('API response successfully flattened.')
            return items

        except Exception as e:
            Logger.log_error(e)


class DFConverter:
    def __init__(self):
        pass

    @staticmethod
    def convert_json(json):
        try:
            flattener = JsonFlattener()
            flat_list = flattener.flatten(json)
            flat_list2 = [flat_list]
            df = pd.DataFrame(flat_list2)
            df['uuid'] = [uuid.uuid4() for _ in range(len(df))]
            insert_cols = {'updates': [], 'insert_datetime': []}
            df_inserts = pd.DataFrame(insert_cols)
            if '[wind_gust]' not in df.columns:
                df_inserts['wind_gust'] = None
            Logger.log_info("Dataframe successfully created.")
            return df

        except Exception as e:
            Logger.log_error()
