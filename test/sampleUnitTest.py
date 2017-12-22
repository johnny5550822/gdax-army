import unittest

'http://www.onlamp.com/pub/a/python/2004/12/02/tdd_pyunit.html'
'https://jeffknupp.com/blog/2013/12/09/improve-your-python-understanding-unit-testing/'

# Here's our "unit".


def IsOdd(n):
    return n % 2 == 1

# Here's our "unit tests".


class IsOddTests(unittest.TestCase):

    def testOne(self):
        self.failUnless(IsOdd(1))

    def testTwo(self):
        self.failIf(IsOdd(2))

    def testThree(self):
        pass


def main():
    unittest.main()

if __name__ == '__main__':
    main()
