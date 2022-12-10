def removeprefix(s: str, prefix: str) -> str:
    if s.startswith(prefix):
        s = s[len(prefix):]
    return s


def removesuffix(self: str, suffix: str) -> str:
    if self.endswith(suffix):
        return self[:-len(suffix)]
    else:
        return self[:]
