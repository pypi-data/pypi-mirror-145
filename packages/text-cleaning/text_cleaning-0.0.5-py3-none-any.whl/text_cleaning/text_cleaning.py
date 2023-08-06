from more_itertools import locate
from sklearn.cluster import AffinityPropagation
from collections import defaultdict

import numpy as np
import Levenshtein as lvt
import copy


class textCleaning:
    def __init__(self, sentences):
        self.res = dict()
        self.word2id = defaultdict(list)
        self.id2word = defaultdict(list)
        self.sentences = sentences
        self.process_clusters = list()
        
    def showClusterInfo(self):
        for key, value in self.res.items():
            print(" - *%s:* *%s:* %s" % (key, value['word_rep'], ", ".join(value['cluster_words'])))
      
    def take_cluster_input(self):
        print('Current Clusters\n')
        self.showClusterInfo()
        self.process_clusters = input('Enter Clusters: ')
        target_clusters = self.process_clusters.split(',')
        return target_clusters

    def flatten(self, sentences):
        return [item for sublist in self.sentences for item in sublist]

    def clean_by_clustering(self):
        word_list = self.flatten(self.sentences)

        words = np.asarray(word_list) #So that indexing with a list will work

        # https://stackoverflow.com/q/54583102
        lev_similarity = -1*np.array([[lvt.distance(w1,w2) for w1 in words] for w2 in words])

        affprop = AffinityPropagation(affinity="precomputed", damping=0.5)
        affprop.fit(lev_similarity)
        for cluster_id in np.unique(affprop.labels_):
            exemplar = words[affprop.cluster_centers_indices_[cluster_id]]
            cluster = np.unique(words[np.nonzero(affprop.labels_==cluster_id)])
            cluster_str = ", ".join(cluster)
            cluster_words = cluster
            self.res[str(cluster_id + 1)] = {'word_rep': exemplar,
                                       'cluster_words': cluster_words}


        for sdx, s in enumerate(self.sentences):
            for word in s:
                self.word2id[word].append(sdx)
                self.id2word[sdx].append(word)

        target_clusters = self.take_cluster_input()
        print('\n')
        print('original sentences')
        print(self.sentences)
        print('\n')
        modifiedSentences = self.sentences
        for target_cluster in target_clusters:
            exemplar = self.res[target_cluster]['word_rep']
            cluster_words = self.res[target_cluster]['cluster_words']
            print('Cluster representation is: ' + exemplar)
            print('Words in cluster are: ' + ', '.join(cluster_words))
            normalise_cluster = input("Enter Normalised word for the Cluster: ")
            print('Normalise_cluster ' + str(target_cluster) +  ' with: ' + normalise_cluster)

            for word in cluster_words:
                sentence_ids = self.word2id[word]

                for ids_ in sentence_ids:
                    words_ids = indexes = list(locate(modifiedSentences[ids_], lambda x: x == word)) 
                    for i in words_ids:
                        modifiedSentences[ids_][i] = normalise_cluster
        return modifiedSentences
