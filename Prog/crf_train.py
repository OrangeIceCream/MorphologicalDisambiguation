import PM
import os
import copy
import pycrfsuite as crf
from common_stuff import make_lists_from_elems, filter_possible_tag_by_feature
from common_stuff import make_train_sentences_for_part, make_possible_features_from_possible_tags


pm = PM.PM()
trainer_pos = crf.Trainer()
trainer_gna = crf.Trainer()
trainer_case = crf.Trainer()


def find_possible_tag(sentence):
    tags = []
    for word in sentence:
        parse = pm.parse_and_add_correct(word)
        tags.append(parse[1])
    return tags


def make_pos_features_for_sentence(sentence_tags, sentence_text):

    possible_tags = find_possible_tag(zip(sentence_text, sentence_tags))
    possible_poses = make_possible_features_from_possible_tags(possible_tags, "pos")

    features_list = []
    for i in range(len(sentence_text)):
        features = dict()
        if i == 0:
            features["BEGIN"] = True
        if i == len(sentence_text) - 1:
            features["END"] = True
        if i != 0:
            features["prev_word"] = sentence_text[i - 1]
        if i != len(sentence_text) - 1:
            features["next_word"] = sentence_text[i + 1]
        features["word"] = sentence_text[i]
        features["possible"] = copy.deepcopy(possible_poses[i])
        features_list.append(features)
    return features_list


def set_trainer_pos(train_sentences_tags, train_sentences_text):
    global trainer_pos

    trainer_pos.clear()

    print("start set trainer")

    for i in range(len(train_sentences_text)):
        print("set " + str(i) + " sentence for trainer")
        sent_correct_pos_seq = make_possible_features_from_possible_tags(train_sentences_tags[i], "pos")
        sent_correct_pos_seq = make_lists_from_elems(sent_correct_pos_seq)
        sent_features = crf.ItemSequence(make_pos_features_for_sentence(train_sentences_tags[i],
                                                                        train_sentences_text[i]))
        for seq in sent_correct_pos_seq:
            trainer_pos.append(sent_features, seq)

    print("finish set trainer")


def train_model_pos(train_sentences_tags, train_sentences_text, destination):
    global trainer_pos

    set_trainer_pos(train_sentences_tags, train_sentences_text)
    trainer_pos.select("l2sgd")

    print("start train crf")
    trainer_pos.train(destination)
    print("finish train crf")


def make_gna_features_for_sentence(sentence_tags, sentence_text, poses):

    possible_tags = find_possible_tag(zip(sentence_text, sentence_tags))
    filter_possible_tag_by_feature(possible_tags, "pos", poses)
    possible_gna = make_possible_features_from_possible_tags(possible_tags, "gen/num/anim")

    features_list = []
    for i in range(len(sentence_text)):
        features = dict()
        if i == 0:
            features["BEGIN"] = True
        if i == len(sentence_text) - 1:
            features["END"] = True
        if i != 0:
            features["prev_pos"] = poses[i - 1]
        if i != len(sentence_text) - 1:
            features["next_pos"] = poses[i + 1]
        features["word"] = sentence_text[i]
        features["pos"] = poses[i]
        features["possible"] = copy.deepcopy(possible_gna[i])
        features_list.append(features)
    return features_list


def set_trainer_gna(train_sentences_tags, train_sentences_text):
    global trainer_gna

    trainer_gna.clear()

    print("start set trainer")

    for i in range(len(train_sentences_text)):
        print("set " + str(i) + " sentence for trainer")
        sent_correct_pgna_seq = make_possible_features_from_possible_tags(train_sentences_tags[i], "pos/gen/num/anim")
        sent_correct_pgna_seq = make_lists_from_elems(sent_correct_pgna_seq)
        for seq in sent_correct_pgna_seq:
            sent_features = crf.ItemSequence(make_gna_features_for_sentence(train_sentences_tags[i],
                                                                            train_sentences_text[i],
                                                                            [x[:4] for x in seq]))
            trainer_gna.append(sent_features, [x[4:] for x in seq])

    print("finish set trainer")


