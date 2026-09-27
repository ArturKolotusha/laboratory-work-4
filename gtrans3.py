from translator.gtrans3_module import (
    CheckPythonVersion,
    TransLate,
    LangDetect,
    CodeLang,
    LanguageList
)


def main():
    text = "Добрий день! Як ваші справи?"

    print("=== Python version ===")
    print(CheckPythonVersion())

    print("\n=== TransLate ===")
    print(TransLate(text, "uk", "en"))

    print("\n=== LangDetect ===")
    print("lang ->", LangDetect(text, "lang"))
    print("confidence ->", LangDetect(text, "confidence"))
    print("all ->", LangDetect(text, "all"))

    print("\n=== CodeLang ===")
    print("uk ->", CodeLang("uk"))
    print("english ->", CodeLang("english"))

    print("\n=== LanguageList ===")
    result = LanguageList("file")
    print("Result:", result)


if __name__ == "__main__":
    main()