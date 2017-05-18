from crf_train import make_pos_features_for_sentence, make_gna_features_for_sentence, make_case_features_for_sentence
from common_stuff import filter_possible_tag_by_feature, make_test_sentences_for_part, concat_files
from markov_tag import find_most_likely_tags
import os
import json
import copy
import pycrfsuite as crf
import PM
from count_results import count_all


pm = PM.PM()

tag_tag = None
tag_word = None

tagger_pos = crf.Tagger()
tagger_gna = crf.Tagger()
tagger_case = crf.Tagger()


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


def find_possible_tag(sentence):
    tags = []
    for word in sentence:
        parse = pm.parse_and_add_correct(word)
        tags.append(parse[1])
    return tags


def parse_test_sentence(sentence_text, sentence_tags):
    global tagger_pos
    global tagger_gna
    global tagger_case

    possible_tag = find_possible_tag(zip(sentence_text, sentence_tags))
    possible_tag_copy = copy.deepcopy(possible_tag)

    sent_features = make_pos_features_for_sentence(sentence_tags, sentence_text)
    result_pos = tagger_pos.tag(crf.ItemSequence(sent_features))

    filter_possible_tag_by_feature(possible_tag, "pos", result_pos)
    for i in range(len(possible_tag)):
        if len(possible_tag[i]) == 0:
            possible_tag[i] = copy.deepcopy(possible_tag_copy[i])
    possible_tag_copy = copy.deepcopy(possible_tag)

    sent_features = make_gna_features_for_sentence(sentence_tags, sentence_text, result_pos)
    result_gna = tagger_gna.tag(crf.ItemSequence(sent_features))

    filter_possible_tag_by_feature(possible_tag, "gen/num/anim", result_gna)
    for i in range(len(possible_tag)):
        if len(possible_tag[i]) == 0:
            possible_tag[i] = copy.deepcopy(possible_tag_copy[i])
    possible_tag_copy = copy.deepcopy(possible_tag)

    sent_features = make_case_features_for_sentence(sentence_tags, sentence_text, result_pos, result_gna)
    result_case = tagger_case.tag(crf.ItemSequence(sent_features))

    filter_possible_tag_by_feature(possible_tag, "case", result_case)
    for i in range(len(possible_tag)):
        if len(possible_tag[i]) == 0:
            possible_tag[i] = copy.deepcopy(possible_tag_copy[i])

    return find_most_likely_tags(sentence_text, possible_tag, tag_tag_similarity, tag_word_similarity)


def test_model_for_part(parts_amount, part_num, source_directory_tags, source_directory_text,
                        source_directory_models_markov, source_directory_models_crf, destination_directory):
    global tag_tag
    global tag_word

    test_sentences_text, test_sentences_tags = make_test_sentences_for_part(parts_amount, part_num,
                                                                            source_directory_tags,
                                                                            source_directory_text)

    tag_tag_filename = source_directory_models_markov + str(parts_amount) + \
                       "_" + str(part_num) + "_tag_tag_probability.txt"
    tag_word_filename = source_directory_models_markov + str(parts_amount) + \
                        "_" + str(part_num) + "_tag_word_probability.txt"

    with open(tag_tag_filename, "r", encoding="utf-8") as infile:
        tag_tag = json.loads(infile.read(), encoding="utf-8")
    with open(tag_word_filename, "r", encoding="utf-8") as infile:
        tag_word = json.loads(infile.read(), encoding="utf-8")

    global tagger_pos
    global tagger_gna
    global tagger_case
    crf_models_prefix = os.path.join(source_directory_models_crf, str(parts_amount) + "_" + str(part_num) + "_")
    tagger_pos.open(crf_models_prefix+"pos")
    tagger_gna.open(crf_models_prefix + "gna")
    tagger_case.open(crf_models_prefix + "case")

    destination_filename = str(parts_amount) + "_" + str(part_num) + "_result.txt"
    destination_filename = os.path.join(destination_directory, destination_filename)

    result = []
    for i in range(len(test_sentences_text)):
        print(i)
        result.append(parse_test_sentence(test_sentences_text[i], test_sentences_tags[i]))

    os.makedirs(os.path.dirname(destination_filename), exist_ok=True)
    with open(destination_filename, "w", encoding="utf-8") as outfile:
        outfile.write(json.dumps(result, indent=4, ensure_ascii=False))


def cross_test_model(parts_amount, source_directory_tags, source_directory_text, source_directory_models_markov,
                     source_directory_models_crf, destination_directory, result_file):
    for i in range(parts_amount):
        print(i)
        test_model_for_part(parts_amount, i, source_directory_tags, source_directory_text,
                            source_directory_models_markov, source_directory_models_crf, destination_directory)
    concat_files(destination_directory, result_file)


if __name__ == "__main__":
    cross_test_model(10, "../Data/parts/tags", "../Data/parts/text", "../models/markov/", "../models/crf/",
                     "../result/crf/parts", "../result/crf/crf_result.txt")
    count_all("../result/crf", "../result/crf/crf_result.txt")
