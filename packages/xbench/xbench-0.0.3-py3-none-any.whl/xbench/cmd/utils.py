import os


def doc_dir(n):
    return "doc-%d" % n


# https://stackoverflow.com/questions/712460/interpreting-number-ranges-in-python
def parse_int_set(nputstr=""):
    selection = set()
    invalid = set()
    # tokens are comma seperated values
    tokens = [x.strip() for x in nputstr.split(",")]
    for i in tokens:
        if len(i) > 0:
            if i[:1] == "<":
                i = "1-%s" % (i[1:])
        try:
            # typically tokens are plain old integers
            selection.add(int(i))
        except:
            # if not, then it might be a range
            try:
                token = [int(k.strip()) for k in i.split("-")]
                if len(token) > 1:
                    token.sort()
                    # we have items seperated by a dash
                    # try to build a valid range
                    first = token[0]
                    last = token[len(token) - 1]
                    for x in range(first, last + 1):
                        selection.add(x)
            except:
                # not an int and not a range...
                invalid.add(i)
    # Report invalid tokens before returning valid selection
    if len(invalid) > 0:
        raise "Invalid set: " + str(invalid)
    return selection


def environ_or_required(key, default=None):
    return (
        {"default": os.environ.get(key, default)}
        if os.environ.get(key, default) is not None
        else {"required": True}
    )
