import json
import os
import math


def divide_data_to_parts(all_data_file, destination_folder, parts_amount):

    with open(all_data_file, "r", encoding="utf-8") as infile:
        all_data = json.loads(infile.read(), encoding="utf-8")

    word_count = 0
    for sent in all_data:
        word_count += len(sent)

    part_size = int(math.ceil(word_count / parts_amount))
    cur_part_size_sent = 0
    cur_part_size_word = 0
    cur_part_num = 0
    part_sizes = [0] * (parts_amount + 1)
    part_word_sizes = [0] * parts_amount

    for sent in all_data:
        if cur_part_size_word >= part_size:
            part_sizes[cur_part_num+1] = cur_part_size_sent
            part_word_sizes[cur_part_num] = cur_part_size_word
            cur_part_num += 1
            cur_part_size_sent = 0
            cur_part_size_word = 0

        cur_part_size_sent += 1
        cur_part_size_word += len(sent)

    if part_sizes[parts_amount] == 0:
        part_sizes[parts_amount] = cur_part_size_sent
        part_word_sizes[parts_amount-1] = cur_part_size_word

    print(part_sizes)
    print(sum(part_sizes))
    print(part_word_sizes)
    print(sum(part_word_sizes))
    print(len(all_data))

    for i in range(parts_amount):
        print(i)
        destination_file = str(parts_amount) + "_" + str(i) + ".txt"
        with open(os.path.join(destination_folder, destination_file), "w", encoding="utf-8") as outfile:
            begin = sum(part_sizes[0:i+1])
            end = begin + part_sizes[i+1]
            outfile.write(json.dumps(all_data[begin:end], indent=4, ensure_ascii=False))


if __name__ == "__main__":
    divide_data_to_parts("../Data/text_all.txt", "../Data/parts/text", 10)
    divide_data_to_parts("../Data/tags_all.txt", "../Data/parts/tags", 10)
