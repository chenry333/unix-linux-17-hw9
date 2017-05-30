class InvalidUsage(Exception):
    """
    InvalidUsage Exception
    facilitates passing back json data with a 4xx status code
    """
    def __init__(self, output, success, status_code=400):
        Exception.__init__(self)
        self.output = output
        self.success = success
        self.status_code = status_code

    def to_dict(self):
        ret_dict = {}
        ret_dict['output'] = self.output
        ret_dict['success'] = self.success
        return ret_dict
