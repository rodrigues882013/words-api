

class WordService(object):
    @staticmethod
    def min(v1, v2, v3):
        return min(min(v1, v2), v3)

    @staticmethod
    def compute_distance(w1, w2):

        def _range(start, end):
            return range(start, end + 1)

        if w1 is None or w2 is None:
            raise ValueError("Word 1  or Word 2 is not a valid value")

        w1, w2 = w1.lower(), w2.lower()
        m, n = len(w1), len(w2)

        if w1 == w2:
            return 0

        if w1 == "" and w2 != "" or w2 == "" and w1 != "":
            return 0

        result = [[0 for _ in _range(0, n)] for _ in _range(0, m)]

        for i in _range(0, m):
            result[i][0] = i

        for j in _range(0, n):
            result[0][j] = j

        for i in _range(1, m):
            for j in _range(1, n):
                cost = 0 if w1[i - 1] == w2[j - 1] else 1
                result[i][j] = WordService.min(result[i - 1][j] + 1,
                                               result[i][j - 1] + 1,
                                               result[i - 1][j - 1] + cost)

        return result[m][n]

    @staticmethod
    def recursive_version(w1, w2):

        if w1 is None or w2 is None:
            raise ValueError("Word 1  or Word 2 is not a valid value")

        if not w1:
            return len(w1)
        if not w2:
            return len(w2)

        w1, w2 = w1.lower(), w2.lower()

        return min(WordService.recursive_version(w1[1:], w2[1:]) + (w1[0] != w2[0]),
                   WordService.recursive_version(w1[1:], w2) + 1,
                   WordService.recursive_version(w1, w2[1:]) + 1)
