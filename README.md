# gdax-army
A bot to trade on gdax api

# To run
log.log will store all the outputs from the script.
```bash
python run.py
```

# Assumptions
- We assume one-buy-one-sell trading cycle. That is, after one buy, we sell to complete the cycle.

# Repo Notes
- We should only keep one single straight global/master history (i.e., we can branch in local, but not in global/master.)
- Please follow as close as pep-0008 for coding (https://www.python.org/dev/peps/pep-0008/), such as having at most 79 characters in a line
- REMEMBER to remove your credentials in code and online everytime before you push to master branch. 
- Code in pythonic way. 
- We follow KISS (Keep it simple, stupid!) for the design principle, and OOP for design pattern.
- Try to look for a good design pattern, e.g., facade 
	- https://www.toptal.com/python/python-design-patterns
	- https://github.com/faif/python-patterns
- If you are using subl, please auto format it following PEP-8 standard
    - https://packagecontrol.io/packages/Python%20PEP8%20Autoformat
- When you write tests in test, please follow the convention in sampleUnitTest.py. Also, please name the test python file accordingly. 

# Trading Strategy Notes
- 12/27/17 If we buy at high price (e.g., $282) and using the macd rule. Let say the price suddenly go down a lot, so the ema-12 and ema-26 will be lowering. Even we use the rule ema-12 < ema-26, we cannot sell the stock because the selling rule is 'return (short_macd_ema < long_macd_ema) and (price > buy_price)', so I have to remove (price > buy_price) in order to sell the stock. But then, hmm..., how do we handle this situation, like we buy in high price following macd rule, and then the price drops. 

- 12/27/17 The granularity is important because that affects ema value. I did one experiment with 5min and 12-, 26- ema, seem like the if I use macd rules, the actual price that I am buying is not good, for example. I buy at 263.70 and sell at 261.69 based on macd rules. Look like 1-min or 15-min is better. 2017-12-27 11-32-52

- 12/27/17 Seem like it took a long time to buy/sell after placing the order if the price is in the third/fourth position (probably because other algorithms are doing this too), so we will just buy/sell in the first position and see what happened. Grandularity:1min, 12-ema, 26-ema. 2017-12-27 15-08-44

- 12/28/17 Look like 12-ema and 26-ema is pretty sensitive to small little up or down, which is not good. Will has a lot of false positive (earning opportunity), will change 26-ema to 36-ema. 2017-12-27_18-03-23_trade.log

- 12/29/17 Even though I used 36-ema, look like the problem still exists, i.e., if the up is not enough, I may end up losing $$ instead of earning $$. Because using macd cross line to determine the buy-in tell has already some delayed i nthe rise of the price, in which it can already gone up to certain point, and then use macd cross line to determine sell price will has some delay as well. At the end, if the up and down is not big enough, we will lose money because we buy at high price and sell at lower price. Let the conclusion is I will add one more rule to determine if I sell or not, which if the price is at least x% gain (like 1% to 2%) I will sell the stock. 2017-12-28_11-49-10_trade.log

- 01/02/18 GG... there is a bug (trade_option) that make me not able to proceed correctly with buy trade option... Redo experiment with seperating possible buy and sell option. 2017-12-29_17-32-25_log.log

- 01/03/18 Hmm... a lot of buy-in and buy-out and then seem like I need to make the long ema from 36 to 26. Also add more log to look at the actual price fluatation. 2018-01-02_15-04-39_log.log

- 01/06/18 SOmetime we will accendially placed >1 buy orders... I checked and found that there can be "No json" object detection in the buy order while loop, in which we have exception to handle it. Yet, the placed buy order will lose track and we will place another buy order. I debug it, i.e., cancell all orders at the beginning of while loop for buy/sell. 2018-01-04_18-11-01_log.log

- 01/13/18 There are two extra buys in this experiment. I found that this is because _wait_order_complete() function has problem in which I checked if order is completed and then wait for certain time and then return. That's not correct. It should wait and then check and then wait again. 2018-01-06_12-14-32_log.log

- 01/19/18 Debug the weird more-buy-than-sell orders and exceptions 2018-01-18_10-47-02_log.log