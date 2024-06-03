# Currency_Arbitrage
Arbitrage is the idea that because of inconsistency and differences in prices of assets/currencies in different markets, there exists a small, yet significant enough, spread to make a profit. 

We can identify opportunities using the well-known Floyd-Warshall Algorithm. After writing this code, I do believe that Bellman-Ford can also be used for a faster runtime, but it may be limited due to its nature as an algorithm with a single-source. 

We can transform this problem into a traditional graph problem by treating each currency as a node and the edges connecting them represent the exchange rate (if there exists a market between the two currencies). Our objective here is to find a positive weight cycle, but most of our typical algorithms do the opposite, solving for the shortest path or finding negative weighted cycles. We can transform the weight of the edges in the graph using the negative logarithm of the exchange rate to do this. Originally, I tried to just negate all the values, but because exchange rates require you to multiple them (2USD-JPY= 2USD * 157.2889(exchange rate)), it clearly failed. 

We adjust the graph G such that V = the currencies, E = u→v if there exists a market for the exchange between u and v and the weight of the edge is equal to -log(u to v exchange rate). By doing this we have transformed the problem successfully into a simple shortest-path problem. 

We can conclude that the runtime = O(n^2) for the data fetch, and O(n^3) for the FW algorithm leading to a total runtime of O(n^2) + O(n^3) = O(n^3). Here, n is the number of currencies (vertices). 
