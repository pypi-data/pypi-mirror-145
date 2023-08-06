from typing import ClassVar

from graphdb import GraphDb, GraphDbConnection
from graphdb.schema import Node, Relationship
from pandas import DataFrame

# LABEL NODE NAME & VARIABLE NAME
from ingestor.common.constants import LABEL, CONTENT, PROPERTIES, RELATIONSHIP, CATEGORY, SUBCATEGORY, COUNTRY, \
    CONTENT_ID, HOMEPAGE, ACTORS, TAGS, PACKAGES, PRODUCTS, ACTOR, PRODUCT, PACKAGE, CONTENT_CORE, HOMEPAGE_ID, \
    IS_CONNECTED, PAY_TV_CONTENT, NO_PAY_TV_CONTENT, YES
# RELATIONSHIP NAME
from ingestor.content_profile.config import content_node_properties, HAS_CATEGORY, HAS_SUBCATEGORY, HAS_COUNTRY, \
    HAS_ACTOR, HAS_TAG, HAS_PRODUCT, HAS_PACKAGE, HAS_HOMEPAGE, HAS_CONTENT_CORE
from ingestor.content_profile.network.content_utils import ContentUtils
from ingestor.content_profile.network.similarity_utils import SimilarityUtils


class ContentNetworkGenerator:

    def __init__(
            self,
            connection_class: GraphDbConnection
    ):
        self.graph = GraphDb.from_connection(connection_class)

    @classmethod
    def from_connection_uri(
            cls,
            connection_uri: str
    ) -> ClassVar:
        """Create new object based on connection uri
        :param connection_uri: string connection uri
        :return: object class
        """
        return cls(GraphDbConnection.from_uri(connection_uri))

    @classmethod
    def from_connection_class(
            cls,
            connection_class: GraphDbConnection
    ) -> ClassVar:
        """Define new class based on object connection
        :param connection_class: object connection class
        :return: object class
        """
        return cls(connection_class)

    @staticmethod
    def build_content_label(home_page):
        if home_page[0].properties[IS_CONNECTED].lower() == YES:
            content_label = PAY_TV_CONTENT
        else:
            content_label = NO_PAY_TV_CONTENT
        return content_label

    def create_content_homepage_network(self, payload: DataFrame):
        content_nodes = []
        if HOMEPAGE in payload.columns:
            for props in payload[HOMEPAGE].loc[0]:
                static_node = Node(**{LABEL: HOMEPAGE, PROPERTIES: props})
                home_page = self.graph.find_node(static_node)

                content_label = self.build_content_label(home_page)
                print("Generating content to homepage network for content label {0}".format(content_label))
                for property_num, property_val in payload.iterrows():
                    content_node_dict = {}
                    if property_val[CONTENT_ID] and property_val[CONTENT_ID] is not None and \
                            property_val[CONTENT_ID] != '':
                        content_node_property = content_node_properties(property_val)
                        content_node = Node(**{LABEL: content_label, PROPERTIES: content_node_property})
                        content_node = self.graph.create_node(content_node)
                        if len(home_page) == 0:
                            print("Record not available in static network for node {0}".format(static_node))
                        else:
                            self.graph.create_relationship_without_upsert(content_node, home_page[0], Relationship(
                                **{RELATIONSHIP: HAS_HOMEPAGE}))
                        content_node_dict[LABEL] = content_label
                        content_node_dict[HOMEPAGE_ID] = home_page[0].properties[HOMEPAGE_ID]
                        content_node_dict[CONTENT] = content_node
                        content_nodes.append(content_node_dict)

        else:
            print("Homepage feature is not available")
        return content_nodes

    def child_network_generator(self, content_node, feature, label, relationship, payload: DataFrame):
        if feature in payload.columns:
            for props in payload[feature].loc[0]:
                static_node = Node(**{LABEL: label, PROPERTIES: props})
                node_in_graph = self.graph.find_node(static_node)
                if len(node_in_graph) == 0:
                    print("Record not available in static network for node {0}".format(static_node))
                else:
                    self.graph.create_relationship_without_upsert(content_node, node_in_graph[0],
                                                                  Relationship(**{RELATIONSHIP: relationship}))
        else:
            print("Feature not available")
        return content_node

    def child_network_generator_2(self, content_node, feature, label, relationship, payload: DataFrame):
        if feature in payload.columns:
            for props in payload[feature].loc[0]:
                final_content_core_props = ContentUtils.prepare_content_core_properties(props, self.graph)
                final_content_core_node = Node(**{LABEL: label, PROPERTIES: final_content_core_props})

                final_content_core_node = self.graph.create_node(final_content_core_node)

                self.graph.create_relationship_without_upsert(content_node, final_content_core_node,
                                                              Relationship(**{RELATIONSHIP: relationship}))
        else:
            print("Feature not available")

        return content_node

    def content_creator_updater_network(self, payload: DataFrame) -> bool:
        print("Generating content node")
        content_nodes = self.create_content_homepage_network(payload=payload)
        if len(content_nodes) > 0:
            temp_storage = []
            for record in content_nodes:
                content_label = record[LABEL]
                content_node = record[CONTENT]
                content_homepage_id = record[HOMEPAGE_ID]
                if content_node not in temp_storage:
                    print("Generating content to category network")
                    content_node = self.child_network_generator(content_node, CATEGORY, CATEGORY, HAS_CATEGORY,
                                                                payload=payload)
                    print("Generating content to subcategory network")
                    content_node = self.child_network_generator(content_node, SUBCATEGORY, SUBCATEGORY, HAS_SUBCATEGORY,
                                                                payload=payload)
                    print("Generating content to country network")
                    content_node = self.child_network_generator(content_node, COUNTRY, COUNTRY, HAS_COUNTRY,
                                                                payload=payload)
                    print("Generating content to actor network")
                    content_node = self.child_network_generator(content_node, ACTORS, ACTOR, HAS_ACTOR, payload=payload)
                    print("Generating content to tag network")
                    content_node = self.child_network_generator(content_node, TAGS, TAGS, HAS_TAG, payload=payload)
                    print("Generating content to product network")
                    content_node = self.child_network_generator(content_node, PRODUCTS, PRODUCT, HAS_PRODUCT,
                                                                payload=payload)
                    print("Generating content to package network")
                    content_node = self.child_network_generator(content_node, PACKAGES, PACKAGE, HAS_PACKAGE,
                                                                payload=payload)
                    print("Generating content to content core network")
                    content_node = self.child_network_generator_2(content_node, CONTENT_CORE, CONTENT_CORE,
                                                                  HAS_CONTENT_CORE,
                                                                  payload=payload)
                    temp_storage.append(content_node)
                print("Updating similarity property in content nodes")
                SimilarityUtils.add_content_similarity_property(content_node, content_label, content_homepage_id,
                                                                self.graph)
        else:
            print("No content node is available")
        return True
