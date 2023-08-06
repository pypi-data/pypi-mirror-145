from .among import Among
from .basestemmer import BaseStemmer


class MaoriStemmer(BaseStemmer):
    a_0 = [
        Among(u"a", -1, 1),
        Among(u"nga", 0, 1),
        Among(u"ia", 0, 1),
        Among(u"ngia", 2, 1),
        Among(u"hia", 2, 1),
        Among(u"whia", 4, 1),
        Among(u"kia", 2, 1),
        Among(u"mia", 2, 1),
        Among(u"ria", 2, 1),
        Among(u"tia", 2, 1),
        Among(u"wh\u00E4ia", 2, 1),
        Among(u"wh\u0101ia", 2, 1),
        Among(u"na", 0, 1),
        Among(u"ina", 12, 1),
        Among(u"whina", 13, 1),
        Among(u"kina", 13, 1)
    ]

    g_v = [17, 65, 16, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 8, 68, 32, 8, 1, 0, 4, 0, 0, 4, 0, 0, 0, 16, 0, 0, 0, 4]

    I_p2 = 0
    I_p1 = 0
    I_pV = 0

    def __r_mark_regions(self):
        self.I_pV = self.limit
        self.I_p1 = self.limit
        self.I_p2 = self.limit
        v_1 = self.cursor
        try:
            if not self.go_out_grouping(MaoriStemmer.g_v, 97, 363):
                raise lab0()
            self.cursor += 1
            self.I_pV = self.cursor
        except lab0: pass
        self.cursor = v_1
        v_2 = self.cursor
        try:
            if not self.go_out_grouping(MaoriStemmer.g_v, 97, 363):
                raise lab1()
            self.cursor += 1
            if not self.go_in_grouping(MaoriStemmer.g_v, 97, 363):
                raise lab1()
            self.cursor += 1
            self.I_p1 = self.cursor
            if not self.go_out_grouping(MaoriStemmer.g_v, 97, 363):
                raise lab1()
            self.cursor += 1
            if not self.go_in_grouping(MaoriStemmer.g_v, 97, 363):
                raise lab1()
            self.cursor += 1
            self.I_p2 = self.cursor
        except lab1: pass
        self.cursor = v_2
        return True

    def __r_RV(self):
        if not self.I_pV <= self.cursor:
            return False
        return True

    def __r_R1(self):
        if not self.I_p1 <= self.cursor:
            return False
        return True

    def __r_R2(self):
        if not self.I_p2 <= self.cursor:
            return False
        return True

    def __r_verb_sfx(self):
        self.ket = self.cursor
        if self.find_among_b(MaoriStemmer.a_0) == 0:
            return False
        self.bra = self.cursor
        if not self.__r_RV():
            return False
        if not self.slice_del():
            return False

        return True

    def _stem(self):
        self.__r_mark_regions()
        self.limit_backward = self.cursor
        self.cursor = self.limit
        v_2 = self.limit - self.cursor
        self.__r_verb_sfx()
        self.cursor = self.limit - v_2
        self.cursor = self.limit_backward
        return True


class lab0(BaseException): pass


class lab1(BaseException): pass
