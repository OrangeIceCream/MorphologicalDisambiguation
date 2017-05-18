import json
from common_stuff import extract_feature_from_short_tag
import os

pos_num = {
    "NOUN": 0,
    "ADJF": 1,
    "ADJS": 2,
    "COMP": 3,
    "NUMR": 4,
    "INFN": 5,
    "PRTS": 6,
    "GRND": 7,
    "PRTF": 8,
    "VERB": 9,
    "ADVB": 10,
    "PRED": 11,
    "CONJ": 12,
    "NPRO": 13,
    "XXXX": 14,
    "PREP": 15,
    "PRCL": 16,
    "INTJ": 17,
    "INIT": 18,
    "LATN": 19,
    "PNCT": 20
}

gender_num ={
    "m": 0,
    "f": 1,
    "b": 2,
    "n": 3,
    "-": 4
}

case_num = {
    "n-": 0,
    "g-": 1,
    "d-": 2,
    "a-": 3,
    "i-": 4,
    "l-": 5,
    "-g": 6,
    "-a": 7,
    "-l": 8,
    "v-": 9,
    "--": 10
}

number_num = {
    "s": 0,
    "p": 1,
    "-": 2
}

anim_num = {
    "a": 0,
    "i": 1,
    "-": 2
}

comp_num = {
    "s": 0,
    "-": 1
}

aspect_num = {
    "p": 0,
    "i": 1,
    "-": 2
}

tran_num = {
    "t": 0,
    "i": 1,
    "-": 2
}

tense_num = {
    "p": 0,
    "n": 1,
    "f": 2,
    "-": 3
}

person_num = {
    "1": 0,
    "2": 1,
    "3": 2,
    "-": 3
}

mood_num = {
    "n": 0,
    "m": 1,
    "-": 2
}

other_num = {
    "n": 0,
    "p": 1,
    "r": 2,
    "-": 3
}

features = [
    "pos",
    "gender",
    "case",
    "number",
    "anim",
    "comp",
    "aspect",
    "transitive",
    "tense",
    "person",
    "mood",
    "other"
]

features_beautiful = {
    "pos": "часть речи",
    "gender": "род",
    "case": "падеж",
    "number": "число",
    "anim": "одушевленность",
    "comp": "степень сравнения",
    "aspect": "вид",
    "transitive": "переходность",
    "tense": "время",
    "person": "лицо",
    "mood": "наклонение",
    "other": "другое"
}

pos_beautiful = {
    "NOUN": "сущ.",
    "ADJF": "полн. прил.",
    "ADJS": "крат. прил.",
    "COMP": "компаратор",
    "NUMR": "числительное",
    "INFN": "инфинитив",
    "PRTS": "крат. прич.",
    "GRND": "дееприч.",
    "PRTF": "полн. прич",
    "VERB": "глагол",
    "ADVB": "наречие",
    "PRED": "предикатив",
    "CONJ": "союз",
    "NPRO": "местоимен. сущ.",
    "XXXX": "неизв.",
    "PREP": "предлог",
    "PRCL": "частица",
    "INTJ": "междометие",
    "INIT": "инициал",
    "LATN": "латиница",
    "PNCT": "знак преп."
}

gender_beautiful ={
    "m": "мужской",
    "f": "женский",
    "b": "общий",
    "n": "средний",
    "-": "-"
}

case_beautiful = {
    "n-": "им.",
    "g-": "род.",
    "d-": "дат.",
    "a-": "вин.",
    "i-": "твор.",
    "l-": "пред.",
    "-g": "род. 2",
    "-a": "вин. 2",
    "-l": "пред. 2",
    "v-": "зват.",
    "--": "-"
}

number_beautiful = {
    "s": "ед.",
    "p": "мн.",
    "-": "-"
}

anim_beautiful = {
    "a": "одуш.",
    "i": "неод.",
    "-": "-"
}

comp_beautiful = {
    "s": "превосход.",
    "-": "-"
}

