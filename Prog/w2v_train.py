import W2V
import os
from common_stuff import make_train_sentences_for_part, make_lists_from_elems

w2v = W2V.W2V()


def train_model_for_part(parts_amount, part_num, source_directory_tags, source_directory_text,
                         destination_directory):

    destination_filename = str(parts_amount) + "_" + str(part_num)
    destination_filename = os.path.join(destination_directory, destination_filename)

    train_sentences_text, train_sentences_tags = \
        make_train_sentences_for_part(parts_amount, part_num, source_directory_tags, source_directory_text)

    train_sentences_tags_for_w2v = []
    for sent_tags in train_sentences_tags:
        train_sentences_tags_for_w2v += make_lists_from_elems(sent_tags)

    print("start train w2v")
    w2v.new(train_sentences_tags_for_w2v, negative=0, size=100, window=10, min_count=0, sg=1, hs=1)
    print("finish train w2v")
    w2v.save_model(destination_filename)


def train_model_all(parts_amount, source_directory_tags, source_directory_text,
                    destination_directory):
    for i in range(parts_amount):
        train_model_for_part(parts_amount, i, source_directory_tags, source_directory_text,
                             destination_directory)


if __name__ == "__main__":
    train_model_all(10, "../Data/parts/tags", "../Data/parts/text", "../models/w2v/")
