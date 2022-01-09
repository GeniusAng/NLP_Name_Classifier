import os
import torch
import glob
import unicodedata
import string

# 所有大小写字母以及空格、句号、逗号、分号、引号，共57个
all_letters = string.ascii_letters + " .,;'"
n_letters = len(all_letters)  # 57


def findFiles(path):
    return glob.glob(path)


# 将Unicode字符转换为ASCII
# 简而言之这个函数的作用就是去除某些语音中的重音标记
# 比如：Ślusàrski --> Slusarski
def unicodeToAscii(s):
    return ''.join(
        c for c in unicodedata.normalize('NFD', s)
        if unicodedata.category(c) != 'Mn'
        and c in all_letters
    )


# 字典category_lines：键为语言，值为保存一个所有名字的列表
# 列表all_categories：保存所有语言名
category_lines = {}
all_categories = []


# 读取文件并进行分割形成列表
def readLines(filename):
    # read()将整个文件读入，strip()去除两侧空白符，使用'\n'进行划分
    lines = open(filename, encoding='utf-8').read().strip().split('\n')
    # 对应每一个lines列表中的名字进行Ascii转换, 使其规范化.最后返回一个名字列表
    return [unicodeToAscii(line) for line in lines]


for filename in findFiles('data/names/*.txt'):
    # findFiles返回了所有文件名
    # basename返回文件名全称，即去除路径
    # splitext将文件名称与后缀分割开，[0]即是取文件名称
    category = os.path.splitext(os.path.basename(filename))[0]
    # 列表all_categories：保存所有语言名
    all_categories.append(category)
    # 字典category_lines：键为语言，值为保存一个所有名字的列表
    lines = readLines(filename)
    category_lines[category] = lines

n_categories = len(all_categories)  # 18


# Find letter index from all_letters, e.g. "a" = 0
def letterToIndex(letter):
    return all_letters.find(letter)


# Turn a line into a <line_length x 1 x n_letters>,
# or an array of one-hot letter vectors
def lineToTensor(line):
    tensor = torch.zeros(len(line), 1, n_letters)
    for li, letter in enumerate(line):
        tensor[li][0][letterToIndex(letter)] = 1
    return tensor
