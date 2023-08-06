from graphdb.schema import Node

from ingestor.common.constants import LABEL, PROPERTIES, CONTENT_ID, CC_SIMILARITY_SCORE, ALL_SIMILARITY_SCORE, \
    PAY_TV_CONTENT, YES, NO
from ingestor.content_profile.content_similarity import cluster_data_to_df, generate_new_features, \
    generate_tfidf_matrix, calculate_cosine_similarity, cluster_data_to_single_df, combine_features, create_tfidf_df, \
    calculate_single_cosine_similarity
from ingestor.content_profile.network.query_utils import QueryUtils


class SimilarityUtils:

    @staticmethod
    def add_similarity_property(content_node, list_dict_content_similarities, list_homepage_id, graph, content_label):
        content_similarity_property = {}
        for (homepage_id, dict_content_similarities) in zip(list_homepage_id, list_dict_content_similarities):
            for key, value in dict_content_similarities.items():
                output_type = {homepage_id: value}
                content_similarity_property.setdefault(key, [])
                content_similarity_property[key].append(output_type)

        for content_id, sim_property in content_similarity_property.items():
            node_to_update = Node(**{LABEL: content_label, PROPERTIES: {CONTENT_ID: int(content_id)}})
            query_content_node = graph.find_node(node_to_update)
            dict_similarity_score = dict(sum(map(list, map(dict.items, sim_property)), []))
            graph.update_node_property(query_content_node[0], {CC_SIMILARITY_SCORE: str(dict_similarity_score)})
        return content_node

    @staticmethod
    def add_all_content_similarity_property(content_node, all_content_dict_cos_sim, content_label, graph):
        for key, value in all_content_dict_cos_sim.items():
            node_to_update = Node(**{LABEL: content_label, PROPERTIES: {CONTENT_ID: int(key)}})
            query_content_node = graph.find_node(node_to_update)
            graph.update_node_property(query_content_node[0], {ALL_SIMILARITY_SCORE: str(value)})
        return content_node

    @staticmethod
    def add_content_similarity_all_content(content_node, content_label, graph):
        all_content_cluster = QueryUtils.get_all_content(content_label, graph)
        all_content_df = cluster_data_to_single_df(all_content_cluster)
        all_content_new_df = combine_features(all_content_df, graph, content_label)
        all_content_tfidf = create_tfidf_df(all_content_new_df)
        all_content_dict_cos_sim = calculate_single_cosine_similarity(all_content_tfidf)
        output_all_content_similarity = SimilarityUtils.add_all_content_similarity_property(content_node,
                                                                                            all_content_dict_cos_sim,
                                                                                            content_label, graph)
        return output_all_content_similarity

    @staticmethod
    def add_content_similarity_property(content_node, content_label, content_homepage_id, graph):
        # Calculate Content-Similarity in Homepage_id Wise
        if content_label == PAY_TV_CONTENT:
            connected_flag = YES
        else:
            connected_flag = NO

        list_homepage_network, list_homepage_ids = QueryUtils.get_contents_based_on_homepage_id(connected_flag,
                                                                                                content_homepage_id,
                                                                                                graph)
        list_dataframe_homepage = cluster_data_to_df(list_homepage_network)
        list_new_df_homepage = generate_new_features(list_dataframe_homepage, graph, content_label)
        list_tfidf_df = generate_tfidf_matrix(list_new_df_homepage)
        list_dict_content_similarities = calculate_cosine_similarity(list_tfidf_df)
        SimilarityUtils.add_similarity_property(content_node, list_dict_content_similarities, list_homepage_ids, graph,
                                                content_label)
        SimilarityUtils.add_content_similarity_all_content(content_node, content_label, graph)
        return content_node
