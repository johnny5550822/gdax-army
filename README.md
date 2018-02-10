# gdax-army
A repository to provide automatic trading bot to trade $-to-coin on GDAX using [gdax-python API](https://github.com/danpaquin/gdax-python).

Maintainers - [Johnny Ho](https://github.com/johnny5550822), [Panayiotis Petousis](https://github.com/panas89)

## Warming
This repository is for non-commercial use and for research purpose. Please use it in caution and it DOES NOT guranttee to earn profit. Please report any bugs.

## Contributing
Please feel free to [pull requests](https://github.com/johnny5550822/gdax-army/pulls).

#### Pull Request Guidelines
- Please follow as close as [pep-0008](https://www.python.org/dev/peps/pep-0008/) coding guidelines, such as having at most 79 characters in a line.
- REMEMBER to remove your credentials in code everytime before you push to master branch. 
- Code in pythonic way. 
- We follow KISS (Keep it simple, stupid!) for the design principle, and OOP for design pattern.
- If you are using subl, please auto format it following PEP-8 standard, [tutorial](https://packagecontrol.io/packages/Python%20PEP8%20Autoformat).
- When you write tests, please follow the convention in sampleUnitTest.py.  

## Code Organization
```bash
run.py - the main for all parameters setup.
lib/Trader.py - the core class to handle trading logic.
lib/Strategier.py - the parent class to provides functionalities for buy & sell.
lib/BuyStrategier.py - the child class to provide specific buy strategy.
lib/SellStrategier.py - the child class to provide specific sell strategy.
lib/GdaxArmy.py - the API class for gdax-python, and GDAX authentication.
lib/utils.py - utilities functions.
test/ - unit tests.
logs/ - [DATE]_log.log for comprehensive log and [DATE]_trade.log for precise transaction.
ext/ - experimental python notebooks.
```

## To run
Input your gdax API keys in run.py [lines 10-12](https://github.com/johnny5550822/gdax-army/blob/b310de96fb47ce526a39498a0321c763511f441f/run.py#L10). And then do:
```bash
python run.py
```

## Trading Assumption
- We provided a good-to-go solution (with buy & sell strategies) for simple trading in GDAX. We assume one-buy-one-sell trading cycle. That is, after one buy, we sell to complete a cycle.

## License
The MIT License (MIT)
