import pymorphy2
import ShortTags


class PM:

    def __init__(self):
        self.morph = pymorphy2.MorphAnalyzer()

    def parse(self, word):
        parses = self.morph.parse(word)
        result = []
        for parse in parses:
            r = dict()
            r["text"] = word
            r["lex"] = parse.normal_form
            r["score"] = parse.score
            tags = parse.tag

            if tags.POS == 'NOUN':
                if "Init" in tags:
                    r["pos"] = "INIT"
                else:
                    r["pos"] = "NOUN"
                    r["gender"] = tags.gender
                    r["case"] = tags.case
                    r["anim"] = tags.animacy
                    r["number"] = tags.number
            elif tags.POS == "ADJF":
                r["pos"] = "ADJF"
                r["gender"] = tags.gender
                r["case"] = tags.case
                r["number"] = tags.number
                if "Supr" in tags:
                    r["comp"] = "Supr"
                if "Anum" in tags:
                    r["other"] = "Anum"
                if "Apro" in tags:
                    r["other"] = "Apro"
            elif tags.POS == "ADJS":
                r["pos"] = "ADJS"
                r["gender"] = tags.gender
                r["number"] = tags.number
            elif tags.POS == "COMP":
                r["pos"] = "COMP"
            elif tags.POS == "NUMR" or "NUMB" in tags:
                r["pos"] = "NUMR"
                r["case"] = tags.case
            elif tags.POS == "INFN":
                r["pos"] = "INFN"
                r["aspect"] = tags.aspect
                r["transitive"] = tags.transitivity
            elif tags.POS == "PRTS":
                r["pos"] = "PRTS"
                r["aspect"] = tags.aspect
                r["tense"] = tags.tense
                r["gender"] = tags.gender
                r["number"] = tags.number
            elif tags.POS == "GRND":
                r["pos"] = "GRND"
                r["aspect"] = tags.aspect
                r["transitive"] = tags.transitivity
                r["tense"] = tags.tense
            elif tags.POS == "PRTF":
                r["pos"] = "PRTF"
                r["aspect"] = tags.aspect
                r["transitive"] = tags.transitivity
                r["tense"] = tags.tense
                r["gender"] = tags.gender
                r["number"] = tags.number
                r["case"] = tags.case
            elif tags.POS == "VERB":
                r["pos"] = "VERB"
                r["aspect"] = tags.aspect
                r["transitive"] = tags.transitivity
                r["tense"] = tags.tense
                r["gender"] = tags.gender
                r["person"] = tags.person
                r["number"] = tags.number
                r["mood"] = tags.mood
            elif tags.POS == "ADVB":
                r["pos"] = "ADVB"
            elif tags.POS == "PRED":
                r["pos"] = "PRED"
            elif tags.POS == "CONJ":
                r["pos"] = "CONJ"
                if "Prnt" in tags:
                    r["other"] = "Prnt"
            elif tags.POS == "NPRO":
                r["pos"] = "NPRO"
                r["gender"] = tags.gender
                r["case"] = tags.case
                r["number"] = tags.number
                r["person"] = tags.person
            elif tags.POS == "PREP":
                r["pos"] = "PREP"
            elif tags.POS == "PRCL":
                r["pos"] = "PRCL"
            elif tags.POS == "INTJ":
                r["pos"] = "INTJ"
            elif "LATN" in tags:
                r["pos"] = "LATN"
            elif "PNCT" in tags:
                r["pos"] = "PNCT"
            else:
                r["pos"] = "XXXX"

            result.append(r)

        return word, [to_short_tag(x) for x in result]

    def parse_and_add_correct(self, parsed_word):
        word = parsed_word[0]
        correct_tags = parsed_word[1]
        result = self.parse(word)
        for correct_tag in correct_tags:
            if correct_tag not in result[1]:
                result[1].append(correct_tag)
        return result


def to_short_tag(dictionary):
    result = dictionary["pos"]
    result += ShortTags.gender[dictionary.get("gender")]
    result += ShortTags.case[dictionary.get("case")]
    result += ShortTags.number[dictionary.get("number")]
    result += ShortTags.anim[dictionary.get("anim")]
    result += ShortTags.comp[dictionary.get("comp")]
    result += ShortTags.aspect[dictionary.get("aspect")]
    result += ShortTags.transitive[dictionary.get("transitive")]
    result += ShortTags.tense[dictionary.get("tense")]
    result += ShortTags.person[dictionary.get("person")]
    result += ShortTags.mood[dictionary.get("mood")]
    result += ShortTags.other[dictionary.get("other")]

    return result


if __name__ == "__main__":
    pm = PM()
    ps = pm.parse_and_add_correct(("кошка", ['NOUNfn-si-------', "bcd"]))
    print(ps)
