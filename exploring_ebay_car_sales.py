#!/usr/bin/env python
# coding: utf-8

# ## Exploring eBay Car Sales Data

# We will analyze a dataset of used cars from eBay Kleinanzeigen, a [classifieds](https://en.wikipedia.org/wiki/Classified_advertising) section of the German eBay website.
# 
# The dataset was originally scraped and uploaded to Kaggle. It's not available on Kaggle anymore but you can find it [here](https://data.world/data-society/used-cars-data)
# 
# The version of the dataset we are working with is a sample of 50,000 data points that was prepared by Dataquest including simulating a less-cleaned version of the data.
# 
# The data dictionary provided with data is as follows:
# 
# - `dateCrawled` - When this ad was first crawled. All field-values are taken from this date.
# - `name` - Name of the car.
# - `seller` - Whether the seller is private or a dealer.
# - `offerType` - The type of listing
# - `price` - The price on the ad to sell the car.
# - `abtest` - Whether the listing is included in an A/B test.
# - `vehicleType` - The vehicle Type.
# - `yearOfRegistration` - The year in which the car was first registered.
# - `gearbox` - The transmission type.
# - `powerPS` - The power of the car in PS.
# - `model` - The car model name.
# - `odometer` - How many kilometers the car has driven.
# - `monthOfRegistration` - The month in which the car was first registered.
# - `fuelType` - What type of fuel the car uses.
# brand - The brand of the car.
# - `notRepairedDamage` - If the car has a damage which is not yet repaired.
# - `dateCreated` - The date on which the eBay listing was created.
# - `nrOfPictures` - The number of pictures in the ad.
# - `postalCode` - The postal code for the location of the vehicle.
# - `lastSeenOnline` - When the crawler saw this ad last online.
# 
# The aim of this project is to clean the data and analyze the included used car listings. 

# First, we need to import necessary packages, then load and read the data.

# In[1]:


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


# In[2]:


autos = pd.read_csv('autos.csv', encoding='Latin-1')


# Now, let's explore this dataset to know if any null values, then take a look first 5 rows.

# In[3]:


autos.info()


# In[4]:


autos.head()


# Here are some insights about this dataset:
# 
# - The dataset contains 20 columns, most of which are strings.
# - Some columns have null values, but none have more than ~20% null values.
# - The column names use [camelcase](https://en.wikipedia.org/wiki/Camel_case) instead of Python's preferred [snakecase](https://en.wikipedia.org/wiki/Snake_case) , which means we can't just replace spaces with underscores.

# ## Clean Columns

# In this step, we need to:
# 
# - Convert columns names from camelcase to snakecase.
# - Reword some of the column names based on the data dictionary to be more descriptive.

# In[5]:


autos.columns


# In[6]:


autos.rename({'dateCrawled':'date_crawled', 'offerType':'offer_type', 'vehicleType':'vehicle_type', 'yearOfRegistration':'registration_year', 'gearbox':'gear_box', 'powerPS':'power_ps', 'monthOfRegistration':'registration_month', 'fuelType':'fuel_type', 'notRepairedDamage':'unrepaired_damage','dateCreated':'ad_created', 'nrOfPictures':'num_photos', 'postalCode':'postal_code', 'lastSeen':'last_seen'}, axis=1, inplace=True)


# In[7]:


autos.head()


# ## Initial Exploration and Cleaning

# In[8]:


autos.describe(include='all')


# In table above, we can see there are many columns with NaN values because they are all text columns which can't be calculated and almost all values are the same such as: `seller`, `offer_type`, and `num_photos`. Let's investigate more these 3 columns.
# 
# 
# We can also convert numeric data stored as text to do more analyses. 
# 
# 

# In[9]:


autos['seller'].value_counts()


# In[10]:


autos['offer_type'].value_counts()


# In[11]:


autos['num_photos'].value_counts()


# Look like `seller` and `offer_type` only has 2 values. For `seller`, private sector appear 49999 times and only 1 time for public. The same thing happened in `offer_type` with 49999 times for offer and 1 times for request type.
# 
# For `num_photos`, there are only 1 value 0 for 50000 rows. Therefore, we can drop these 3 columns.

# In[12]:


autos = autos.drop(["num_photos", "seller", "offer_type"], axis=1)


# There are two columns, `price` and `odometer`, which are numeric values with extra characters being stored as text. We'll clean these columns by removing non-numeric characters and convert the column to a numeric type.
# 
# 

# In[13]:


new_price = []
for c in autos['price']:
    remove_symbol = c.strip('$')
    remove_comma = remove_symbol.replace(',', '')
    new_price.append(remove_comma)
autos['price'] = new_price


# In[14]:


new_odometer = []
for c in autos['odometer']:
    remove_km = c.strip('km')
    remove_comma = remove_km.replace(',', '')
    new_odometer.append(remove_comma)
autos['odometer'] = new_odometer


# In[15]:


autos.rename({'odometer':'odometer_km'}, axis=1, inplace=True)


# In[16]:


autos['price'] = autos['price'].astype(int)


# In[17]:


autos['odometer_km'] = autos['odometer_km'].astype(int)


# In[18]:


autos["price"].head()


# In[19]:


autos["odometer_km"].head()


# ## Exploring the Odometer and Price Columns

# In[20]:


autos["odometer_km"].value_counts()


# As observation, we can see that these value already rounded, which might indicate that sellers had to choose from pre-set options for this field. Moreover, there are more high mileage than low mileage vehicles.

# In[21]:


print(autos["price"].unique().shape)
print(autos["price"].describe())
autos["price"].value_counts().head(20)