aspect_beautiful = {
    "p": "соверш.",
    "i": "несов.",
    "-": "-"
}

tran_beautiful = {
    "t": "перех.",
    "i": "непер.",
    "-": "-"
}

tense_beautiful = {
    "p": "прош.",
    "n": "наст.",
    "f": "буд.",
    "-": "-"
}

person_beautiful = {
    "1": "1",
    "2": "2",
    "3": "3",
    "-": "-"
}

mood_beautiful = {
    "n": "изъяв.",
    "m": "повел.",
    "-": "-"
}

other_beautiful = {
    "n": "порядковое",
    "p": "местоимен.",
    "r": "вводное",
    "-": "-"
}

all_beautiful = {
    "pos": pos_beautiful,
    "gender": gender_beautiful,
    "case": case_beautiful,
    "number": number_beautiful,
    "anim": anim_beautiful,
    "comp": comp_beautiful,
    "aspect": aspect_beautiful,
    "transitive": tran_beautiful,
    "tense": tense_beautiful,
    "person": person_beautiful,
    "mood": mood_beautiful,
    "other": other_beautiful
}


def set_data(correct_filename, parsed_filename, text_filename):

    with open(correct_filename, "r", encoding="utf-8") as infile:
        correct_tags = json.loads(infile.read(), encoding="utf-8")
    with open(parsed_filename, "r", encoding="utf-8") as infile:
        parsed_tags = json.loads(infile.read(), encoding="utf-8")
    with open(text_filename, "r", encoding="utf-8") as infile:
        text = json.loads(infile.read(), encoding="utf-8")

    return correct_tags, parsed_tags, text


def write_tag_comparison_to_file(correct_tag, parsed_tag):
    result = " "*20 + ("%20s" % "правильный") + ("%20s" % "неправильный") + "\n"
    for feature in features:
        feature_correct_short_tag = extract_feature_from_short_tag(correct_tag, feature)
        feature_parsed_short_tag = extract_feature_from_short_tag(parsed_tag, feature)
        result += ("%20s" % features_beautiful[feature])
        result += ("%20s" % all_beautiful[feature][feature_correct_short_tag])
        result += ("%20s" % all_beautiful[feature][feature_parsed_short_tag])
        result += "\n"
    result += "\n"
    return result


def count_pos(destination, correct_tags, parsed_tags, text):

    statistics = [None] * len(pos_num)
    for i in range(len(statistics)):
        statistics[i] = [0] * len(pos_num)
    correct_count = 0
    word_count = 0

    outfile = open(destination, "w", encoding="utf-8")

    for i in range(len(correct_tags)):
        for j in range(len(correct_tags[i])):
            print(str(i) + " " + str(j))
            word_count += 1
            correct_word_tags = {extract_feature_from_short_tag(x, "pos") for x in correct_tags[i][j]}
            parsed_word_tag = extract_feature_from_short_tag(parsed_tags[i][j], "pos")
            parsed_word_tag_num = pos_num[parsed_word_tag]
            is_correct = parsed_word_tag in correct_word_tags
            if is_correct:
                statistics[parsed_word_tag_num][parsed_word_tag_num] += 1
                correct_count += 1
            else:
                outfile.write("\n"+("-"*100)+"\n\n")
                outfile.write("sentence: " + str(text[i]) + "\n")
                outfile.write("word: " + text[i][j] + "\n")
                for tag in correct_tags[i][j]:
                    outfile.write(write_tag_comparison_to_file(tag, parsed_tags[i][j]))
                outfile.write("\n" + ("-" * 100) + "\n")
                for correct_word_tag in correct_word_tags:
                    statistics[pos_num[correct_word_tag]][parsed_word_tag_num] += 1

    for short_tag in pos_num:
        outfile.write(("%2s" % str(pos_num[short_tag])) + ": " + pos_beautiful[short_tag]+ "\n")
    outfile.write("\n")
    for row in statistics:
        for column in row:
            outfile.write("%7d" % column)
        outfile.write("\n")
    outfile.write("\n\nword count = " + str(word_count))
    outfile.write("\ncorrect pos count = " + str(correct_count))
    outfile.write("\npercent of correct = " + str(correct_count * 100 / word_count))
    outfile.close()


