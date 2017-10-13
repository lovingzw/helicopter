# helicopter
MSBD 5013 Project

## About this project
This is a quantitative trading model based on pairs trading. 

## How this strategy works

Finding similar pair of trading items is the foundation of pair trading. First, we transform history data into price changing rate. By definition, the commodities with similar price changing rate are similar items. So, by similarity metrics (cosine/knn/pearson correlation), we pick out the most similar pair of commodities.


Say we find out that A and B are the commodities with most similarity. Then we trade on these 2 items.

The trading steps are:

1. Set status = 0

Loop

2. If status = 0, do step 3; Else, do step 8

3. If the difference of price changing rate satisfies with the condition of transaction fee rate, do step 4








4. Set status = 1

5. Calculate the average price changing rate to determine their global trend

6. If the global trend goes up, hold the commodity with lower price changing rate. Else, do the opposite

7. Back to step 2

8. If the price changing rate of the item we hold chases up, close out

9. Set status = 0

## How to improve

1. We can trade on more commodities to hedge the risk.

2. With machine learning algorithms, we can calculate the "average price changing rate" with more accuracy.

3. We can modify selling point to get more interest.