def train_model_gna(train_sentences_tags, train_sentences_text, destination):
    global trainer_gna

    set_trainer_gna(train_sentences_tags, train_sentences_text)
    trainer_gna.select("l2sgd")

    print("start train crf")
    trainer_gna.train(destination)
    print("finish train crf")


def make_case_features_for_sentence(sentence_tags, sentence_text, poses, gnas):

    possible_tags = find_possible_tag(zip(sentence_text, sentence_tags))
    filter_possible_tag_by_feature(possible_tags, "pos", poses)
    filter_possible_tag_by_feature(possible_tags, "gen/num/anim", gnas)
    possible_case = make_possible_features_from_possible_tags(possible_tags, "case")

    features_list = []
    for i in range(len(sentence_text)):
        features = dict()
        if i == 0:
            features["BEGIN"] = True
        if i == len(sentence_text) - 1:
            features["END"] = True
        if i != 0:
            features["prev_pos"] = poses[i - 1]
            features["prev_gna"] = gnas[i - 1]
        if i != len(sentence_text) - 1:
            features["next_pos"] = poses[i + 1]
            features["next_gna"] = gnas[i-1]
        features["word"] = sentence_text[i]
        features["pos"] = poses[i]
        features["gna"] = gnas[i]
        features["possible"] = copy.deepcopy(possible_case[i])
        features_list.append(features)
    return features_list


def set_trainer_case(train_sentences_tags, train_sentences_text):
    global trainer_case

    trainer_case.clear()

    print("start set trainer")

    for i in range(len(train_sentences_text)):
        print("set " + str(i) + " sentence for trainer")
        sent_correct_pgnac_seq = make_possible_features_from_possible_tags(train_sentences_tags[i],
                                                                          "pos/gen/num/anim/case")
        sent_correct_pgnac_seq = make_lists_from_elems(sent_correct_pgnac_seq)
        for seq in sent_correct_pgnac_seq:
            sent_features = crf.ItemSequence(make_case_features_for_sentence(train_sentences_tags[i],
                                                                             train_sentences_text[i],
                                                                             [x[:4] for x in seq],
                                                                             [x[4:7] for x in seq]))
            trainer_case.append(sent_features, [x[7:] for x in seq])

    print("finish set trainer")


def train_model_case(train_sentences_tags, train_sentences_text, destination):
    global trainer_case

    set_trainer_case(train_sentences_tags, train_sentences_text)
    trainer_case.select("l2sgd")

    print("start train crf")
    trainer_case.train(destination)
    print("finish train crf")


def train_models_for_part(parts_amount, part_num, source_directory_tags, source_directory_text,
                          destination_directory):

    train_sentences_text, train_sentences_tags = \
        make_train_sentences_for_part(parts_amount, part_num, source_directory_tags, source_directory_text)

    pos_model_filename = str(parts_amount) + "_" + str(part_num) + "_pos"
    gna_model_filename = str(parts_amount) + "_" + str(part_num) + "_gna"
    case_model_filename = str(parts_amount) + "_" + str(part_num) + "_case"
    pos_model_filename = os.path.join(destination_directory, pos_model_filename)
    gna_model_filename = os.path.join(destination_directory, gna_model_filename)
    case_model_filename = os.path.join(destination_directory, case_model_filename)

    train_model_pos(train_sentences_tags, train_sentences_text, pos_model_filename)
    train_model_gna(train_sentences_tags, train_sentences_text, gna_model_filename)
    train_model_case(train_sentences_tags, train_sentences_text, case_model_filename)


def train_models_all(parts_amount, source_directory_tags, source_directory_text,
                     destination_directory):
    for i in range(parts_amount):
        train_models_for_part(parts_amount, i, source_directory_tags, source_directory_text, destination_directory)


if __name__ == "__main__":
    train_models_for_part(10, 0, "../Data/parts/tags", "../Data/parts/text", "../models/crf/")
