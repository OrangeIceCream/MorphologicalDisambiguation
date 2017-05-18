from common_stuff import find_num_of_max_elem, make_test_sentences_for_part, concat_files
import json
import os
import PM
from count_results import count_all


pm = PM.PM()


tag_tag = None
tag_word = None


def tag_tag_similarity(tag1, tag2):
    if tag2 in tag_tag:
        if tag1 in tag_tag[tag2]["tags"]:
            return tag_tag[tag2]["tags"][tag1]
    return 0.0001


def tag_word_similarity(tag, word):
    if tag in tag_word:
        if word in tag_word[tag]["words"]:
            return tag_word[tag]["words"][word]
    return 0.0001


def find_most_likely_tags(words,
                          possible_tags,
                          tag_tag_similarity,
                          word_tag_similarity):

    forward_probabilities = [[1]] + [[0] * len(word_possible_tag) for word_possible_tag in possible_tags]
    backward_probabilities = [[0] * len(word_possible_tag) for word_possible_tag in possible_tags] + [[1]]
    result_probabilities = [[0] * len(word_possible_tag) for word_possible_tag in possible_tags]

    for k in range(1, len(forward_probabilities)):
        for i in range(len(forward_probabilities[k])):
            prev_prob = 0
            tag1 = possible_tags[k-1][i]
            for j in range(len(forward_probabilities[k-1])):
                if k == 1:
                    tag2 = "BEGIN"
                else:
                    tag2 = possible_tags[k-2][j]
                prev_prob += forward_probabilities[k-1][j] * tag_tag_similarity(tag1, tag2)
            forward_probabilities[k][i] = prev_prob * word_tag_similarity(tag1, words[k-1])
        norm = 0
        for forward_prob in forward_probabilities[k]:
            norm += forward_prob
        for i in range(len(forward_probabilities[k])):
            forward_probabilities[k][i] /= norm

    for k in range(len(backward_probabilities) - 2, -1, -1):
        for i in range(len(backward_probabilities[k])):
            prev_prob = 0
            tag1 = possible_tags[k][i]
            for j in range(len(backward_probabilities[k+1])):
                if k == len(backward_probabilities) - 2:
                    tag2 = "END"
                    word_probability = 1
                else:
                    tag2 = possible_tags[k+1][j]
                    word_probability = word_tag_similarity(tag2, words[k+1])
                prev_prob += backward_probabilities[k+1][j] * \
                             tag_tag_similarity(tag2, tag1) * word_probability
            backward_probabilities[k][i] = prev_prob
        norm = 0
        for backward_prob in backward_probabilities[k]:
            norm += backward_prob
        for i in range(len(backward_probabilities[k])):
            backward_probabilities[k][i] /= norm

    for k in range(len(result_probabilities)):
        norm = 0
        for i in range(len(result_probabilities[k])):
            norm += forward_probabilities[k + 1][i] * backward_probabilities[k][i]
        for i in range(len(result_probabilities[k])):
            result_probabilities[k][i] = forward_probabilities[k + 1][i] * backward_probabilities[k][i] / norm

    result = []
    for i in range(len(possible_tags)):
        result.append(possible_tags[i][find_num_of_max_elem(result_probabilities[i])])
    return result


def find_possible_tag(sentence):
    tags = []
    for word in sentence:
        parse = pm.parse_and_add_correct(word)
        tags.append(parse[1])
    return tags


def parse_test_sentence(sentence_text, sentence_tags):
    possible_tags = find_possible_tag(zip(sentence_text, sentence_tags))
    return find_most_likely_tags(sentence_text, possible_tags,
                                 tag_tag_similarity,
                                 tag_word_similarity)


def test_model_for_part(parts_amount, part_num, source_directory_tags, source_directory_text,
                        source_directory_models, destination_folder):
    global tag_tag
    global tag_word

    test_sentences_text, test_sentences_tags = make_test_sentences_for_part(parts_amount, part_num,
                                                                            source_directory_tags,
                                                                            source_directory_text)

    tag_tag_filename = source_directory_models + str(parts_amount) + "_" + str(part_num) + "_tag_tag_probability.txt"
    tag_word_filename = source_directory_models + str(parts_amount) + "_" + str(part_num) + "_tag_word_probability.txt"

    with open(tag_tag_filename, "r", encoding="utf-8") as infile:
        tag_tag = json.loads(infile.read(), encoding="utf-8")
    with open(tag_word_filename, "r", encoding="utf-8") as infile:
        tag_word = json.loads(infile.read(), encoding="utf-8")

    destination_filename = str(parts_amount) + "_" + str(part_num) + "_result.txt"
    destination_filename = os.path.join(destination_folder, destination_filename)

    result = []
    for i in range(len(test_sentences_text)):
        print(i)
        result.append(parse_test_sentence(test_sentences_text[i], test_sentences_tags[i]))

    with open(destination_filename, "w", encoding="utf-8") as outfile:
        outfile.write(json.dumps(result, indent=4, ensure_ascii=False))


def cross_test_model(parts_amount, source_directory_tags, source_directory_text, source_directory_models,
                     destination_folder, result_file):
    for i in range(parts_amount):
        print(i)
        test_model_for_part(parts_amount, i, source_directory_tags, source_directory_text,
                            source_directory_models, destination_folder)
    concat_files(destination_folder, result_file)


if __name__ == "__main__":
    cross_test_model(10, "../Data/parts/tags", "../Data/parts/text", "../models/markov/",
                     "../result/markov/parts", "../result/markov/markov_result.txt")
    count_all("../result/markov", "../result/markov/markov_result.txt")
