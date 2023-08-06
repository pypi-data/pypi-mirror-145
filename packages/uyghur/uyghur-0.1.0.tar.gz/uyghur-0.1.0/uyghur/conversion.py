# coding:utf-8
import re
from functools import lru_cache
from unicodedata import lookup, name

_ = lru_cache(lookup)

ARABIC_CHARACTER = (
    r"[\u0600-\u06FF\u0750-\u077F\u08A0-\u08FF\uFB50-\uFDEE\uFE70-\uFEFF]"
)
LATIN_CHARACTER = (
    r"[\u0000-\u024F\u1E00-\u1EFF\u2C60-\u2C7F\uA720-\uA7FF\uFB00-\uFB06\uFF00-\uFF5E]"
)
UYGHUR_VOWEL = "".join(
    (
        _(f"ARABIC LETTER {l}")
        for l in "ALEF|AE|HEH|WAW|U|OE|YU|E|ALEF MAKSURA".split("|")
    )
)
WORDS_SHOULD_BE_CAPITALIZED = ("shinjang", "nemen'gan", "is'haq", "es'et", "ez'her")

UEY2ULY = {
    _("ARABIC LETTER ALEF"): "a",
    _("ARABIC SEQUENCE YEH WITH HAMZA ABOVE WITH ALEF"): "'a",
    _("ARABIC LETTER AE"): "e",
    _("ARABIC LETTER HEH"): "e",
    _("ARABIC SEQUENCE YEH WITH HAMZA ABOVE WITH AE"): "'e",
    _("ARABIC LETTER BEH"): "b",
    _("ARABIC LETTER PEH"): "p",
    _("ARABIC LETTER TEH"): "t",
    _("ARABIC LETTER JEEM"): "j",
    _("ARABIC LETTER TCHEH"): "ch",
    _("ARABIC LETTER KHAH"): "x",
    _("ARABIC LETTER DAL"): "d",
    _("ARABIC LETTER REH"): "r",
    _("ARABIC LETTER ZAIN"): "z",
    _("ARABIC LETTER JEH"): "zh",
    _("ARABIC LETTER SEEN"): "s",
    _("ARABIC LETTER SHEEN"): "sh",
    _("ARABIC LETTER GHAIN"): "gh",
    _("ARABIC LETTER FEH"): "f",
    _("ARABIC LETTER QAF"): "q",
    _("ARABIC LETTER KAF"): "k",
    _("ARABIC LETTER GAF"): "g",
    _("ARABIC LETTER NG"): "ng",
    _("ARABIC LETTER LAM"): "l",
    _("ARABIC LETTER MEEM"): "m",
    _("ARABIC LETTER NOON"): "n",
    _("ARABIC LETTER QAF"): "q",
    _("ARABIC LETTER HEH DOACHASHMEE"): "h",
    _("ARABIC LETTER WAW"): "o",
    _("ARABIC SEQUENCE YEH WITH HAMZA ABOVE WITH WAW"): "'o",
    _("ARABIC LETTER U"): "u",
    _("ARABIC SEQUENCE YEH WITH HAMZA ABOVE WITH U"): "'u",
    _("ARABIC LETTER OE"): "ö",
    _("ARABIC SEQUENCE YEH WITH HAMZA ABOVE WITH OE"): "'ö",
    _("ARABIC LETTER YU"): "ü",
    _("ARABIC SEQUENCE YEH WITH HAMZA ABOVE WITH YU"): "'ü",
    _("ARABIC LETTER VE"): "w",
    _("ARABIC LETTER E"): "ë",
    _("ARABIC SEQUENCE YEH WITH HAMZA ABOVE WITH E"): "'ë",
    _("ARABIC LETTER ALEF MAKSURA"): "i",
    _("ARABIC SEQUENCE YEH WITH HAMZA ABOVE WITH ALEF MAKSURA"): "'i",
    _("ARABIC LETTER YEH"): "y",
    _("ARABIC LETTER YEH WITH HAMZA ABOVE"): "'",
    "\u0632\u06BE": "z'h",
    "\u0633\u06BE": "s'h",
    "\u06AF\u06BE": "g'h",
    "\u0646\u06AF": "n'g",
    _("ARABIC COMMA"): ",",
    _("ARABIC QUESTION MARK"): "?",
    _("ARABIC SEMICOLON"): ";",
}

PRESENTATION2BASIC = {
    _("ARABIC LIGATURE YEH WITH HAMZA ABOVE WITH AE ISOLATED FORM"): _(
        "ARABIC SEQUENCE YEH WITH HAMZA ABOVE WITH AE"
    ),
    _("ARABIC LIGATURE YEH WITH HAMZA ABOVE WITH AE FINAL FORM"): _(
        "ARABIC SEQUENCE YEH WITH HAMZA ABOVE WITH AE"
    ),
    _("ARABIC LETTER HEH ISOLATED FORM"): _("ARABIC LETTER HEH"),
    _("ARABIC LETTER HEH FINAL FORM"): _("ARABIC LETTER HEH"),
    _("ARABIC LETTER ALEF MAKSURA ISOLATED FORM"): _("ARABIC LETTER ALEF MAKSURA"),
    _("ARABIC LETTER ALEF MAKSURA FINAL FORM"): _("ARABIC LETTER ALEF MAKSURA"),
    _("ARABIC LETTER UIGHUR KAZAKH KIRGHIZ ALEF MAKSURA INITIAL FORM"): _(
        "ARABIC LETTER ALEF MAKSURA"
    ),
    _("ARABIC LETTER UIGHUR KAZAKH KIRGHIZ ALEF MAKSURA MEDIAL FORM"): _(
        "ARABIC LETTER ALEF MAKSURA"
    ),
    _("ARABIC LIGATURE YEH WITH HAMZA ABOVE WITH U ISOLATED FORM"): _(
        "ARABIC SEQUENCE YEH WITH HAMZA ABOVE WITH ALEF MAKSURA"
    ),
    _(
        "ARABIC LIGATURE UIGHUR KIRGHIZ YEH WITH HAMZA ABOVE WITH ALEF MAKSURA FINAL FORM"
    ): _("ARABIC SEQUENCE YEH WITH HAMZA ABOVE WITH ALEF MAKSURA"),
    _(
        "ARABIC LIGATURE UIGHUR KIRGHIZ YEH WITH HAMZA ABOVE WITH ALEF MAKSURA INITIAL FORM"
    ): _("ARABIC SEQUENCE YEH WITH HAMZA ABOVE WITH ALEF MAKSURA"),
}

