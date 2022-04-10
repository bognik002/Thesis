def mean(x: list):
    return sum(x) / len(x)


def quantile(x: list, q=.5):
    return sorted(x)[round(len(x) * q) - 1]


def std(x: list):
    m = mean(x)
    return (sum([(i - m)**2 for i in x]) / len(x))**.5