def count_gender(destination, correct_tags, parsed_tags, text):

    statistics = [None] * len(gender_num)
    for i in range(len(statistics)):
        statistics[i] = [0] * len(gender_num)
    correct_count = 0
    word_count = 0

    outfile = open(destination, "w", encoding="utf-8")

    for i in range(len(correct_tags)):
        for j in range(len(correct_tags[i])):
            print(str(i) + " " + str(j))
            word_count += 1
            correct_word_tags = {extract_feature_from_short_tag(x, "gender") for x in correct_tags[i][j]}
            parsed_word_tag = extract_feature_from_short_tag(parsed_tags[i][j], "gender")
            parsed_word_tag_num = gender_num[parsed_word_tag]
            is_correct = parsed_word_tag in correct_word_tags
            if is_correct:
                statistics[parsed_word_tag_num][parsed_word_tag_num] += 1
                correct_count += 1
            else:
                outfile.write("\n" + ("-" * 100) + "\n\n")
                outfile.write("sentence: " + str(text[i]) + "\n")
                outfile.write("word: " + text[i][j] + "\n")
                for tag in correct_tags[i][j]:
                    outfile.write(write_tag_comparison_to_file(tag, parsed_tags[i][j]))
                outfile.write("\n" + ("-" * 100) + "\n")
                for correct_word_tag in correct_word_tags:
                    statistics[gender_num[correct_word_tag]][parsed_word_tag_num] += 1

    for short_tag in gender_num:
        outfile.write(("%2s" % str(gender_num[short_tag])) + ": " + gender_beautiful[short_tag] + "\n")
    outfile.write("\n")
    for row in statistics:
        for column in row:
            outfile.write("%7d" % column)
        outfile.write("\n")
    outfile.write("\n\nword count = " + str(word_count))
    outfile.write("\ncorrect gender count = " + str(correct_count))
    outfile.write("\npercent of correct = " + str(correct_count * 100 / word_count))
    outfile.close()


def count_number(destination, correct_tags, parsed_tags, text):

    statistics = [None] * len(number_num)
    for i in range(len(statistics)):
        statistics[i] = [0] * len(number_num)
    correct_count = 0
    word_count = 0

    outfile = open(destination, "w", encoding="utf-8")

    for i in range(len(correct_tags)):
        for j in range(len(correct_tags[i])):
            print(str(i) + " " + str(j))
            word_count += 1
            correct_word_tags = {extract_feature_from_short_tag(x, "number") for x in correct_tags[i][j]}
            parsed_word_tag = extract_feature_from_short_tag(parsed_tags[i][j], "number")
            parsed_word_tag_num = number_num[parsed_word_tag]
            is_correct = parsed_word_tag in correct_word_tags
            if is_correct:
                statistics[parsed_word_tag_num][parsed_word_tag_num] += 1
                correct_count += 1
            else:
                outfile.write("\n" + ("-" * 100) + "\n\n")
                outfile.write("sentence: " + str(text[i]) + "\n")
                outfile.write("word: " + text[i][j] + "\n")
                for tag in correct_tags[i][j]:
                    outfile.write(write_tag_comparison_to_file(tag, parsed_tags[i][j]))
                outfile.write("\n" + ("-" * 100) + "\n")
                for correct_word_tag in correct_word_tags:
                    statistics[number_num[correct_word_tag]][parsed_word_tag_num] += 1

    for short_tag in number_num:
        outfile.write(("%2s" % str(number_num[short_tag])) + ": " + number_beautiful[short_tag] + "\n")
    outfile.write("\n")
    for row in statistics:
        for column in row:
            outfile.write("%7d" % column)
        outfile.write("\n")
    outfile.write("\n\nword count = " + str(word_count))
    outfile.write("\ncorrect number count = " + str(correct_count))
    outfile.write("\npercent of correct = " + str(correct_count * 100 / word_count))
    outfile.close()


