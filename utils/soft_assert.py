class SoftAssert:
    def __init__(self):
        self._errors = []

    def assert_equal(self, actual, expected, message=""):
        try:
            assert actual == expected, message
        except AssertionError as e:
            self._errors.append(str(e))

    def assert_true(self, condition, message=""):
        try:
            assert condition, message
        except AssertionError as e:
            self._errors.append(str(e))

    def assert_all(self):
        if self._errors:
            raise AssertionError("Soft assertion errors occurred:\n" + "\n".join(self._errors))
