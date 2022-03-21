
class MissForestFiller:
    name = "MissForest"
    fname = "MissForest"
    cnname = "随机森林回归"
    @staticmethod
    def fill(ts, oob=False):
        from missingpy import MissForest
        tsc = ts.complete()
        if not oob:
            tc = MissForest().fit_transform(tsc)
            return type(tsc)(data = tc, index=tsc.index, columns=tsc.columns)
        else:
            tc, oobs, oobp = MissForest(oob_score=oob).fit_transform(tsc)
            return type(ts)(datas = tc, indexs=tsc.index, columns=tsc.columns), oobs, oobp