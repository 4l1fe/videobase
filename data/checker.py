

class FactChecker(object):

    checkers = {}

    def __init__(self, target_type):

        self.target_type = target_type

    def add(self,message):

        def wrapper(func):
            self.checkers[message] = func
        return wrapper


    def check(self, target):

        if  not (type(target) is self.target_type):
            raise NameError("Wrong type of data. Expected {}, got {}".format(self.target_type,type(target)))
        else:
            failures = [ name for name in self.checkers if not self.checkers[name](target)]
            return failures
            