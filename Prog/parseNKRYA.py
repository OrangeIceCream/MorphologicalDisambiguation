import xml.etree.cElementTree as cET
import os
import json
import POSclasses
from PM import to_short_tag


def parse_xml_file(source):
    tree = cET.parse(source)
    root = tree.getroot()

    file_text = []
    file_tags = []

    for sentence in root.iter('se'):
        sentence_text = []
        sentence_tags = []

        for word in sentence.findall('w'):
            word_tags = []
            word_text = word[-1].tail.replace('`', '')

            for analysis in word.findall('ana'):
                lex = analysis.get('lex')
                gr = analysis.get('gr').replace('=', ',').split(',')
                gr[0] = gr[0].replace('-', '')
                gr = POSclasses.to_pymorphy(word_text, gr, lex)
                word_tags.append(gr)

            sentence_text.append(word_text)
            sentence_tags.append(word_tags)

            punc = word.tail
            if punc is not None:
                punc = punc.replace(' ', '')
                punc = punc.replace('\n', '')
                punc = punc.replace('--', '-')
                if punc != "":
                    sentence_tags.append([to_short_tag({"text": punc, "lex": punc, "pos": "PNCT"})])
                    sentence_text.append(punc)

        file_text.append(sentence_text)
        file_tags.append(sentence_tags)

    return file_text, file_tags


def parse_xml_directory(source, text_destination, tags_destination):
    all_text = []
    all_tags = []
    for filename in os.listdir(source):
        text = []
        tags = []
        if filename.endswith(".xhtml"):
            print(source, filename)
            text, tags = parse_xml_file(os.path.join(source, filename))
        all_text += text
        all_tags += tags

    with open(text_destination, "w", encoding="utf-8") as outfile:
        outfile.write(json.dumps(all_text, indent=4, ensure_ascii=False))
    with open(tags_destination, "w", encoding="utf-8") as outfile:
        outfile.write(json.dumps(all_tags, indent=4, ensure_ascii=False))


if __name__ == "__main__":
    parse_xml_directory("../Data/corpora", "../Data/text_all.txt", "../Data/tags_all.txt")
