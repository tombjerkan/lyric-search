import gensim


def similarity_to_song(song_id, index_filename, num_best=10):
    index = gensim.similarities.Similarity.load(index_filename)

    # Add 1 as most similar list will include song itself which will then be
    # removed to give desired number of best
    index.num_best = num_best + 1

    # Subtract 1 from song_id as database starts mapping at 1, but gensim at 0
    similarities = index.similarity_by_id(song_id - 1)

    # Remove song itself (which will be most similar)
    del similarities[0]

    # Add 1 to all gensim song indexes to give their database ids
    similarities = [(index + 1, similarity)
                    for (index, similarity) in similarities]

    return similarities
