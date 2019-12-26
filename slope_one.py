class SlopeOne(object):
    def __init__(self):
        self.diffs = {}
        self.freqs = {}

    def predict(self, userprefs):
        preds, freqs = {}, {}
        for item, rating in userprefs.items():
            for diffitem, diffratings in self.diffs.items():
                try:
                    freq = self.freqs[diffitem][item]
                except KeyError:
                    continue
                preds.setdefault(diffitem, 0.0)
                freqs.setdefault(diffitem, 0)
                preds[diffitem] += freq * (diffratings[item] + rating)
                freqs[diffitem] += freq
        return dict([(item, value / freqs[item])
                     for item, value in preds.items()
                     if item not in userprefs and freqs[item] > 0])

    def update(self, userdata):
        for ratings in userdata.values():
            for item1, rating1 in ratings.items():
                self.freqs.setdefault(item1, {})
                self.diffs.setdefault(item1, {})
                for item2, rating2 in ratings.items():
                    self.freqs[item1].setdefault(item2, 0)
                    self.diffs[item1].setdefault(item2, 0.0)
                    self.freqs[item1][item2] += 1
                    self.diffs[item1][item2] += rating1 - rating2
        for item1, ratings in self.diffs.items():
            for item2 in ratings:
                ratings[item2] /= self.freqs[item1][item2]

if __name__ == '__main__':
    userdata = dict(
        alice=dict(apple=1.5,
                   lemon=1.0,
                   orange=0.7),
        bob=dict(apple=2.0,
                 orange=1.6,
                 guava=0.9),
        carole=dict(apple=1.2,
                    orange=1.0,
                    lemon=0.6,
                    guava=0.4),
        dave=dict(lemon=1.4,
                  orange=0.6,
                  guava=0.8),            

        )
    s = SlopeOne()
    s.update(userdata)
    print (s.predict(dict(apple=1.0)))
