import gensim


class W2V:

    def __init__(self, sentences=None, size=100, alpha=0.025, window=5, min_count=5, sample=0.001,
                 min_alpha=0.0001, sg=0, negative=5, cbow_mean=1, epoch=5, hs=0):
        self.model = gensim.models.Word2Vec(sentences=sentences, size=size, alpha=alpha, window=window,
                                            min_count=min_count, sample=sample, min_alpha=min_alpha, sg=sg,
                                            negative=negative, cbow_mean=cbow_mean, iter=epoch, hs=hs)

    def new(self, sentences=None, size=100, alpha=0.025, window=5, min_count=5, sample=0.001,
            min_alpha=0.0001, sg=0, negative=5, cbow_mean=1, epoch=5, hs=0):
        self.model = gensim.models.Word2Vec(sentences=sentences, size=size, alpha=alpha, window=window,
                                            min_count=min_count, sample=sample, min_alpha=min_alpha, sg=sg,
                                            negative=negative, cbow_mean=cbow_mean, iter=epoch, hs=hs)

    def train(self, sentences):
        self.model.train(sentences)

    def similarity(self, word1, word2):
        p = 0.001
        try:
            p = self.model.similarity(word1, word2)
        except Exception:
            pass
        return p

    def same_similarity(self, word11, word12, word21):
        word22 = self.model.most_similar([word11, word12], [word21])
        return word22

    def save_model(self, filename):
        self.model.save(filename)

    def load_model(self, filename):
        self.model = gensim.models.Word2Vec.load(filename)

if __name__ == "__main__":
    model = gensim.models.Word2Vec(hs=1)
