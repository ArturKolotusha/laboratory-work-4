import sys


def CheckPythonVersion() -> str:
    if sys.version_info >= (3, 13):
        return (
            "Error: googletrans 3.1.0a0 is not supported "
            "on Python 3.13 or newer"
        )

    return f"Python {sys.version_info.major}.{sys.version_info.minor} is supported"


if sys.version_info < (3, 13):
    from googletrans import Translator
    from googletrans.constants import LANGUAGES


def TransLate(text: str, scr: str, dest: str) -> str:
    if sys.version_info >= (3, 13):
        return CheckPythonVersion()

    try:
        translator = Translator()
        result = translator.translate(text, src=scr, dest=dest)
        return result.text

    except Exception as error:
        return f"Error: {error}"

def LangDetect(text: str, set: str = "all") -> str:
    if sys.version_info >= (3, 13):
        return CheckPythonVersion()

    try:
        translator = Translator()
        result = translator.detect(text)

        set = set.lower().strip()

        if set == "lang":
            return result.lang

        if set == "confidence":
            return str(result.confidence)

        if set == "all":
            return f"Language: {result.lang}, Confidence: {result.confidence}"

        return "Error: incorrect set parameter"

    except Exception as error:
        return f"Error: {error}"

def CodeLang(lang: str) -> str:
    if sys.version_info >= (3, 13):
        return CheckPythonVersion()

    try:
        lang = lang.lower().strip()

        if lang in LANGUAGES:
            return LANGUAGES[lang]

        for code, name in LANGUAGES.items():
            if name.lower() == lang:
                return code

        return "Error: language not found"

    except Exception as error:
        return f"Error: {error}"

def LanguageList(out: str = "screen", text: str = "") -> str:
    if sys.version_info >= (3, 13):
        return CheckPythonVersion()

    try:
        out = out.lower().strip()

        if out not in ("screen", "file"):
            return "Error: incorrect out parameter"

        rows = []

        if text:
            rows.append(f"{'Code':<10}{'Language':<25}{'Translation'}")
            rows.append("-" * 70)

            for code, language in LANGUAGES.items():
                translation = TransLate(text, "auto", code)

                if translation.startswith("Error:"):
                    return translation

                rows.append(
                    f"{code:<10}{language:<25}{translation}"
                )

        else:
            rows.append(f"{'Code':<10}{'Language':<25}")
            rows.append("-" * 35)

            for code, language in LANGUAGES.items():
                rows.append(
                    f"{code:<10}{language:<25}"
                )

        table = "\n".join(rows)

        if out == "screen":
            print(table)

        else:
            with open(
                "languages_gtrans3.txt",
                "w",
                encoding="utf-8"
            ) as file:
                file.write(table)

        return "Ok"

    except Exception as error:
        return f"Error: {error}"