def count_case(destination, correct_tags, parsed_tags, text):

    statistics = [None] * len(case_num)
    for i in range(len(statistics)):
        statistics[i] = [0] * len(case_num)
    correct_count = 0
    word_count = 0

    outfile = open(destination, "w", encoding="utf-8")

    for i in range(len(correct_tags)):
        for j in range(len(correct_tags[i])):
            print(str(i) + " " + str(j))
            word_count += 1
            correct_word_tags = {extract_feature_from_short_tag(x, "case") for x in correct_tags[i][j]}
            parsed_word_tag = extract_feature_from_short_tag(parsed_tags[i][j], "case")
            parsed_word_tag_num = case_num[parsed_word_tag]
            is_correct = parsed_word_tag in correct_word_tags
            if is_correct:
                statistics[parsed_word_tag_num][parsed_word_tag_num] += 1
                correct_count += 1
            else:
                outfile.write("\n" + ("-" * 100) + "\n\n")
                outfile.write("sentence: " + str(text[i]) + "\n")
                outfile.write("word: " + text[i][j] + "\n")
                for tag in correct_tags[i][j]:
                    outfile.write(write_tag_comparison_to_file(tag, parsed_tags[i][j]))
                outfile.write("\n" + ("-" * 100) + "\n")
                for correct_word_tag in correct_word_tags:
                    statistics[case_num[correct_word_tag]][parsed_word_tag_num] += 1

    for short_tag in case_num:
        outfile.write(("%2s" % str(case_num[short_tag])) + ": " + case_beautiful[short_tag] + "\n")
    outfile.write("\n")
    for row in statistics:
        for column in row:
            outfile.write("%7d" % column)
        outfile.write("\n")
    outfile.write("\n\nword count = " + str(word_count))
    outfile.write("\ncorrect case count = " + str(correct_count))
    outfile.write("\npercent of correct = " + str(correct_count * 100 / word_count))
    outfile.close()


def count_full(destination, correct_tags, parsed_tags, text):

    correct_count = 0
    word_count = 0
    outfile = open(destination, "w", encoding="utf-8")

    for i in range(len(correct_tags)):
        for j in range(len(correct_tags[i])):
            print(str(i) + " " + str(j))
            word_count += 1
            correct_word_tags = correct_tags[i][j]
            parsed_word_tag = parsed_tags[i][j]
            is_correct = parsed_word_tag in correct_word_tags
            if is_correct:
                correct_count += 1
            else:
                outfile.write("\n" + ("-" * 100) + "\n\n")
                outfile.write("sentence: " + str(text[i]) + "\n")
                outfile.write("word: " + text[i][j] + "\n")
                for tag in correct_tags[i][j]:
                    outfile.write(write_tag_comparison_to_file(tag, parsed_tags[i][j]))
                outfile.write("\n" + ("-" * 100) + "\n")

    outfile.write("\n\nword count = " + str(word_count))
    outfile.write("\ncorrect count = " + str(correct_count))
    outfile.write("\npercent of correct = " + str(correct_count * 100 / word_count))
    outfile.close()


def count_all(destination_directory, parsed_filename):
    correct_tags, parsed_tags, text = set_data("../Data/tags_all.txt", parsed_filename, "../Data/text_all.txt")

    count_full(os.path.join(destination_directory, "full_analysis.txt"), correct_tags, parsed_tags, text)
    count_pos(os.path.join(destination_directory, "pos_analysis.txt"), correct_tags, parsed_tags, text)
    count_gender(os.path.join(destination_directory, "gender_analysis.txt"), correct_tags, parsed_tags, text)
    count_case(os.path.join(destination_directory, "case_analysis.txt"), correct_tags, parsed_tags, text)
    count_number(os.path.join(destination_directory, "number_analysis.txt"), correct_tags, parsed_tags, text)
