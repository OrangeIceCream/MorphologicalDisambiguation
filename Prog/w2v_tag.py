import json
import os
from markov_tag import find_most_likely_tags
import PM
import W2V
from common_stuff import concat_files, make_test_sentences_for_part
from count_results import count_all


pm = PM.PM()
tag_word = None
w2v = W2V.W2V()


def tag_word_similarity(tag, word):
    if tag in tag_word:
        if word in tag_word[tag]["words"]:
            return tag_word[tag]["words"][word]
    return 0.0001


def find_possible_tag(sentence):
    tags = []
    for word in sentence:
        parse = pm.parse_and_add_correct(word)
        tags.append(parse[1])
    return tags


def parse_test_sentence(sentence_text, sentence_tags):
    global w2v

    possible_tags = find_possible_tag(zip(sentence_text, sentence_tags))
    return find_most_likely_tags(sentence_text, possible_tags,
                                 w2v.similarity,
                                 tag_word_similarity)


def test_model_for_part(parts_amount, part_num, source_directory_tags, source_directory_text,
                        source_directory_models_markov, source_directory_models_w2v, destination_directory):
    global tag_word

    test_sentences_text, test_sentences_tags = make_test_sentences_for_part(parts_amount, part_num,
                                                                            source_directory_tags,
                                                                            source_directory_text)

    tag_word_filename = source_directory_models_markov + str(parts_amount) + \
                        "_" + str(part_num) + "_tag_word_probability.txt"

    with open(tag_word_filename, "r", encoding="utf-8") as infile:
        tag_word = json.loads(infile.read(), encoding="utf-8")

    w2v.load_model(os.path.join(source_directory_models_w2v, str(parts_amount) + "_" + str(part_num)))

    destination_filename = str(parts_amount) + "_" + str(part_num) + "_result.txt"
    destination_filename = os.path.join(destination_directory, destination_filename)

    result = []
    for i in range(len(test_sentences_text)):
        print(i)
        result.append(parse_test_sentence(test_sentences_text[i], test_sentences_tags[i]))

    with open(destination_filename, "w", encoding="utf-8") as outfile:
        outfile.write(json.dumps(result, indent=4, ensure_ascii=False))


def cross_test_model(parts_amount, source_directory_tags, source_directory_text, source_directory_models_markov,
                     source_directory_models_w2v, destination_directory, result_file):
    for i in range(parts_amount):
        print(i)
        test_model_for_part(parts_amount, i, source_directory_tags, source_directory_text,
                            source_directory_models_markov, source_directory_models_w2v, destination_directory)
    concat_files(destination_directory, result_file)


if __name__ == "__main__":
    cross_test_model(10, "../Data/parts/tags", "../Data/parts/text", "../models/markov/", "../models/w2v/",
                     "../result/w2v/parts", "../result/w2v/w2v_result.txt")
    count_all("../result/w2v", "../result/w2v/w2v_result.txt")
