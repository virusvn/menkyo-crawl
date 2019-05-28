import MeCab


class Morph(object):
    kinds = None
    log_stamp = 1000

    @classmethod
    def set_log(cls, num):
        cls.log_stamp = num

    @classmethod
    def set_kind(cls, *args):
        cls.kinds = args
        return cls

    @classmethod
    def reset_kind(cls):
        cls.kinds = None
        return cls

    def set_file(self, file, up_to=100000000):
        fi = codecs.open(file, "r", "utf-8", "ignore")
        self.lines = fi
        return self

    def set_sentence(self, sentence):
        self.lines = sentence.split("\n")
        return self

    def set_chasen(self, s):
        import MeCab

        self.chasen = MeCab.Tagger(s)
        return self

    def set_wakati(self, s):
        import MeCab

        self.wakati = MeCab.Tagger(s)
        return self

    def __init__(self, dic_path=None):
        try:
            self.chasen = MeCab.Tagger("-Ochasen -d {}".format(dic_path))
            self.wakati = MeCab.Tagger("-Owakati -d {}".format(dic_path))
        except:
            self.chasen = MeCab.Tagger("-Ochasen")
            self.wakati = MeCab.Tagger("-Owakati")

    def wakatigaki(self):
        res = ""
        for line in self.lines:
            res += self.wakati.parse(line)
        return res

    def extract(self, feature=True):
        feature_flag = feature
        """return type of list"""
        tagger = self.chasen
        for i, line in enumerate(self.lines):
            line = line.strip()
            if (i + 1) % self.log_stamp == 0:
                print("line {}".format(i + 1))
            # 最後はEOSなので、読み飛ばす
            chunks = tagger.parse(line).splitlines()[:-1]

            for idx, chunk in enumerate(chunks):
                try:
                    # #表層形\t読み\t原型\t品詞なので、(原型、品詞)のみとり出す。
                    _surface, _yomi, origin, feature = chunk.split("\t")[:4]
                except:
                    import traceback

                    print("×", end="/")
                    continue
                origin = origin.lower()
                if Morph.kinds is None:
                    if feature_flag:
                        yield (origin, feature.split("-")[0])
                    elif not feature_flag:
                        yield origin
                    continue
                for kind in Morph.kinds:
                    if feature.startswith(kind):
                        if feature_flag:
                            yield (origin, kind)
                        elif not feature_flag:
                            yield origin
                        break

        return 0
