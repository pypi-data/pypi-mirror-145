# yomitai
[![PyPI version](https://badge.fury.io/py/yomitai.svg)](https://badge.fury.io/py/yomitai)

CLI Application for quick reference of Japanese-Yomikata.

* <code>pip install yomitai</code>

## Usage
<pre>
<code>$ python -m yomitai [OPTIONS] WORDS
</code></pre>

<pre>
<code>$ yomitai 劈く 
つんざく
</code></pre>

<pre>
<code>$ yomitai --kana 齟齬
ソゴ
$ yomitai --k 齟齬
ソゴ
</code></pre>

<pre>
<code>$ yomitai --romaji 炙りカルビ
aburi karubi
$ yomitai --r 炙りカルビ
aburi karubi
</code></pre>

## TODO
- [ ] add --detail flag using Apple Dictionary or Web Dictionary
