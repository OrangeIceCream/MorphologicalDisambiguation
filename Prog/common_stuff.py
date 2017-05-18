import json
import os


def make_train_sentences_for_part(parts_amount, part_num, source_directory_tags, source_directory_text):
    print("set train sentences\n")
    train_sentences_tags = []
    train_sentences_text = []
    file_names = [i for i in range(parts_amount)]
    file_names.remove(part_num)
    file_names = [str(parts_amount) + "_" + str(i) + ".txt" for i in file_names]
    file_names_tags = [os.path.join(source_directory_tags, name) for name in file_names]
    file_names_text = [os.path.join(source_directory_text, name) for name in file_names]

    for file_name in file_names_tags:
        with open(file_name, "r", encoding="utf-8") as infile:
            sentences = json.loads(infile.read(), encoding="utf-8")
        train_sentences_tags += sentences

    for file_name in file_names_text:
        with open(file_name, "r", encoding="utf-8") as infile:
            sentences = json.loads(infile.read(), encoding="utf-8")
        train_sentences_text += sentences

    return train_sentences_text, train_sentences_tags


def make_test_sentences_for_part(parts_amount, part_num, source_directory_tags, source_directory_text):
    print("set test sentences\n")
    file_name = str(parts_amount) + "_" + str(part_num) + ".txt"
    file_name_tags = os.path.join(source_directory_tags, file_name)
    file_name_text = os.path.join(source_directory_text, file_name)

    with open(file_name_tags, "r", encoding="utf-8") as infile:
        test_sentences_tags = json.loads(infile.read(), encoding="utf-8")

    with open(file_name_text, "r", encoding="utf-8") as infile:
        test_sentences_text = json.loads(infile.read(), encoding="utf-8")

    return test_sentences_text, test_sentences_tags


def make_lists_from_elems(elems):
    if len(elems) == 1:
        result = []
        for elem in elems[0]:
            result.append([elem])
        return result
    elif len(elems) == 0:
        return []
    else:
        result = []
        tails = make_lists_from_elems(elems[1:])
        for elem in elems[0]:
            for tail in tails:
                result.append([elem]+tail)
        return result


def extract_feature_from_short_tag(tag, feature_name):
    if feature_name == "gen/num/anim":
        return tag[4:5] + tag[7:8] + tag[8:9]
    elif feature_name == "pos/gen/num/anim/case":
        return tag[:4] + tag[4:5] + tag[7:8] + tag[8:9] + tag[5:7]
    elif feature_name == "pos/gen/num/anim":
        return tag[:4] + tag[4:5] + tag[7:8] + tag[8:9]
    elif feature_name == "pos/case":
        return tag[:4] + tag[5:7]
    elif feature_name == "pos":
        return tag[:4]
    elif feature_name == "gender":
        return tag[4:5]
    elif feature_name == "case":
        return tag[5:7]
    elif feature_name == "number":
        return tag[7:8]
    elif feature_name == "anim":
        return tag[8:9]
    elif feature_name == "comp":
        return tag[9:10]
    elif feature_name == "aspect":
        return tag[10:11]
    elif feature_name == "tran":
        return tag[11:12]
    elif feature_name == "tense":
        return tag[12:13]
    elif feature_name == "person":
        return tag[13:14]
    elif feature_name == "mood":
        return tag[14:15]
    elif feature_name == "other":
        return tag[15:16]
    else:
        return "-"


def find_num_of_max_elem(l):
    result = 0
    for i in range(1, len(l)):
        if l[i] > l[result]:
            result = i
    return result


def concat_files(source_folder, destination):
    sentences = []
    for filename in os.listdir(source_folder):
        if filename.endswith(".txt"):
            print(source_folder, filename)
            with open(os.path.join(source_folder, filename), "r", encoding="utf-8") as infile:
                sentences += json.loads(infile.read(), encoding="utf-8")

    with open(destination, "w", encoding="utf-8") as outfile:
        outfile.write(json.dumps(sentences, indent=4, ensure_ascii=False))


def filter_possible_tag_by_feature(possible_tag, feature_name, features):
    if feature_name is None:
        return
    for i in range(len(possible_tag)):
        possible_tag[i] = \
            [x for x in possible_tag[i] if extract_feature_from_short_tag(x, feature_name) == features[i]]


def make_possible_features_from_possible_tags(possible_tags, feature_name):
    result = []
    for word_possible_tags in possible_tags:
        result.append(list({extract_feature_from_short_tag(x, feature_name) for x in word_possible_tags}))
    return result
