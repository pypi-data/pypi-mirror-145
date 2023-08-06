class DataModel:
    """

    """

    def __init__(self, config):
        """
        Instantiates the class, and if possible initializes the data model for use
        :param config: All configuration needed for the data model to operate
        """
        self.config = config

    def build(self, target=None, environment=None):
        """
        Build the database model
        :return:
        """
