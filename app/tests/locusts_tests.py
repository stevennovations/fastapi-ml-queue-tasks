from locust import HttpUser, task, between
import pandas as pd
import random

# Creates a date range value from October 1 2019 to October 31 2019
future = pd.date_range('2019-10-01', '2019-10-31', freq='D')
df_unseen = pd.DataFrame(index=future)
date_list = list(pd.to_datetime(df_unseen.index,
                                format='%Y-%m-%d').strftime('%Y%m%d'))
# ^ The above code can be changed not using pandas dataframe

class AppUser(HttpUser):
    """Load testing class to create a sample AppUser.
    That will query a specific date

    Args:
        HttpUser (_type_): _description_
    """
    wait_time = between(2, 3)

    @task
    def get_forecast(self):
        my_date = random.choice(date_list)
        url_str = '/api/v1/nikesalesforecast/forecast/?date_str='
        self.client.get(f'{url_str}{my_date}')
