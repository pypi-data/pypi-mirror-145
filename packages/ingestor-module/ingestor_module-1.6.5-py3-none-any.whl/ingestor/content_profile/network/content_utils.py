from graphdb import Node
from pandas import DataFrame

from ingestor.common import CONTENT_CORE_ID, SEASON_ID, LABEL, SEASON, PROPERTIES, SEASON_NAME, CONTENT_CORE_SYNOPSIS, \
    CONTENT_CORE_SYNOPSIS_EN, CONTENT_CORE, CONTENT_CORE_TITLE, CONTENT_CORE_EPISODE, CREATED_ON, MODIFIED_ON, \
    CONTENT_ID
from ingestor.content_profile.config import content_node_properties


class ContentUtils:

    @staticmethod
    def find_static_node(payload: DataFrame, feature, label, graph):
        static_node_list = []
        if feature in payload.columns:
            for props in payload[feature].loc[0]:
                static_node = Node(**{LABEL: label, PROPERTIES: props})
                node_in_graph = graph.find_node(static_node)
                if len(node_in_graph) == 0:
                    print("Record not available in static network for node {0}".format(static_node))
                else:
                    node = node_in_graph
                    static_node_list.append(node)
        else:
            print("Feature not available")
        return static_node_list

    @staticmethod
    def prepare_content_properties(payload: DataFrame):
        content_node_property = None
        for property_num, property_val in payload.iterrows():
            if property_val[CONTENT_ID] and property_val[CONTENT_ID] is not None and \
                    property_val[CONTENT_ID] != '':
                content_node_property = content_node_properties(property_val)
        return content_node_property

    @staticmethod
    def prepare_content_core_properties(props, graph):
        final_content_core_props = {}
        if CONTENT_CORE_ID in props:
            ContentUtils.add_content_core_properties(final_content_core_props, props, graph)
            ContentUtils.add_content_core_synopsis(final_content_core_props, props, graph)
            ContentUtils.add_season(final_content_core_props, props, graph)
        return final_content_core_props

    @staticmethod
    def add_season(final_content_core_props, props, graph):
        if SEASON_ID in props:
            node_content_season = Node(**{LABEL: SEASON, PROPERTIES: {SEASON_ID: props[SEASON_ID]}})
            node_content_season = graph.find_node(node_content_season)
            final_content_core_props[SEASON_NAME] = node_content_season[0].properties[SEASON_NAME]

    @staticmethod
    def add_content_core_synopsis(final_content_core_props, props, graph):
        node_content_core_synopsis = Node(
            **{LABEL: CONTENT_CORE_SYNOPSIS, PROPERTIES: {CONTENT_CORE_ID: props[CONTENT_CORE_ID]}})
        node_content_core_synopsis = graph.find_node(node_content_core_synopsis)
        if len(node_content_core_synopsis) > 0:
            final_content_core_props[CONTENT_CORE_SYNOPSIS] = node_content_core_synopsis[0].properties[
                CONTENT_CORE_SYNOPSIS]
            final_content_core_props[CONTENT_CORE_SYNOPSIS_EN] = node_content_core_synopsis[0].properties[
                CONTENT_CORE_SYNOPSIS_EN]

    @staticmethod
    def add_content_core_properties(final_content_core_props, props, graph):
        node_content_core = Node(
            **{LABEL: CONTENT_CORE, PROPERTIES: {CONTENT_CORE_ID: props[CONTENT_CORE_ID]}})
        node_content_core = graph.find_node(node_content_core)
        final_content_core_props[CONTENT_CORE_ID] = node_content_core[0].properties[CONTENT_CORE_ID]
        final_content_core_props[CONTENT_CORE_TITLE] = node_content_core[0].properties[CONTENT_CORE_TITLE]
        final_content_core_props[CONTENT_CORE_EPISODE] = node_content_core[0].properties[CONTENT_CORE_EPISODE]
        final_content_core_props[CREATED_ON] = node_content_core[0].properties[CREATED_ON]
        final_content_core_props[MODIFIED_ON] = node_content_core[0].properties[MODIFIED_ON]