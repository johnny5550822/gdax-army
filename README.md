# gdax-army
A bot to trade on gdax api

# To run
log.log will store all the outputs from the script.
```bash
python run.py
```

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

-12/28/17 Look like 12-ema and 26-ema is pretty sensitive to small little up or down, which is not good. Will has a lot of false positive (earning opportunity), will change 26-ema to 36-ema. 2017-12-27_18-03-23_trade.log

