# gdax-army
A bot to trade on gdax api

# Notes
- we need to place at least 0.01 BTC for buy or sell in the limit or market order
- let say we place a limit order, a, on sell, if we then place a market order, b, on buy (bigger than the limit order sell), we will reduce the b by b-a=c, and fullfill c by the current market price. 
