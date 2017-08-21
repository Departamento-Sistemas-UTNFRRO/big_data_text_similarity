from __future__ import division
import nltk, math, sys
from nltk.corpus import brown, wordnet_ic
from nltk.corpus import wordnet as wn
import numpy as np

ALPHA = 0.2
BETA = 0.45 
ETA = 0.4
PHI = 0.2 
DELTA = 0.85 
N = 0

brown_freqs = dict()
semcor_ic = wordnet_ic.ic('ic-semcor.dat')

class SemanticComparator(object):
    
    def get_best_synset_pair(self, word_1, word_2):
        max_sim = -1.0
        synsets_1 = wn.synsets(word_1)
        synsets_2 = wn.synsets(word_2)
        if len(synsets_1) == 0 or len(synsets_2) == 0:
            return None, None
        else:
            max_sim = -1.0
            best_pair = None, None
            for synset_1 in synsets_1:
                for synset_2 in synsets_2:
                    try:
                        sim = synset_1.lin_similarity(synset_2, semcor_ic)
                    except nltk.corpus.reader.wordnet.WordNetError:
                        sim = 0
                    except: 
                        sim = 0
                    if sim > max_sim:
                        max_sim = sim
                        best_pair = synset_1, synset_2
            return best_pair

    def length_dist(self, synset_1, synset_2):
        l_dist = sys.maxsize
        if synset_1 is None or synset_2 is None: 
            return 0.0
        if synset_1 == synset_2:
            l_dist = 0.0
        else:
            wset_1 = set([str(x.name()) for x in synset_1.lemmas()])        
            wset_2 = set([str(x.name()) for x in synset_2.lemmas()])
            if len(wset_1.intersection(wset_2)) > 0:
                l_dist = 1.0
            else:
                l_dist = synset_1.shortest_path_distance(synset_2)
                if l_dist is None:
                    l_dist = 0.0
        return math.exp(-ALPHA * l_dist)

    def hierarchy_dist(self, synset_1, synset_2):
        h_dist = sys.maxsize
        if synset_1 is None or synset_2 is None: 
            return h_dist
        if synset_1 == synset_2:
            h_dist = max([x[1] for x in synset_1.hypernym_distances()])
        else:
            hypernyms_1 = {x[0]:x[1] for x in synset_1.hypernym_distances()}
            hypernyms_2 = {x[0]:x[1] for x in synset_2.hypernym_distances()}
            lcs_candidates = set(hypernyms_1.keys()).intersection(set(hypernyms_2.keys()))
            if len(lcs_candidates) > 0:
                lcs_dists = []
                for lcs_candidate in lcs_candidates:
                    lcs_d1 = 0
                    if lcs_candidate in hypernyms_1:
                        lcs_d1 = hypernyms_1[lcs_candidate]
                    lcs_d2 = 0
                    if lcs_candidate in hypernyms_2:
                        lcs_d2 = hypernyms_2[lcs_candidate]
                    lcs_dists.append(max([lcs_d1, lcs_d2]))
                h_dist = max(lcs_dists)
            else:
                h_dist = 0.0
        return ((math.exp(BETA * h_dist) - math.exp(-BETA * h_dist)) / (math.exp(BETA * h_dist) + math.exp(-BETA * h_dist)))

    def word_similarity(self, word_1, word_2):
        synset_pair = self.get_best_synset_pair(word_1, word_2)
        return (self.length_dist(synset_pair[0], synset_pair[1]) * self.hierarchy_dist(synset_pair[0], synset_pair[1]))

    def most_similar_word(self, word, word_set):
        max_sim = -1.0
        sim_word = ""
        for ref_word in word_set:
            sim = self.word_similarity(word, ref_word)
            if sim > max_sim:
                max_sim = sim
                sim_word = ref_word
        return sim_word, max_sim

    def info_content(self, lookup_word):
        global N
        if N == 0:
            for sent in brown.sents():
                for word in sent:
                    word = word.lower()
                    if word not in brown_freqs:
                        brown_freqs[word] = 0
                    brown_freqs[word] = brown_freqs[word] + 1
                    N = N + 1
        lookup_word = lookup_word.lower()
        n = 0 if lookup_word not in brown_freqs else brown_freqs[lookup_word]
        return 1.0 - (math.log(n + 1) / math.log(N + 1))

    def semantic_vector(self, words, joint_words, info_content_norm):
        sent_set = set(words)
        semvec = np.zeros(len(joint_words))
        i = 0
        for joint_word in joint_words:
            if joint_word in sent_set:
                semvec[i] = 1.0
                if info_content_norm:
                    semvec[i] = semvec[i] * math.pow(self.info_content(joint_word), 2)
            else:
                sim_word, max_sim = self.most_similar_word(joint_word, sent_set)
                semvec[i] = max_sim if max_sim > PHI else 0.0
                if info_content_norm:
                    semvec[i] = semvec[i] * self.info_content(joint_word) * self.info_content(sim_word)
            i = i + 1
        return semvec

    def semantic_similarity(self, sentence_1, sentence_2, info_content_norm):
        words_1 = nltk.word_tokenize(sentence_1)
        words_2 = nltk.word_tokenize(sentence_2)
        joint_words = set(words_1).union(set(words_2))
        vec_1 = self.semantic_vector(words_1, joint_words, info_content_norm)
        vec_2 = self.semantic_vector(words_2, joint_words, info_content_norm)
        value = (np.linalg.norm(vec_1) * np.linalg.norm(vec_2))
        if not value==0:
            return np.dot(vec_1, vec_2.T) / value
        else:
            return 0.0

    def word_order_vector(self, words, joint_words, windex):
        wovec = np.zeros(len(joint_words))
        i = 0
        wordset = set(words)
        for joint_word in joint_words:
            if joint_word in wordset:
                wovec[i] = windex[joint_word]
            else:
                sim_word, max_sim = self.most_similar_word(joint_word, wordset)
                if max_sim > ETA:
                    wovec[i] = windex[sim_word]
                else:
                    wovec[i] = 0
            i = i + 1
        return wovec

    def word_order_similarity(self, sentence_1, sentence_2):
        words_1 = nltk.word_tokenize(sentence_1)
        words_2 = nltk.word_tokenize(sentence_2)
        joint_words = list(set(words_1).union(set(words_2)))
        windex = {x[1]: x[0] for x in enumerate(joint_words)}
        r1 = self.word_order_vector(words_1, joint_words, windex)
        r2 = self.word_order_vector(words_2, joint_words, windex)
        value = np.linalg.norm(r1 + r2)
        if not value==0:
            return 1.0 - (np.linalg.norm(r1 - r2) / value)
        else:
            return 1.0 - (np.linalg.norm(r1 - r2))

    def similarity(self, sentence_1, sentence_2, info_content_norm):
        return DELTA * self.semantic_similarity(sentence_1, sentence_2, info_content_norm) + (1.0 - DELTA) * self.word_order_similarity(sentence_1, sentence_2)

    def must_train(self):
        return False
    
    def compare(self, question1, question2):
        return float(1 - self.similarity(question1, question2, True))
