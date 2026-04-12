import re
from xml.etree.ElementTree import Element
import json


def openURL(url, timeout=5, **kwargs):
    """Open *url* for reading. Raise an :exc:`IOError` if *url* cannot be
    reached.  Small *timeout* values are suitable if *url* is an ip address.
    *kwargs* will be used to make :class:`urllib.request.Request` instance
    for opening the *url*."""

    try:
        from urllib2 import urlopen, URLError, Request
    except ImportError:
        from urllib.request import urlopen, Request
        from urllib.error import URLError

    if kwargs:
        request = Request(url, **kwargs)
    else:
        request = str(url)

    try:
        return urlopen(request, timeout=int(timeout))
    except URLError:
        raise IOError('{0} could not be opened for reading, invalid URL or '
                      'no internet connection'.format(repr(request)))
    
def dictElementLoop(dict_, keys=None, prefix=None, number_multiples=False):

    if isinstance(keys, str):
        keys = [keys]

    if not keys:
        keys = dict_.keys()

    for orig_key in keys:
        item = dict_[orig_key]
        if isinstance(item, Element):
            dict2 = dictElement(dict_[orig_key], prefix, number_multiples)
            finished = False
            while not finished:
                dict3 = dict2.copy()
                try:
                    key = dict2.keys()[0]
                    dict2[key] = dictElement(dict2[key], prefix, number_multiples)
                except:
                    finished = True
                else:
                    dict2 = dict3
                    for key in dict2.keys():
                        dict2[key] = dictElement(dict2[key], prefix, number_multiples)

            dict_[orig_key] = dict2

    return dict_

def dictElement(element, prefix=None, number_multiples=False):
    """Returns a dictionary built from the children of *element*, which must be
    a :class:`xml.etree.ElementTree.Element` instance. Keys of the dictionary
    are *tag* of children without the *prefix*, or namespace. Values depend on
    the content of the child. If a child does not have any children, its text
    attribute is the value. If a child has children, then the child is the
    value.
    """
    
    dict_ = {}
    length = False
    if isinstance(prefix, str):
        length = len(prefix)

    prev_tag = ''
    for child in element:
        tag = child.tag

        if length and tag.startswith(prefix):
            tag = tag[length:]

        if tag != prev_tag:
            prev_tag = tag
            i = 0
        else:
            i += 1

        if number_multiples:
            tag = tag + '{:>4}'.format(str(i))
            
        if len(child) == 0:
            if child.text is None:
                dict_[tag] = child.items()
            else:
                dict_[tag] = child.text
        else:
            dict_[tag] = child

    return dict_

def ALLdictElement(obj, prefix=None, number_multiples=False):
    """Return a pure-Python structure (no Element objects left)."""
    if isinstance(obj, Element):
        # Convert one layer, then keep recursing
        return ALLdictElement(dictElement(obj, prefix, number_multiples),
                            prefix, number_multiples)

    if isinstance(obj, dict):
        return {k: ALLdictElement(v, prefix, number_multiples)
                for k, v in obj.items()}

    if isinstance(obj, (list, tuple)):
        return [ALLdictElement(v, prefix, number_multiples) for v in obj]

    return obj