for l in "ALEF|WAW|U|OE|YU".split("|"):
    for lttr_or_lgtr, lttr_or_sqnc in (
        ("LETTER", "LETTER"),
        ("LIGATURE YEH WITH HAMZA ABOVE WITH", "SEQUENCE YEH WITH HAMZA ABOVE WITH"),
    ):
        for f in "ISOLATED|FINAL".split("|"):
            PRESENTATION2BASIC[_(f"ARABIC {lttr_or_lgtr} {l} {f} FORM")] = _(
                f"ARABIC {lttr_or_sqnc} {l}"
            )

for lttr_or_lgtr, lttr_or_sqnc in (
    ("LETTER", "LETTER"),
    ("LIGATURE YEH WITH HAMZA ABOVE WITH", "SEQUENCE YEH WITH HAMZA ABOVE WITH"),
):
    for f in "ISOLATED|FINAL|INITIAL|MEDIAL".split("|"):
        if f == "MEDIAL" and lttr_or_lgtr != "LETTER":
            continue
        PRESENTATION2BASIC[_(f"ARABIC {lttr_or_lgtr} E {f} FORM")] = _(
            f"ARABIC {lttr_or_sqnc} E"
        )

for (
    l
) in "BEH|PEH|TEH|JEEM|TCHEH|KHAH|SEEN|SHEEN|GHAIN|FEH|QAF|KAF|GAF|NG|LAM|MEEM|NOON|HEH DOACHASHMEE|YEH|YEH WITH HAMZA ABOVE".split(
    "|"
):
    for f in "ISOLATED|FINAL|INITIAL|MEDIAL".split("|"):
        PRESENTATION2BASIC[_(f"ARABIC LETTER {l} {f} FORM")] = _(f"ARABIC LETTER {l}")

for l in "DAL|REH|ZAIN|JEH|VE".split("|"):
    for f in "ISOLATED|FINAL".split("|"):
        PRESENTATION2BASIC[_(f"ARABIC LETTER {l} {f} FORM")] = _(f"ARABIC LETTER {l}")


def get_name(char: str) -> str:
    if len(char) == 1:
        return name(char).replace(" ", "_")
    else:
        if char in (
            n := f"ARABIC SEQUENCE YEH WITH HAMZA ABOVE WITH {l}"
            for l in "ALEF|AE|WAW|U|OE|YU|E|ALEF MAKSURA".split("|")
        ):
            return n.replace(" ", "_")
        else:
            return " PLUS ".join(map(name, char)).replace(" ", "_")


def presentation2basic(presentation: str) -> str:
    return "".join((PRESENTATION2BASIC.get(c, c) for c in presentation))


def _uey2uly_conversion(match_object: re.Match) -> str:
    kind = match_object.lastgroup
    value = match_object.group()

    if kind == "IGNORE":
        return value[1:-1]
    elif kind == "ARABIC_TATWEEL_IN_WORD":
        return ""
    elif kind == "ARABIC_LETTER_YEH_WITH_HAMZA_ABOVE_PLUS_UYGHUR_VOWEL":
        return UEY2ULY[match_object.group(2)]
    elif kind == "LATIN_CHARACTER":
        return _("ZERO WIDTH SPACE") + value + _("ZERO WIDTH NO-BREAK SPACE")
    else:
        return UEY2ULY.get(value, value)


def uey2uly(uey: str) -> str:
    basic = presentation2basic(uey)
    expressions = (
        ("IGNORE", r"\u200B[^\uFEFF]+\uFEFF"),
        *((get_name(k), k) for k in sorted(UEY2ULY.keys(), key=len, reverse=True)),
        (
            "ARABIC_TATWEEL_IN_WORD",
            fr"(?<={ARABIC_CHARACTER})\u0640(?={ARABIC_CHARACTER})",
        ),
        ("LATIN_CHARACTER", r"[A-Za-z]+"),
        ("OTHERS", r"[\s\S]"),
    )

    regexp = "|".join(rf"(?P<{grp}>{exp})" for grp, exp in expressions)
    result = "".join(_uey2uly_conversion(mo) for mo in re.finditer(regexp, basic))
    result = re.sub(r"(?<=\W)'(?=[aeiouëöü])", "", result)
    result = re.sub(r"^'(?=[aeiouëöü])", "", result)
    words = []
    abbr = False
    for word in result.split(" "):
        if word in WORDS_SHOULD_BE_CAPITALIZED:
            words.append(word.capitalize())
        else:
            mo = re.match(r"^(ch|gh|sh|zh|ng|[a-zëöü])$", word)
            if mo is not None and abbr:
                words[-1] += word.capitalize()
                continue
            elif mo is not None and not abbr:
                abbr = True
                word = word.capitalize()
            elif abbr:
                abbr = False
            words.append(word)
    result = " ".join(words)
    return result
