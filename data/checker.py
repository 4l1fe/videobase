

class FactChecker(object):

    checkers = {}
    correctors = {}

    def __init__(self, target_type):

        self.target_type = target_type

    def add(self, message, corrector = None):

        def wrapper(func):
            self.checkers[message] = func
            if not corrector is None:
                self.correctors[message] = corrector
        return wrapper

    def check(self, target):
        if not (type(target) is self.target_type):
            raise NameError("Wrong type of data. Expected {}, got {}".format(self.target_type, type(target)))
        else:
            failures = [name for name in self.checkers if not self.checkers[name](target)]
            return failures

    def check_and_correct(self, target):
        failures = self.check(target)
        for failure in failures:
            if failure in self.correctors:
                self.correctors[failure](target)
        return self.check(target)


