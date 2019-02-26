Title: Predicting Bitcoin Price Using Metcalfe's Law
Date: 2017-11-15
Modified: 2017-11-16
Authors: Adil Sadik
Tags: bitcoin, cryptocurrency, finance

Metcalfe's Law states that the value of a network is proportional to the square of the number of users on the network. The classic example is a fax machine: a fax machine is useless by itself, but is very useful if a few of your friends have one. If the number of fax machine users doubles, the value of the network increases exponentially.

This model has been successfully applied to a few real-world networks. Below is Facebook, as an example (stolen from [Wikipedia](https://en.wikipedia.org/wiki/Metcalfe%27s_law#Validation_with_actual_data)):

\begin{equation*}
V = 5.70\times10^{-9}\times n^{2}
\end{equation*}

[Fundstrat](http://www.businessinsider.com/bitcoin-price-movement-explained-by-one-equation-fundstrat-tom-lee-metcalf-law-network-effect-2017-10#ampshare=http://www.businessinsider.com/bitcoin-price-movement-explained-by-one-equation-fundstrat-tom-lee-metcalf-law-network-effect-2017-10) had the idea to try and apply this formula to the price of bitcoin. Unique bitcoin addresses are used as a proxy for number of network users.

Fundstrat also added to this formula the number of transactions per user. Per the article, they arrived at their formula as such:
> FundStrat found a formula by regressing the price of bitcoin against both unique addresses squared and transaction volume per user. This model explained 94% of the variation in the cryptocurrency price since 2013.

Something like:
\begin{equation*}
BTC = x\times n^{2} \times \frac tn
\end{equation*}

Where X is a constant, n is number of addresses, and t is transactions

In this notebook, I try and replicate these results. Ultimately, I was able to reproduce the results by *not* normalizing the number of transactions (using the raw transaction volume instead) as such:

\begin{equation*}
BTC = x\times n^{2} \times t
\end{equation*}

Using the above formula I achieve the same 94% accuracy.

## Getting the data

First, import the required modules:


```python
import requests
from datetime import datetime
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sb
from sklearn import linear_model
from sklearn.metrics import r2_score

sb.set(font_scale=2.0)
%matplotlib inline
```

We will use the excellent [blockchain.info](https://blockchain.info/) to acquire the necessary data. Blockchain.info has charts for nearly every aspect of bitcoin. All charts are accessible via an API that returns JSON objects

The below function fetches the data, parses out the relevant portion and returns it as a pandas ```Dataframe```.


```python
def get_data(address):
    r = requests.get(address)
    data = r.json()
    data = pd.DataFrame(data['values'])
    return data
```


```python
# fetch all data
addresses = get_data('https://api.blockchain.info/charts/n-unique-addresses?timespan=all&format=json')
price = get_data('https://api.blockchain.info/charts/market-price?timespan=all&format=json')
volume = get_data('https://api.blockchain.info/charts/estimated-transaction-volume-usd?timespan=all&format=json')
```

Once we have our data, we'll rename the columns, convert timestamps to ```datetime``` objects, and reindex by date


```python
# rename columns
addresses.columns = ['date', 'addresses']
volume.columns = ['date', 'volume']
price.columns = ['date', 'price']
```


```python
# convert unix-stye timestamps into datetime objects
addresses.date = addresses.date.apply(datetime.fromtimestamp)
volume.date = volume.date.apply(datetime.fromtimestamp)
price.date = price.date.apply(datetime.fromtimestamp)
```


```python
# reindex the dataframe by date
addresses.set_index(keys='date', inplace=True)
volume.set_index(keys='date', inplace=True)
price.set_index(keys='date', inplace=True)
```

We'll join the dataframes so we only have one dataframe we need to worry about for the rest of the notebook


```python
data = price.join([addresses, volume], how='outer')
```

It looks like these API endpoints will sometimes return data for different days (ie one returns odd-numbered dates and the other even-numbered dates.) Let's interpolate the data to make sure there are no gaps


```python
data = data.interpolate()
data.tail()
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
      <th>price</th>
      <th>addresses</th>
      <th>volume</th>
    </tr>
    <tr>
      <th>date</th>
      <th></th>
      <th></th>
      <th></th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>2017-11-04 20:00:00</th>
      <td>7377.01</td>
      <td>555458</td>
      <td>1.309727e+09</td>
    </tr>
    <tr>
      <th>2017-11-06 19:00:00</th>
      <td>7092.12</td>
      <td>714349</td>
      <td>1.826009e+09</td>
    </tr>
    <tr>
      <th>2017-11-08 19:00:00</th>
      <td>7158.03</td>
      <td>727945</td>
      <td>2.267000e+09</td>
    </tr>
    <tr>
      <th>2017-11-10 19:00:00</th>
      <td>6362.85</td>
      <td>455431</td>
      <td>1.344146e+09</td>
    </tr>
    <tr>
      <th>2017-11-12 19:00:00</th>
      <td>6550.22</td>
      <td>694828</td>
      <td>2.115296e+09</td>
    </tr>
  </tbody>
</table>
</div>



Looks good. We only care about the last ~3 years, so let's cut that out of the dataframe


```python
# get the last ~3 years
data = data.tail(1150)
```

Great! Let's take a look at what we have. Since all three values are on such different scales, we'll look at them separately


```python
data.price.plot(figsize=(25,10))
```








![png]({filename}/images/output_21_1.png)



```python
data.addresses.plot(figsize=(25,10))
```








![png]({filename}/images/output_22_1.png)



```python
data.volume.plot(figsize=(25,10))
```








![png]({filename}/images/output_23_1.png)


Hard to tell if there's any relationship here. What's clear is that the data is pretty noisy, so let's smooth it out by applying an exponentially-weighted moving average


```python
# smoothing
data = pd.ewma(data, span=7)
```


## Fitting the model

Ok, now we have the data. Let us try and do something with it.

Here we are going to use [Scikit Learn](http://scikit-learn.org/stable/)'s [Linear Regression](http://scikit-learn.org/stable/modules/generated/sklearn.linear_model.LinearRegression.html) model to fit our data. 

First we create the classifier:


```python
clf = linear_model.LinearRegression(n_jobs=2)
```

Next we pull our inputs out of the ```data``` dataframe into a new ```train``` dataframe


```python
train = data[['addresses', 'volume']]
```

Per Metcalfe's law, we will square the number of "users:"


```python
train.addresses = train.addresses.pow(2)
```

Next we grab our target output ```price``` and put it in its own dataframe


```python
y = data['price']
```

Finally, we fit the model:


```python
clf.fit(train, y)
```




    LinearRegression(copy_X=True, fit_intercept=True, n_jobs=2, normalize=False)



Fitting the model should happen pretty quickly (less than a second on a modern machine.) 

## Analyzing Results
Now we can take a look at the results. We use the classifiers ```predict``` function to run through our test set and produce expected outputs (prices). We then join this with the actual prices, rename the columns, and plot the results for the past year.


```python
pred = pd.DataFrame(clf.predict(train), index=data.index)
```


```python
compare = pred.join(data['price'])
```


```python
compare.columns = ['predicted', 'actual']
```


```python
compare.tail(365).plot(figsize=(25,10))
```








![png]({filename}/images/output_42_1.png)


It looks like we have a pretty good fit here. Let's take a closer look at the last ten days


```python
compare.tail(10).plot(figsize=(25,10))
```








![png]({filename}/images/output_44_1.png)


At the time of this writing Bitcoin is (somewhat shockingly) *undervalued.*

We can take a look at the r-score to see that we achieved the same results as described in the article:


```python
r2_score(y, pred)
```




    0.94264680416237079



The data is current to 11/13 and shows Bitcoin at a predicted price of ~7000 USD and an actual price of ~6700 USD. Given that Bitcoin is currently trading at ~7200 USD on GDAX as of this writing (11/15), it seems that this model has some value.

This is probably not very useful for investment purposes, though, as the data generally lags too far behind what's actually happening. Still, it's interesting to see that Bitcoin userbase and trading volume appear to be closely correlated with price.

If you would like to explore this notebook yourself, you can download it [here]({attach}/downloads/predicting_bitcoin_price_metcalfe.ipynb). If you use conda/miniconda, you can use this [environment file]({attach}/downloads/env.yaml).
