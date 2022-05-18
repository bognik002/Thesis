from math import exp


def mean(x: list):
    return sum(x) / len(x)


def quantile(x: list, q=.5):
    return sorted(x)[round(len(x) * q) - 1]


def std(x: list):
    m = mean(x)
    return (sum([(i - m)**2 for i in x]) / len(x))**.5


def rolling(x: list, n):
    if None not in x:
        return [mean(x[i:i+n]) for i in range(len(x) - n)]
    else:
        res = list()
        for i in range(len(x) - n):
            xs = [el for el in x[i:i+n] if el is not None]
            res.append(mean(xs)) if xs else res.append(None)


def aggregate(types_arr: list, target_arr: list, labels):
    data = {tr_str: list() for tr_str in labels}
    for it in range(len(target_arr)):
        tmp = {tr_str: list() for tr_str in labels}
        for tr_id in target_arr[it].keys():
            if types_arr[it][tr_id] in labels:
                tmp[types_arr[it][tr_id]].append(target_arr[it][tr_id])
        for k, v in tmp.items():
            if v:
                v = mean(v)
            else:
                v = None
            data[k].append(v)
    return data
