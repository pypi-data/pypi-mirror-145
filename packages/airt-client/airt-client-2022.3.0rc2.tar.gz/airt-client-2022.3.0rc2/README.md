# Python client for airt service 2022.3.0rc2

A python library encapsulating airt service REST API available at:

- <a href="https://api.airt.ai/docs" target="_blank">https://api.airt.ai/</a>

## Docs

For full documentation, Please follow the below link:

- <a href="https://docs.airt.ai" target="_blank">https://docs.airt.ai/</a>


## How to install

If you don't have the airt library already installed, please install it using pip.


```console
pip install airt-client
```

## How to use

To access the airt service, you must create a developer account. Please fill out the signup form below to get one:

- [https://bit.ly/3hbXQLY](https://bit.ly/3hbXQLY)

Upon successful verification, you will receive the username/password for the developer account in an email. 

Finally, you need an application token to access all the APIs in airt service. Please call the `Client.get_token` method with the username/password to get one. You 
can either pass the username, password, and server address as parameters to the `Client.get_token` method or store the same in the **AIRT_SERVICE_USERNAME**, 
**AIRT_SERVICE_PASSWORD**, and **AIRT_SERVER_URL** environment variables.

Upon successful authentication, the airt services will be available to access.
    
For more information, please check:

- [Tutorial](https://docs.airt.ai/Tutorial/) with more elaborate example, and

- [API](https://docs.airt.ai/API/client/Client/) with reference documentation.

Below is a minimal example explaining how to train a model and make predictions using airt services. 

!!! info

	In the below example, the username, password, and server address are stored in **AIRT_SERVICE_USERNAME**, **AIRT_SERVICE_PASSWORD**, and **AIRT_SERVER_URL** environment variables.


### 0. Get token


```
from airt.client import Client, DataSource, DataBlob

Client.get_token()
```

### 1. Connect data


```
# In this case, the input data is a CSV file strored in an AWS S3 bucket.

# Pulling the data into airt server
data_blob = DataBlob.from_s3(
    uri="s3://test-airt-service/ecommerce_behavior_csv"
)
data_blob.progress_bar()

# Preprocessing the data
data_source = data_blob.from_csv(
    index_column="user_id",
    sort_by="event_time"
)
data_source.progress_bar()

display(data_source.head())
```

    100%|██████████| 1/1 [00:35<00:00, 35.33s/it]
    100%|██████████| 1/1 [00:30<00:00, 30.28s/it]



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
      <th>event_time</th>
      <th>event_type</th>
      <th>product_id</th>
      <th>category_id</th>
      <th>category_code</th>
      <th>brand</th>
      <th>price</th>
      <th>user_session</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>2019-11-06 06:51:52+00:00</td>
      <td>view</td>
      <td>26300219</td>
      <td>2053013563424899933</td>
      <td>None</td>
      <td>sokolov</td>
      <td>40.54</td>
      <td>d1fdcbf1-bb1f-434b-8f1a-4b77f29a84a0</td>
    </tr>
    <tr>
      <th>1</th>
      <td>2019-11-05 21:25:44+00:00</td>
      <td>view</td>
      <td>2400724</td>
      <td>2053013563743667055</td>
      <td>appliances.kitchen.hood</td>
      <td>bosch</td>
      <td>246.85</td>
      <td>b097b84d-cfb8-432c-9ab0-a841bb4d727f</td>
    </tr>
    <tr>
      <th>2</th>
      <td>2019-11-05 21:27:43+00:00</td>
      <td>view</td>
      <td>2400724</td>
      <td>2053013563743667055</td>
      <td>appliances.kitchen.hood</td>
      <td>bosch</td>
      <td>246.85</td>
      <td>b097b84d-cfb8-432c-9ab0-a841bb4d727f</td>
    </tr>
    <tr>
      <th>3</th>
      <td>2019-11-05 19:38:48+00:00</td>
      <td>view</td>
      <td>3601406</td>
      <td>2053013563810775923</td>
      <td>appliances.kitchen.washer</td>
      <td>beko</td>
      <td>195.60</td>
      <td>d18427ab-8f2b-44f7-860d-a26b9510a70b</td>
    </tr>
    <tr>
      <th>4</th>
      <td>2019-11-05 19:40:21+00:00</td>
      <td>view</td>
      <td>3601406</td>
      <td>2053013563810775923</td>
      <td>appliances.kitchen.washer</td>
      <td>beko</td>
      <td>195.60</td>
      <td>d18427ab-8f2b-44f7-860d-a26b9510a70b</td>
    </tr>
    <tr>
      <th>5</th>
      <td>2019-11-06 05:39:21+00:00</td>
      <td>view</td>
      <td>15200134</td>
      <td>2053013553484398879</td>
      <td>None</td>
      <td>racer</td>
      <td>55.86</td>
      <td>fc582087-72f8-428a-b65a-c2f45d74dc27</td>
    </tr>
    <tr>
      <th>6</th>
      <td>2019-11-06 05:39:34+00:00</td>
      <td>view</td>
      <td>15200134</td>
      <td>2053013553484398879</td>
      <td>None</td>
      <td>racer</td>
      <td>55.86</td>
      <td>fc582087-72f8-428a-b65a-c2f45d74dc27</td>
    </tr>
    <tr>
      <th>7</th>
      <td>2019-11-05 20:25:52+00:00</td>
      <td>view</td>
      <td>1005106</td>
      <td>2053013555631882655</td>
      <td>electronics.smartphone</td>
      <td>apple</td>
      <td>1422.31</td>
      <td>79d8406f-4aa3-412c-8605-8be1031e63d6</td>
    </tr>
    <tr>
      <th>8</th>
      <td>2019-11-05 23:13:43+00:00</td>
      <td>view</td>
      <td>31501222</td>
      <td>2053013558031024687</td>
      <td>None</td>
      <td>dobrusskijfarforovyjzavod</td>
      <td>115.18</td>
      <td>e3d5a1a4-f8fd-4ac3-acb7-af6ccd1e3fa9</td>
    </tr>
    <tr>
      <th>9</th>
      <td>2019-11-06 07:00:32+00:00</td>
      <td>view</td>
      <td>1005115</td>
      <td>2053013555631882655</td>
      <td>electronics.smartphone</td>
      <td>apple</td>
      <td>915.69</td>
      <td>15197c7e-aba0-43b4-9f3a-a815e31ade40</td>
    </tr>
  </tbody>
</table>
</div>


### 2. Train


```
from datetime import timedelta

model = data_source.train(
    client_column="user_id",
    target_column="event_type",
    target="*purchase",
    predict_after=timedelta(hours=3),
)
model.progress_bar()
print(model.evaluate())
```

    100%|██████████| 5/5 [00:00<00:00, 135.21it/s]

                eval
    accuracy   0.985
    recall     0.962
    precision  0.934


    


### 3. Predict


```
predictions = model.predict()
predictions.progress_bar()
print(predictions.to_pandas().head())
```

    100%|██████████| 3/3 [00:00<00:00, 112.70it/s]


                  Score
    user_id            
    520088904  0.979853
    530496790  0.979157
    561587266  0.979055
    518085591  0.978915
    558856683  0.977960

