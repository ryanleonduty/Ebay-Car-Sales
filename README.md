# Ebay Car Sales

### Project Overview

This project delves into the analysis of a dataset of used cars from eBay Kleinanzeigen, the classifieds section of the German eBay website. Originally scraped and uploaded to Kaggle, this particular dataset comprises a sample of 50,000 data points, specifically prepared by Dataquest to simulate a less-clean version for educational purposes.

### Dataset

The dataset offers a comprehensive look into the used car market, featuring details such as the date an ad was crawled, car names, seller type, offer types, prices, and many more attributes related to the cars being sold. Notably, it includes fields like vehicle type, year of registration, gearbox type, power in PS, car model, odometer readings, and the month of registration, among others. This wealth of information facilitates a rich analysis of the used car listings, allowing for insights into pricing trends, popular car models, and other aspects of the second-hand car market.

### Objectives
The primary aim of this project is to clean and analyze the used car listings included in the dataset. This involves:

- Importing necessary Python packages.
- Loading and reading the data.
- Identifying and handling missing or null values.
- Converting column names from camelcase to Python's preferred snakecase to facilitate data handling.
- Performing exploratory data analysis to uncover key trends and insights.

### Insights and Findings

This project uncovers several compelling insights about the used car market on eBay Kleinanzeigen. Some of the key findings include:

- Price Trends: We observed a wide range of car prices, from surprisingly low to exceptionally high values. Upon closer examination, it became clear that the very low prices were often due to cars being listed as 'for parts' or having significant damage. High-end prices typically corresponded to luxury brands and newer vehicles in excellent condition.

- Brand Popularity: Certain car brands emerged as more popular among sellers, indicating potential trends in consumer preference or brand reliability. For instance, German manufacturers like Volkswagen, BMW, and Mercedes-Benz had a significant presence in the listings, reflecting their popularity in the domestic market.

- Vehicle Age vs. Price: As expected, there was a general trend of decreasing price with increasing vehicle age. However, classic cars and well-maintained vehicles from sought-after brands sometimes defied this trend, fetching higher prices despite their age.

- Geographical Variations: Analysis of the postal code data revealed interesting geographical patterns in the listings. Certain areas had higher concentrations of luxury car listings, possibly reflecting the economic status of the region.

- Condition and Price: The dataset allowed for an analysis of how a car's condition impacts its selling price. Cars listed with no unrepaired damage or with a recent registration date generally commanded higher prices, underscoring the importance of vehicle condition in the used car market.

- Transmission Types: Manual and automatic transmissions showed distinct pricing patterns, with automatic vehicles often priced higher. This difference might be attributed to the perceived convenience of automatic transmissions and their prevalence in higher-end car models.

These findings offer a glimpse into the dynamics of the used car market, highlighting the factors that influence car prices and seller behavior on eBay Kleinanzeigen. The project demonstrates the power of data analysis in uncovering market trends and consumer preferences, providing valuable insights for potential buyers, sellers, and market analysts alike.

### Usage
This project is intended for anyone interested in data analysis, particularly in the context of the used car market. It serves as an example of how to clean a real-world dataset and extract meaningful insights from it.
