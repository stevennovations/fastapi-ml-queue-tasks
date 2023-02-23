from locust import HttpUser, task, between
import pandas as pd
import random

future = pd.date_range('2019-10-01', '2019-10-31', freq = 'D')
df_unseen = pd.DataFrame(index = future)
date_list = list(pd.to_datetime(df_unseen.index, format = '%Y-%m-%d').strftime('%Y%m%d'))

class AppUser(HttpUser):
    wait_time = between(2,5)


    @task
    def get_forecast(self):
        my_date = random.choice(date_list)
        self.client.get(f'/invoke?date_str={my_date}')
