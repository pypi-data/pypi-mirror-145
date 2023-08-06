from ingestor.common.constants import HOMEPAGE_ID, IS_CONNECTED
# RELATIONSHIP NAME
from ingestor.content_profile.config import HAS_HOMEPAGE


class QueryUtils:

    @staticmethod
    def get_contents_based_on_homepage_id(connected_flag, content_homepage_id, graph):
        homepage_network = []
        list_homepage_ids = []
        query_network = graph.custom_query(f'''
                    g.V().has('{HOMEPAGE_ID}',{content_homepage_id}).has('{IS_CONNECTED}',
                                '{connected_flag}').in('{HAS_HOMEPAGE}').valueMap().by(unfold()).toList()
                    ''', payload={
            HOMEPAGE_ID: content_homepage_id,
            IS_CONNECTED: connected_flag,
            HAS_HOMEPAGE: HAS_HOMEPAGE
        })
        homepage_network.append(query_network)
        list_homepage_ids.append(content_homepage_id)
        return homepage_network, list_homepage_ids

    @staticmethod
    def get_all_content(content_label, graph):
        query = graph.custom_query(f'''
        g.V().hasLabel('{content_label}').valueMap().by(unfold()).toList()
        ''', payload={
            content_label: content_label
        })
        return query
