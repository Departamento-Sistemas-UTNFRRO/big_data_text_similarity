import uuid, math
import numpy as np
from utils import general_utils as gu
from ensembles.dao import ensembles_dao


class PamHelper:
    def __init__(self, n, k_array):
        self.n = n
        self.k_array = k_array

    def calculate_max_k(self):
        return math.floor(math.sqrt(self.n))

    def calculate_initial_medoids(self, k):
        return np.random.randint(0, self.n - 1, k)  # First question index = 0.

    def generate_clustering_labels_for_k(self, sample_individual_questions_array, distance_matrix_dict, timestamped_results_path):
        for k in self.k_array:
            run_uuid = uuid.uuid1().int
            cluster_labels = self.k_medoids(sample_individual_questions_array, distance_matrix_dict, k, run_uuid)
            if len(cluster_labels) != self.n:
                raise Exception('Wrong number of cluster labels for clustering ID: ' + str(run_uuid))
            ensembles_dao.write_clustering_labels(cluster_labels, timestamped_results_path, k, self.n, run_uuid)

    def k_medoids(self, sample_individual_questions, similarity_matrix_dict, k, run_uuid):
        # Returns an array of size k, choosing random elements from 0 to sample_size
        max_iterations = 100

        gu.print_screen('Starting clustering ID: ' + str(run_uuid) + '. Initial k medoids k = ' + str(k))
        medoids = self.calculate_initial_medoids(k)

        for i in range(max_iterations):
            # Labels for this iteration
            cluster_labels = set()
            medoids_similarity_sum = [0] * k

            for question in sample_individual_questions:
                question_id = int(question[0])

                selected_medoid_index = 0
                selected_medoid = medoids[0]
                max_similarity_to_medoid = 0.0

                for medoid_index in range(0, k):
                    medoid = medoids[medoid_index]
                    similarity_to_medoid = self.get_similarity_to_medoid(similarity_matrix_dict, question_id, medoid)
                    if similarity_to_medoid > max_similarity_to_medoid:
                        selected_medoid_index = medoid_index
                        selected_medoid = medoid
                        max_similarity_to_medoid = similarity_to_medoid

                medoids_similarity_sum[selected_medoid_index] += max_similarity_to_medoid
                cluster_labels.add((question_id, selected_medoid))

            new_medoids, new_cluster_labels = self.update_medoids(cluster_labels, medoids, k, medoids_similarity_sum, similarity_matrix_dict, run_uuid)

            reach_limit = i == (max_iterations - 1)
            if self.is_converged(medoids, new_medoids) or reach_limit:
                if reach_limit:
                    gu.print_screen('NOT CONVERGED.')
                return new_cluster_labels
            else:
                medoids = new_medoids

    def update_medoids(self, cluster_labels, medoids, k, medoids_similarity_sum, similarity_matrix_dict, run_uuid):
        # Store data points to the current cluster they belong to
        clusters = []  # Ver si necesito esta coleccion, tambien esta en cluster_labels pero acomodado de otra manera.
        new_medoids = []

        # Build clusters in different collections.
        for current_medoid in medoids:
            cluster = []
            for pair_question_cluster in cluster_labels:
                if pair_question_cluster[1] == current_medoid:
                    cluster.append(pair_question_cluster[0])

            clusters.append(cluster)

        for cluster_index in range(0, k):
            new_medoid = medoids[cluster_index]
            old_medoids_similarity_sum = medoids_similarity_sum[cluster_index]

            # Compare each question with each other in the same cluster.
            for question_index_i in range(len(clusters[cluster_index])):
                cur_medoids_similarity_sum = 0
                for question_index_j in range(len(clusters[cluster_index])):
                    similarity_to_medoid = self.get_similarity_to_medoid(similarity_matrix_dict,
                                                                         clusters[cluster_index][question_index_i],
                                                                         clusters[cluster_index][question_index_j])
                    cur_medoids_similarity_sum += similarity_to_medoid

                if cur_medoids_similarity_sum > old_medoids_similarity_sum:
                    new_medoid = clusters[cluster_index][question_index_i]
                    old_medoids_similarity_sum = cur_medoids_similarity_sum

            # Now we have the optimal medoid of the current cluster
            new_medoids.append(new_medoid)

        new_cluster_labels = self.build_new_cluster_labels(new_medoids, clusters, run_uuid)
        return new_medoids, new_cluster_labels

    @staticmethod
    def get_similarity_to_medoid(similarity_matrix_dict, question_id_i, question_id_j):
        if question_id_i == question_id_j:
            return 1.0

        # We might need two look-ups because we don't know the order in the key (i, j) or (j, i) (triangular matrix).
        similarity_to_medoid_record = similarity_matrix_dict.get((question_id_i, question_id_j))
        if not similarity_to_medoid_record:
            similarity_to_medoid_record = similarity_matrix_dict.get((question_id_j, question_id_i))

        if similarity_to_medoid_record:
            return similarity_to_medoid_record['similarity']
        else:
            return 0.0

    @staticmethod
    def is_converged(medoids, new_medoids):
        return np.array_equal(medoids, new_medoids)

    @staticmethod
    def build_new_cluster_labels(new_medoids, clusters, run_uuid):
        new_cluster_labels = set()

        for mediod_index in range(len(new_medoids)):
            for question_index_i in range(len(clusters[mediod_index])):
                new_cluster_labels.add((run_uuid, clusters[mediod_index][question_index_i], new_medoids[mediod_index]))

        return new_cluster_labels
