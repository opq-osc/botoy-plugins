"""绝绝子生成器
1. 绝绝子更新:  更新词库
2. 绝绝子+{内容}: 内容请使用空格间隔动词与名词，例如：喝奶茶 => 喝 奶茶
"""
import random
from typing import List

from botoy import GroupMsg, S
from botoy import decorators as deco
from botoy.contrib import download, get_cache_dir
from pydantic import BaseModel

data_path = get_cache_dir("juejuezi") / "juejuezi.json"


def download_material():
    download(
        "https://cdn.jsdelivr.net/gh/kingcos/JueJueZiGenerator@main/materials.json",
        data_path,
    )


if not data_path.exists():
    download_material()


class Emotion(BaseModel):
    emoji: List[str]
    xiaohongshu: List[str]
    weibo: List[str]


class Material(BaseModel):
    emotions: Emotion  # 表情
    symbols: List[str]
    auxiliaryWords: List[str]
    dividers: List[str]  # 断句符
    fashion: List[str]  # 潮流
    attribute: List[str]  # 定语

    beginning: List[str]  # 开头
    ending: List[str]  # 结尾
    who: List[str]  # 主语
    someone: List[str]  # 和/跟谁

    todosth: List[str]  # 干什么
    another: List[str]  # 扯另一个淡
    collections: List[str]  # 一些固定搭配
    default: List[str]  # 默认 something


material = Material.parse_file(data_path)


class Random:
    @staticmethod
    def word(words: List[str], nullable=False, divier="") -> str:
        word = random.choice(
            [*words, *([""] * (nullable and int(len(words) / 3) or 0))]
        )
        if word:
            return word + divier
        return ""

    @staticmethod
    def word_not_contain(words: List[str], already: str) -> str:
        word = Random.word(words)

        word_set = set(word.replace(" ", ""))
        already_set = set(already.replace(" ", ""))

        if len(word_set & already_set) == 0:
            return word

        return Random.word_not_contain(words, already)

    @staticmethod
    def words(words_: List[str], count: int) -> List[str]:
        if len(words_) >= count:
            words_ = words_.copy()
            random.shuffle(words_)
        return words_[:count]

    @staticmethod
    def repeat(word: str, times: int = -1) -> str:
        if times > 0:
            return word * times

        num = random.randint(1, 3)
        if num == 2:
            return ""
        return word * num


def generate_beginning(divider: str):
    beginning = (
        Random.word(material.beginning)
        .replace("who", Random.word(material.who))
        .replace("someone", Random.word(material.someone))
    )
    emotion = Random.word(material.emotions.emoji, True)
    return beginning + emotion + divider


def generate_dosth(something: str, divider: str):
    todosth = Random.word(material.todosth).replace(" ", "").replace("dosth", something)
    emotion = Random.repeat(Random.word(material.emotions.emoji))
    return todosth + emotion + divider


def praise_sth(something: str, praised_words: List[str], has_also=False) -> str:
    praise_word = Random.word(praised_words)

    verb, noun = something.split(" ")[:2]

    intro = Random.word(["这家的", "这家店的", "这个", "这件", "这杯"])
    also = has_also and "也" or ""

    praise_word.replace("dosth", verb)

    return intro + noun + also + praise_word


def generate(something: str) -> str:
    divider = Random.word(material.dividers)

    fashion_words = Random.words(material.fashion, len(material.fashion))

    first = generate_beginning(divider)
    second = fashion_words[0] + divider
    third = generate_dosth(something, divider)
    forth = fashion_words[1] + divider
    fifth = Random.repeat(Random.word(material.auxiliaryWords), 3) + divider
    sixth = praise_sth(something, material.attribute) + Random.repeat(
        Random.word(material.symbols), 3
    )
    seventh = praise_sth(
        Random.word_not_contain(material.another, something), material.attribute, True
    ) + Random.repeat(Random.word(material.symbols), 3)
    eighth = fashion_words[2] + divider
    ninth = (
        Random.word(material.collections, True, divider) + fashion_words[3] + divider
    )
    tenth = Random.repeat(Random.word(material.auxiliaryWords), 3) + divider
    last = Random.word(material.ending) + Random.word(material.emotions.emoji)

    return (
        first
        + second
        + third
        + forth
        + fifth
        + sixth
        + seventh
        + eighth
        + ninth
        + tenth
        + last
    )


# bot
@deco.ignore_botself
@deco.startswith("绝绝子")
def receive_group_msg(ctx: GroupMsg):
    do = ctx.Content[3:].strip()
    if not do:
        return

    if do == "更新":
        try:
            download_material()
        except Exception:
            S.bind(ctx).text("下载出错")
        else:
            S.bind(ctx).text("好了，没事不要老更新")
    else:
        try:
            sentence = generate(do)
        except:
            pass
        else:
            S.bind(ctx).text(sentence)


if __name__ == "__main__":
    for _ in range(3):
        print(generate("想 躺平"))
