# helicopter
MSBD 5013 Project

## About this project
This is a quantitative trading model based on pairs trading. 

## How this strategy works

Finding similar pair of trading items is the foundation of pair trading. First, we transform history data into price changing rate. By definition, the commodities with similar price changing rate are similar items. So, by similarity metrics (cosine/knn/pearson correlation), we pick out the most similar pair of commodities.


Say we find out that A and B are the commodities with most similarity. Then we trade on these 2 items.

The trading steps are:

1. If the average price changing rate is positive, do step 2

2. If the difference of pricec changing rate satisfies with the condition of transaction fee rate, do step 3

3. Hold the commodity with lower price changing rate, until the price changing rate chases up.

## How to improve

1. We can trade on more commodities to hedge the risk.

2. With machine learning algorithms, we can calculate the "average price changing rate" with more accuracy.

3. We can modify selling point to get more interest.