# There are 2357 unique value in `price` column, and they seem already rounded. The highest price is 100 million and lowest price is 0 lead to an odd situation that we need to investigate more. 

# In[22]:


autos["price"].value_counts().sort_index(ascending=False).head(20)


# In[23]:


autos["price"].value_counts().sort_index(ascending=True).head(20)


# There are 14 items with a price higher than 900,000 dollars, 1 item nearly 100 million dollars. Moreover, there are 1,421 cars listed with 0 dollar.
# 
# Given that eBay is an auction site, there could legitimately be items where the opening bid is 1 dollar. Therefore, we will keep the item higher than $1 but remove anything above 350,000 dollars because it increase steadily to that price then suddenly jump to less realistic numbers.

# In[24]:


autos = autos[autos["price"].between(1,351000)]
autos["price"].describe()


# ## Exploring the date columns

# There are 5 columns that should represent date values. Some of these columns were created by the crawler, some came from the website itself. We can differentiate by referring to the data dictionary:
# 
# - `date_crawled`: added by the crawler
# - `last_seen`: added by the crawler
# - `ad_created`: from the website
# - `registration_month`: from the website
# - `registration_year`: from the website
# 
# First, let's take a look at `date_crawled`, `last_seen`, and `ad_created`.

# In[25]:


autos[['date_crawled','ad_created','last_seen']][0:5]


# In[26]:


autos['date_crawled'].str[:10].value_counts(normalize=True, dropna=False).sort_index()


# It seems like the site was crawled daily over a one month period in March and April 2016. The distribution of listings crawled on each day is roughly uniform.
# 
# 

# In[27]:


autos['ad_created'].str[:10].value_counts(normalize=True, dropna=False).sort_index()


# There were not many ads created in 2015 with the uniform distribution for each listing and one new car ad created over a period of 2 month. 
# 
# However, there were more ads created in 2016 due to more new listings on the web. On the table above, we can see the ad was created daily with difference frequency. 

# In[28]:


autos['last_seen'].str[:10].value_counts(normalize=True, dropna=False).sort_index()


# In `last_seen` column, the crawler recorded the date it last saw any listing, which allows us to determine on what day a listing was removed, presumably because the car was sold.
# 
# The last three days contain a disproportionate amount of `last_seen` values. The largest value around 10x compare to the value from the previous days, for instance, 0.22 on 2016-04-06 and 0.024 on 2016-04-04. The reason led to this situation might be because the ended of crawler and these value don't indicate car sales.

# ## Dealing with Incorrect Registration Year Data

# In[29]:


autos['registration_year'].describe()


# The year that the car was first registered will likely indicate the age of the car. Looking at this column, we note some odd values. The minimum value is 1000, before cars were invented, and the maximum is 9999, many years into the future.
# 
# Moreover, because a car can't be registered after the listing was seen on the web, therefore, any vehicle with a registration year after 2016 is definitely inaccurate. In addition, to determine the earliest year is more difficult becuase it could be somewhere in the first few decades of the 1900s.

# In[30]:


autos['registration_year'].value_counts().sort_index()


# In[31]:


autos['registration_year'].value_counts().sort_index(ascending=True).tail(15)


# In[32]:


(~autos["registration_year"].between(1900,2016)).sum() / autos.shape[0]


# Around 4% of the date outside the range 1900-2016, therefore, we can remove these rows. 

# In[33]:


autos = autos[autos["registration_year"].between(1900,2016)]
autos["registration_year"].value_counts(normalize=True).head(10)


# It appears that most of the vehicles were first registered in the past 20 years.

# ## Exploring Price by Brand
# 

# In[34]:


autos["brand"].value_counts(normalize=True).head(10)


# German manufacturers represent four out of the top five brands were listed on the web and almost 50% of the overall listings. Volkswagen is by far the most popular brand, with approximately double the cars for sale of the next two brands combined.
# 
# There are lots of brands that don't have a significant percentage of listings, so we will limit our analysis to brands representing more than 5% of total listings.

# In[35]:


brand_counts = autos["brand"].value_counts(normalize=True)
common_brands = brand_counts[brand_counts > .05].index
print(common_brands)


# In[37]:


brand_mean_prices = {}

for brand in common_brands:
    brand_filter = autos[autos['brand'] == brand]
    mean = brand_filter['price'].mean()
    brand_mean_prices[brand] = int(mean)
brand_mean_prices


# We can see that:
# 
# - Audi, Mercedes Benz, and BMW are the most expensive in the list.
# - Volkswagen is in middle price range. This could explain why this brand has the highest frequency above with 21%.
# - Ford and Opel are less expensive one.

# ## Storing Aggregate Data in a DataFrame

# In[38]:


bmp_series = pd.Series(brand_mean_prices)
pd.DataFrame(bmp_series, columns=["mean_price"])


# In[42]:


brand_mean_mileage = {}

for brand in common_brands:
    brand_filter = autos[autos['brand'] == brand]
    mean = brand_filter['odometer_km'].mean()
    brand_mean_mileage[brand] = int(mean)

mean_mileage = pd.Series(brand_mean_mileage).sort_values(ascending=False)
mean_prices = pd.Series(brand_mean_prices).sort_values(ascending=False)


# In[46]:


brand_info = pd.DataFrame(mean_mileage,columns=['mean_mileage'])
brand_info


# In[44]:


brand_info["mean_price"] = mean_prices
brand_info


# The range of car mileages does not vary as much as the prices do by brand, instead all falling within 10% for the top brands. There is a slight trend to the more expensive vehicles having higher mileage, with the less expensive vehicles having lower mileage.
