from ingestor.common.constants import USER_CONTENT_RELATIONSHIP_LABEL, \
    CONTENT, CONTENT_ID, CUSTOMER_ID
from ingestor.user_profile.network.plot_relations import PlotRelations
from pandas import DataFrame

class UCNetworkGenerator(PlotRelations):

    def __init__(
            self,
            data: DataFrame,
            connection_uri
    ):
        """
        Calls the parent class used in user profile
        network generation.
        :param data: dataframe object pandas
        :param connection_uri: graphDB connection URI
        """
        PlotRelations.__init__(
            self,
            data=data,
            label=USER_CONTENT_RELATIONSHIP_LABEL,
            connection_uri=connection_uri
        )

    def filter_features(
            self
    ):
        """
        Filters to keep only the required fields
        :return: None, simply updates the state of
        instance data member
        """
        self.data = self.data[[CUSTOMER_ID,
                               CONTENT]]

    def create_relationships(
            self
    ):
        """
        Generate relationships between user and
        content nodes using the controller function
        of parent class
        :return:None, simply updates the state of graphDB
        """
        self.filter_features()
        self.controller(
            destination_prop_label=CONTENT_ID
        )