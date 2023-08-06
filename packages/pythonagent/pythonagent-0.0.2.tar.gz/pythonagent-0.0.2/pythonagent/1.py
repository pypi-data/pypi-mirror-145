class NDHavocException(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)


def common_failure(exception_message):
    raise NDHavocException(exception_message)

try:
    #common_failure("Test")
    a = 10 / 0
except Exception as e:
    if isinstance(e, NDHavocException):
        print("Yes")
    else:
        print("No")

    #print(type(e))
    # raise e 
