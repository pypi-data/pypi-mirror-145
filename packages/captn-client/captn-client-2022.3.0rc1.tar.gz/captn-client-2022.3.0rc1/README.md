# Capt’n python client 2022.3.0rc1

A python library encapsulating captn service REST API available at:

- <a href="https://api.airt.ai/docs" target="_blank">https://api.airt.ai/</a>

## Docs

Full documentation can be found at the following link:

- <a href="https://docs.captn.ai" target="_blank">https://docs.captn.ai/</a>


## How to install

If you don't have the captn library already installed, please install it using pip.


```console
pip install captn-client
```

## How to use

To access the captn service, you must create a developer account. Please fill out the signup form below to get one:

- [https://bit.ly/3I4cNuv](https://bit.ly/3I4cNuv)

Upon successful verification, you will receive the username/password for the developer account in an email. 

Finally, you need an application token to access all the APIs in captn service. Please call the `Client.get_token` method with the username/password to get one. 

You can either pass the username, password, and server address as parameters to the `Client.get_token` method or store the same in the **CAPTN_SERVICE_USERNAME**, **CAPTN_SERVICE_PASSWORD**, and **CAPTN_SERVER_URL** environment variables.

After successful authentication, the captn services will be available to access.

For more information, please check:

- [Tutorial](https://docs.captn.ai/Tutorial/) with more elaborate example, and

- [API](https://docs.captn.ai/API/client/Client/) with reference documentation.


Below is a minimal example explaining how to load the data, train a model and make predictions using captn services. 

!!! info

	In the below example, the username, password, and server address are stored in **CAPTN_SERVICE_USERNAME**, **CAPTN_SERVICE_PASSWORD**, and **CAPTN_SERVER_URL** environment variables.


### 0. Get token


```
import json
from captn.client import Client, DataBlob, DataSource

Client.get_token()
```

### 1. Connect and preprocess data

In our example, we will be using the captn APIs to load and preprocess a sample CSV file stored in an AWS S3 bucket. 


```
data_blob = DataBlob.from_s3(
    uri="s3://test-airt-service/sample_gaming_cohort_data/"
)
data_blob.progress_bar()

```

    100%|██████████| 1/1 [01:35<00:00, 95.81s/it]


The sample data we used in this example doesn't have the header rows and their data types defined. 

The following code creates the necessary headers along with their data types and reads only a subset of columns that are required for modeling:



```
prefix = ["revenue", "ad_revenue", "conversion", "retention"]
days = list(range(30)) + list(range(30, 361, 30))
dtype = {
    "date": "str",
    "game_name": "str",
    "platform": "str",
    "user_type": "str",
    "network": "str",
    "campaign": "str",
    "adgroup": "str",
    "installs": "int32",
    "spend": "float32",
}
dtype.update({f"{p}_{d}": "float32" for p in prefix for d in days})
names = list(dtype.keys())

kwargs = {"delimiter": "|", "names": names, "parse_dates": ["date"], "usecols": names[:42], "dtype": dtype}
```

Finally, the above variables are passed to the `DataBlob.from_csv` method which preprocesses the data and stores it in captn server.


```
data_source = data_blob.from_csv(
    index_column="game_name",
    sort_by="date",
    kwargs_json=json.dumps(kwargs)
)

data_source.progress_bar()
```

    100%|██████████| 1/1 [00:40<00:00, 40.37s/it]



```
data_source.head()
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>date</th>
      <th>platform</th>
      <th>user_type</th>
      <th>network</th>
      <th>campaign</th>
      <th>adgroup</th>
      <th>installs</th>
      <th>spend</th>
      <th>revenue_0</th>
      <th>revenue_1</th>
      <th>...</th>
      <th>revenue_23</th>
      <th>revenue_24</th>
      <th>revenue_25</th>
      <th>revenue_26</th>
      <th>revenue_27</th>
      <th>revenue_28</th>
      <th>revenue_29</th>
      <th>revenue_30</th>
      <th>revenue_60</th>
      <th>revenue_90</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>2021-03-15</td>
      <td>ios</td>
      <td>Facebook Ads</td>
      <td>Facebook Ads</td>
      <td>campaign_144</td>
      <td>adgroup_271</td>
      <td>96</td>
      <td>545.849976</td>
      <td>130.000000</td>
      <td>170.144928</td>
      <td>...</td>
      <td>632.002380</td>
      <td>632.539246</td>
      <td>660.857056</td>
      <td>666.857056</td>
      <td>666.857056</td>
      <td>700.857056</td>
      <td>729.035645</td>
      <td>729.035645</td>
      <td>1115.538574</td>
      <td>1282.981079</td>
    </tr>
    <tr>
      <th>1</th>
      <td>2021-03-15</td>
      <td>ios</td>
      <td>snapchat_int</td>
      <td>snapchat_int</td>
      <td>campaign_569</td>
      <td>adgroup_1634</td>
      <td>10</td>
      <td>207.919998</td>
      <td>33.000000</td>
      <td>39.000000</td>
      <td>...</td>
      <td>71.282143</td>
      <td>71.282143</td>
      <td>71.282143</td>
      <td>71.282143</td>
      <td>73.376190</td>
      <td>73.376190</td>
      <td>73.376190</td>
      <td>73.376190</td>
      <td>94.752373</td>
      <td>143.727859</td>
    </tr>
    <tr>
      <th>2</th>
      <td>2021-03-15</td>
      <td>ios</td>
      <td>unityads_int</td>
      <td>unityads_int</td>
      <td>campaign_62</td>
      <td>adgroup_275</td>
      <td>41</td>
      <td>73.339996</td>
      <td>6.000000</td>
      <td>22.297548</td>
      <td>...</td>
      <td>42.324429</td>
      <td>42.462334</td>
      <td>42.462334</td>
      <td>42.462334</td>
      <td>42.500793</td>
      <td>43.640785</td>
      <td>43.869404</td>
      <td>43.871078</td>
      <td>50.590389</td>
      <td>50.590389</td>
    </tr>
    <tr>
      <th>3</th>
      <td>2021-03-15</td>
      <td>ios</td>
      <td>jetfuelit_int</td>
      <td>jetfuelit_int</td>
      <td>campaign_0</td>
      <td>adgroup_683</td>
      <td>32</td>
      <td>60.099998</td>
      <td>33.000000</td>
      <td>45.928074</td>
      <td>...</td>
      <td>58.466618</td>
      <td>58.466618</td>
      <td>58.466618</td>
      <td>58.466618</td>
      <td>58.466618</td>
      <td>58.466618</td>
      <td>58.466618</td>
      <td>58.466618</td>
      <td>58.466618</td>
      <td>72.491997</td>
    </tr>
    <tr>
      <th>4</th>
      <td>2021-03-15</td>
      <td>ios</td>
      <td>jetfuelit_int</td>
      <td>jetfuelit_int</td>
      <td>campaign_0</td>
      <td>adgroup_278</td>
      <td>9</td>
      <td>19.500000</td>
      <td>13.000000</td>
      <td>13.438093</td>
      <td>...</td>
      <td>19.427818</td>
      <td>19.427818</td>
      <td>19.427818</td>
      <td>19.427818</td>
      <td>19.427818</td>
      <td>19.427818</td>
      <td>19.427818</td>
      <td>19.427818</td>
      <td>19.427818</td>
      <td>19.427818</td>
    </tr>
    <tr>
      <th>5</th>
      <td>2021-03-15</td>
      <td>ios</td>
      <td>jetfuelit_int</td>
      <td>jetfuelit_int</td>
      <td>campaign_0</td>
      <td>adgroup_921</td>
      <td>4</td>
      <td>7.950000</td>
      <td>0.000000</td>
      <td>0.129259</td>
      <td>...</td>
      <td>4.205401</td>
      <td>4.205401</td>
      <td>4.205401</td>
      <td>4.205401</td>
      <td>4.205401</td>
      <td>4.205401</td>
      <td>4.205401</td>
      <td>4.205401</td>
      <td>4.227401</td>
      <td>4.227401</td>
    </tr>
    <tr>
      <th>6</th>
      <td>2021-03-15</td>
      <td>ios</td>
      <td>jetfuelit_int</td>
      <td>jetfuelit_int</td>
      <td>campaign_0</td>
      <td>adgroup_327</td>
      <td>3</td>
      <td>5.380000</td>
      <td>0.000000</td>
      <td>0.000000</td>
      <td>...</td>
      <td>0.000000</td>
      <td>0.000000</td>
      <td>0.000000</td>
      <td>0.000000</td>
      <td>0.000000</td>
      <td>0.000000</td>
      <td>0.000000</td>
      <td>0.000000</td>
      <td>0.000000</td>
      <td>0.000000</td>
    </tr>
    <tr>
      <th>7</th>
      <td>2021-03-15</td>
      <td>ios</td>
      <td>jetfuelit_int</td>
      <td>jetfuelit_int</td>
      <td>campaign_0</td>
      <td>adgroup_5815</td>
      <td>1</td>
      <td>2.450000</td>
      <td>0.000000</td>
      <td>0.000000</td>
      <td>...</td>
      <td>0.000000</td>
      <td>0.000000</td>
      <td>0.000000</td>
      <td>0.000000</td>
      <td>0.000000</td>
      <td>0.000000</td>
      <td>0.000000</td>
      <td>0.000000</td>
      <td>0.000000</td>
      <td>0.000000</td>
    </tr>
    <tr>
      <th>8</th>
      <td>2021-03-15</td>
      <td>ios</td>
      <td>jetfuelit_int</td>
      <td>jetfuelit_int</td>
      <td>campaign_0</td>
      <td>adgroup_162</td>
      <td>1</td>
      <td>0.600000</td>
      <td>0.000000</td>
      <td>0.026555</td>
      <td>...</td>
      <td>0.026555</td>
      <td>0.026555</td>
      <td>0.026555</td>
      <td>0.026555</td>
      <td>0.026555</td>
      <td>0.026555</td>
      <td>0.026555</td>
      <td>0.026555</td>
      <td>0.026555</td>
      <td>0.026555</td>
    </tr>
    <tr>
      <th>9</th>
      <td>2021-03-15</td>
      <td>android</td>
      <td>Facebook Ads</td>
      <td>Facebook Ads</td>
      <td>campaign_23</td>
      <td>adgroup_9</td>
      <td>730</td>
      <td>335.640015</td>
      <td>36.300461</td>
      <td>59.481831</td>
      <td>...</td>
      <td>124.508873</td>
      <td>124.631615</td>
      <td>124.644920</td>
      <td>124.652664</td>
      <td>124.905174</td>
      <td>124.946205</td>
      <td>125.000298</td>
      <td>125.046783</td>
      <td>125.483368</td>
      <td>125.519073</td>
    </tr>
  </tbody>
</table>
<p>10 rows × 41 columns</p>
</div>



### 2. Training


```
# Todo
```
