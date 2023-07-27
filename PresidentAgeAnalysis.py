#!/usr/bin/env python
# coding: utf-8

# In[39]:


#import all required libraries
import pandas as pd 
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns


# In[2]:


# Load the CSV data into a DataFrame
df = df = pd.read_csv('U.S. Presidents Birth and Death Information - Sheet1.csv')


# In[7]:


#drop rows that don't have BIRTH DATE
df = df.dropna(subset=['BIRTH DATE'])

todays_date = pd.Timestamp.now().date()

#convert birth & death date columsn to datetime
df['BIRTH DATE'] = pd.to_datetime(df['BIRTH DATE'])
df['DEATH DATE'] = pd.to_datetime(df['DEATH DATE'])

#fill in missing values
df['DEATH DATE'].fillna(todays_date)

print(df.dtypes)


# In[16]:


#Addition of new features to the data

df['year_of_birth'] = df['BIRTH DATE'].dt.year
df['lived_years'] = df['DEATH DATE'].dt.year - df['BIRTH DATE'].dt.year
df['lived_months'] = round(((df['DEATH DATE'] - df['BIRTH DATE'])/np.timedelta64(1, 'M')), 2)
df['lived_days'] = (df['DEATH DATE'] - df['BIRTH DATE']).dt.days
df


# In[58]:


#sort values based on 'lived_days' in ascending order and get first 10 rows
shortest_lived = df.sort_values(by=['lived_days'], ignore_index=True).head(10)

#rename & display only required columns
shortest_lived = shortest_lived[['PRESIDENT','year_of_birth', 'lived_years', 'lived_days']]
shortest_lived.rename(columns = {"year_of_birth" : "Birth Year",
                               "lived_years": "Age",
                               "lived_days": "Days Lived"}, inplace=True)
print("TOP 10 Presidents from shortest to longest lived")
shortest_lived


# In[59]:


#Get shortest lived presidents amongst deceased presidents

deceased_presidents = df[df['LOCATION OF DEATH'].notnull()]
shortest_lived_deceased = df.sort_values(by=['lived_days'], ignore_index=True).head(10)

#rename & display only required columns
shortest_lived_deceased = shortest_lived_deceased[['PRESIDENT','year_of_birth', 'lived_years', 'lived_days']]
shortest_lived_deceased.rename(columns = {"year_of_birth" : "Birth Year",
                               "lived_years": "Age",
                               "lived_days": "Days Lived"}, inplace=True)

print("TOP 10 Deceased Presidents from shortest to longest lived")
shortest_lived_deceased


# In[60]:


#sort values based on 'lived_days' in descending order and get first 10 rows
longest_lived = df.sort_values(by=['lived_days'], ascending=False, ignore_index=True).head(10)

#rename & display only required columns
longest_lived = longest_lived[['PRESIDENT','year_of_birth', 'lived_years', 'lived_days']]
longest_lived.rename(columns = {"year_of_birth" : "Birth Year",
                               "lived_years": "Age",
                               "lived_days": "Days Lived"}, inplace=True)
print("TOP 10 Presidents from longest to shortest lived")
longest_lived


# In[61]:


#Get longest to shortest amongst living presidents
living_presidents = df[df['LOCATION OF DEATH'].isnull()]
longest_living = living_presidents.sort_values(by=['lived_days'], ascending=False, ignore_index=True)

#rename & display only required columns
longest_living = longest_living[['PRESIDENT','year_of_birth', 'lived_years', 'lived_days']]
longest_living.rename(columns = {"year_of_birth" : "Birth Year",
                               "lived_years": "Age",
                               "lived_days": "Days Lived"}, inplace=True)

print("Longest to Shortest LIVING presidents")
longest_living


# In[62]:


#calculate metrics from the newly created dataset
mean = round(df['lived_days'].mean(),2)
weighted_avg = round((sum(df['lived_days'] * df['lived_years']) / sum(df['lived_years'])),2)
median = df['lived_days'].median()
mode = df['lived_days'].mode().iloc[0]
max_value = df['lived_days'].max()
min_value = df['lived_days'].min()
std_deviation = round(df['lived_days'].std(), 2)

metrics = pd.DataFrame({
    'Metric': ['Mean','Weighted Average', 'Median', 'Mode', 'Maximum Value', 'Minimum Value', 'Standard Deviation'], 
    'Value': [mean, weighted_avg, median, mode, max_value, min_value, std_deviation]})

metrics


# In[52]:


#Histogram with Kernal Density Estimation
sns.histplot(df['lived_years'], kde=True, bins=20)

plt.xlabel('Lived Years')
plt.ylabel('Number of Presidents')
plt.show()


# In[63]:


#plot frequency distribution of different age groups
labels=['45-50', '50-55', '55-60', '60-65', '65-70', '70-75', '75-80', '80-85', '85-90', '90-95', '95-100']
age_group= pd.cut(df['lived_years'], bins=[45,50,55,60,65,70,75,80,85,90,95,100], labels=labels)
ax = age_group.value_counts().sort_index().plot.bar()
plt.xlabel('Age Groups')
plt.ylabel('Number of Presidents')
plt.show()


# In[ ]:




