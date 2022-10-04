import urllib.request

from browser import document


def create_script_tag(src):
    _fp = urllib.request.urlopen(src)
    _data = _fp.read()

    _tag = document.createElement('script')
    _tag.type = "text/javascript"
    _tag.text = _data
    document.get(tag='head')[0].appendChild(_tag)
