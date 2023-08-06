Uyghur toolkit
==============

[中文](README_zh.md)

## Glossary

UEY
: the Uyghur Arabic alphabet, the only official alphabet in the Xinjiang province of China and is widely used in government, social media and in everyday life;

UKY
: the Uyghur Cyrillic alphabet is mostly used by Uyghurs living in Central Asian countries, especially in Kazakhstan;

ULY
: the Uyghur Latin alphabet was introduced in 2008 and is to be used solely in computer-related fields as an ancillary writing system, [6] [5] but has now largely fallen into disuse after the expanded availability of UEY keyboards and keypads on all devices.

UYY
: the mixed Uyghur New Script (also called Pinyin Yeziⱪi or UPNY), this alphabet is also Latin-based, but now most people who want to type in Latin use ULY instead.

## Install

```sh
$ pip install uyghur
```

## Usage

```python
from uyghur.conversion import uey2uly

print(uey2uly('پلام، جهان'))
```

## Testing

Tested in CPython 3.8/3.9/3.10 and Pypy 3.8, install tox globally and run

```shell
tox
```

## TODO

* [x] UEY2ULY
* [ ] ULY2UEY
* [ ] UEY2UKY
* [ ] UKY2UEY
* [ ] UEY2UYY
* [ ] UYY2UEY
* [ ] TEXT2SPEECH

## References

1. DB65/T 3690-2015 Coded Character Conversion Rules between Uyghur and Latin Uyghur
