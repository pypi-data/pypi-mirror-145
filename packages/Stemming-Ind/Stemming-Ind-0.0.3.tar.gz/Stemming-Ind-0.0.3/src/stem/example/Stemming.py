import re


class Stemming():

    def dasar(self, kata):
        vocal = ["a","i","u","e","o"]
        if (len(kata) > 4):
            if (kata[len(kata)-2:] == "ku" or kata[len(kata)-2:] == "mu"):
                kata = kata[:len(kata)-2]
            else:
                if (kata[len(kata)-6:] == "kannya"):
                    kata = kata[:len(kata)-3]
                elif (kata[len(kata)-5:] == "annya") and len(kata) > 8:
                    kata = kata[:len(kata)-5]
                else:
                    if (kata[len(kata)-3:] == "nya"):
                        kata = kata[:len(kata)-3]

        if (kata[:2] == "me"):
            if (kata[:3] == "mem"):
                if (kata[3:4] == "a" or kata[3:4] == "i" or kata[3:4] == "e" or kata[3:4] == "u" or kata[3:4] == "o"):
                    if (
                        # (kata[4:5] == "s" and kata.[5, 6] != "t") or
                        ((kata[4:5] == "l" or
                            kata[len(kata)-1:] == "m" or
                            kata[len(kata)-1:] == "k") and
                            kata[len(kata)-1:] != "n") or
                        (kata[len(kata)-1:] == "n" and len(kata) <= 7)
                    ):
                        kata = "m" + kata[3:len(kata)]
                    else:
                        kata = "p" + kata[3:len(kata)]
                else:
                    kata = kata[3:len(kata)]

            else:
                if (kata[:3] == "men"):
                    if (kata[3:4] in vocal):
                        if ((kata[3:4] == "i" and kata[6:7] == "h") or kata[4:5] == "i") or (kata[4:5] in vocal):
                            kata = "n" + kata[3:len(kata)]
                        else:
                            kata = "t" + kata[3:len(kata)]
                    else:
                        if (kata[:4] == "meng"):
                            if (
                                kata[4:5] == "a" or
                                kata[4:5] == "e" or
                                kata[4:5] == "o" or
                                kata[4:5] == "u"
                            ):
                                if (
                                    (len(self.suffix(kata[4:len(kata)])) > 5 and
                                     kata[len(kata)-1:] != "t") or
                                    (kata[len(kata)-1:] == "p" and kata[5:6] == "c") or
                                    (kata[4:5] == "e" and (kata[5:6] == "m" or kata[5:6] == "j" or kata[6:7] == "j")) or
                                    kata[len(kata)-3:] == "lah"
                                ):
                                    kata = "k" + kata[4:len(kata)]
                                else:
                                    kata = kata[4:len(kata)]

                            else:
                                kata = kata[4:len(kata)]
                        else:
                            if (kata[:4] == "meny"):
                                kata = "s" + kata[4:len(kata)]
                            else:
                                kata = kata[3:len(kata)]
                else:
                    if (len(kata) > 5):
                        kata = kata[:2]
        else:
            if (kata[:4] == "peng"):
                if (kata[4:5] == "e"):
                    kata = "k" + kata[4:len(kata)]
                else:
                    kata = kata[4:len(kata)]
            else:
                if (kata[:3] == "pem"):
                    if (kata[6: 7] != "r"):
                        if (
                            kata[3:4] == "a" or
                            kata[3:4] == "i" or
                            kata[3:4] == "e" or
                            kata[3:4] == "u" or
                            kata[3:4] == "o"
                        ):
                            kata = "p" + kata[3:len(kata)]
                        else:
                            kata = kata[3:len(kata)]
                    else:
                        kata = "m" + kata[3:len(kata)]

                else:
                    if (kata[:4] == "peny"):
                        kata = "s" + kata[4:len(kata)]
                    elif (kata[:3] == "pen"):
                        if (
                            kata[3:4] == "a" or
                            kata[3:4] == "i" or
                            kata[3:4] == "e" or
                            kata[3:4] == "u" or
                            kata[3:4] == "o"
                        ):
                            kata = "t" + kata[3:len(kata)]
                        else:
                            kata = kata[3:len(kata)]
                    else:
                        if (kata[:2] == "di"):
                            kata = kata[2: len(kata)]
                        else:
                            if (kata[:3] == "ter"):
                                kata = kata[3:len(kata)]
                            else:
                                if (kata[:2] == "ke"):
                                    if (kata[2:3] == "m" or kata[2:3] == "l"):
                                        kata = kata
                                    else:
                                        if (kata[2:3] != "n" and len(kata) > 5):
                                            kata = kata[2: len(kata)]

        if (kata[:2] == "be"):
            if (kata[2:3] == "k"):
                kata = kata[2: len(kata)]
            else:
                if (kata[:3] == "bel"):
                    kata = kata[3:len(kata)]
                else:
                    if (kata[:3] == "ber"):
                        if (
                            kata[3:6] == "sih" or
                            kata[3:6] == "ani" or
                            kata[3:7] == "ikan"
                        ):
                            # ==
                            kata = kata
                        else:
                            if (kata[3:4] == "i"):
                                kata = kata[2:len(kata)]
                            else:
                                kata = kata[3:len(kata)]

        else:
            if (kata[:3] == "per" and len(kata[3:len(kata)]) > 5):
                kata = kata[3:len(kata)]
            else:
                if (kata[:3] == "pel" and len(kata) > 5):
                    kata = kata[3:len(kata)]
                else:
                    if (kata[:2] == "se" and len(kata) > 5):
                        if (kata[2:3] == "t"):
                            kata = kata[2: len(kata)]
                    else:
                        if (kata[:2] == "pe" and len(kata[:2]) > 5):
                            if (kata[2:3] == "r" and len(kata[:3]) > 5):
                                kata = kata[3:len(kata)]
                            else:
                                if (kata[2:3] == "l" and len(kata) > 5):
                                    if (kata[4:5] == "y"):
                                        kata = kata[2: len(kata)]
                                    else:
                                        kata = kata[3:len(kata)]
                                else:
                                    if (len(self.suffix(kata[2: len(kata)])) > 4):
                                        kata = kata[2: len(kata)]

        kata = self.suffix(kata)
        if (len(kata) == 1):
            kata = ""

        return kata

    def suffix(self, kata):
        prefix = "kah|lah|pun|me|mem|men|meng|meny|peng|pem|pen|peny|di|ter|ke|kem|ken|be|bek|bel|ber|per|pel|se"

        regex = re.compile(prefix)
        str = regex.sub('', kata.lower()).split(" ")

        if ((kata[len(kata)-3:] == "kah" and len(kata) > 7) or (len(kata) > 5 and kata[len(kata)-3:] == "lah") or kata[len(kata)-3:] == "pun"):
            kata = kata[:len(kata)-3]

        if (kata[len(kata)-1:] == "i"):
            if (len(str) > 5):
                if (kata[(len(kata) - 3):(len(kata) - 1)] != "rt"):
                    kata = kata[:len(kata) - 1]
            elif (len(kata) > 5) and (("l" not in kata) and ("m" not in kata) and ("n" not in kata)):
                kata = kata[:len(kata) - 1]
        else:
            if (kata[len(kata)-2:] == "an"):
                if (kata[len(kata)-3:] != "ian"):
                    if (kata[len(kata)-3:] == "kan"):
                        if (kata[:len(kata)-4] == "ikan"):
                            if (kata[len(kata)-4: (len(kata)-3)] == "p"):
                                kata = kata[len(kata)-3:] + "an"
                            else:
                                if (kata[len(kata)-4: (len(kata)-3)] == "l"):
                                    kata = kata[:len(kata)-3]
                                else:
                                    kata = kata[:len(kata)-3]
                        else:
                            if (len(kata) > 5):
                                kata = kata[:len(kata)-3]
                    elif (len(kata) > 5) and kata[:4] != "deng" and ("u" not in kata) or kata[len(kata)-4:] == "iman":
                        kata = kata[:len(kata)-2]

        return kata

    def stem(self, kalimat):
        if (kalimat != ""):
            str = ""
            regex = re.compile('[^a-zA-Z]')
            ark = regex.sub(" ", kalimat.lower()).split(" ")
            for kata in ark:
                kata = kata.strip()
                dasar = self.dasar(kata)
                if dasar != "":
                    str = str + " " + dasar

            return str.strip()

        return ""
