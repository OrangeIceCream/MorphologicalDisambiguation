import json
from common_stuff import make_train_sentences_for_part
import os


def train_tag_tag_probability(destination, train_sentences_tags):
    print("start train tags probabilities")
    tags_probabilities = dict()

    for sent in train_sentences_tags:
        tag_seq = [["BEGIN"]] + sent + [["END"]]
        for i in range(0, len(tag_seq)-1):
            cur_tags = tag_seq[i]
            next_tags = tag_seq[i+1]
            for tag1 in next_tags:
                for tag2 in cur_tags:
                    if tag2 in tags_probabilities:
                        tags_probabilities[tag2]["count"] += 1
                    else:
                        tags_probabilities[tag2] = {"count": 1, "tags": dict()}
                    if tag1 in tags_probabilities[tag2]["tags"]:
                        tags_probabilities[tag2]["tags"][tag1] += 1
                    else:
                        tags_probabilities[tag2]["tags"][tag1] = 1

    for tag1 in tags_probabilities:
        for tag2 in tags_probabilities[tag1]["tags"]:
            tags_probabilities[tag1]["tags"][tag2] /= tags_probabilities[tag1]["count"]

    with open(destination, "w", encoding="utf-8") as outfile:
        outfile.write(json.dumps(tags_probabilities, indent=4, ensure_ascii=False))

    print("finish train tags probabilities")


def train_tag_tag_probability_all(parts_amount, source_directory_tags, source_directory_text, destination_folder):
    for i in range(parts_amount):
        train_sentences_text, train_sentences_tags = \
            make_train_sentences_for_part(parts_amount, i, source_directory_tags, source_directory_text)
        destination_filename = "10_" + str(i) + "_tag_tag_probability.txt"
        destination_filename = os.path.join(destination_folder, destination_filename)
        train_tag_tag_probability(destination_filename, train_sentences_tags)


def train_tag_word_probability(destination, train_sentences_tags, train_sentences_text):
    print("start train tag word probabilities")
    words_probabilities = dict()
    for i in range(len(train_sentences_text)):
        for j in range(len(train_sentences_text[i])):
            word = train_sentences_text[i][j]
            tags = train_sentences_tags[i][j]
            for tag in tags:
                if tag in words_probabilities:
                    words_probabilities[tag]["count"] += 1
                else:
                    words_probabilities[tag] = {"count": 1, "words": dict()}
                if word in words_probabilities[tag]["words"]:
                    words_probabilities[tag]["words"][word] += 1
                else:
                    words_probabilities[tag]["words"][word] = 1

    for tag in words_probabilities:
        for word in words_probabilities[tag]["words"]:
            words_probabilities[tag]["words"][word] /= words_probabilities[tag]["count"]

    with open(destination, "w", encoding="utf-8") as outfile:
        outfile.write(json.dumps(words_probabilities, indent=4, ensure_ascii=False))

    print("finish train tags probabilities")


def train_tag_word_probability_all(parts_amount, source_directory_tags, source_directory_text, destination_folder):
    for i in range(parts_amount):
        train_sentences_text, train_sentences_tags = \
            make_train_sentences_for_part(parts_amount, i, source_directory_tags, source_directory_text)
        destination_filename = "10_" + str(i) + "_tag_word_probability.txt"
        destination_filename = os.path.join(destination_folder, destination_filename)
        train_tag_word_probability(destination_filename, train_sentences_tags, train_sentences_text)


if __name__ == "__main__":
    train_tag_tag_probability_all(10, "../Data/parts/tags", "../Data/parts/text", "../models/markov/")
    train_tag_word_probability_all(10, "../Data/parts/tags", "../Data/parts/text", "../models/markov/")
