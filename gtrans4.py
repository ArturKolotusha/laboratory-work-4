import asyncio

from translator.gtrans4_module import (
    TransLate,
    LangDetect,
    CodeLang,
    LanguageList
)


async def main():
    text = "Добрий день! Як ваші справи?"

    print("=== TransLate ===")
    print(await TransLate(text, "uk", "en"))

    print("\n=== LangDetect ===")
    print(await LangDetect(text, "lang"))
    print(await LangDetect(text, "confidence"))
    print(await LangDetect(text, "all"))

    print("\n=== CodeLang ===")
    print("uk ->", await CodeLang("uk"))
    print("english ->", await CodeLang("english"))

    print("\n=== LanguageList ===")
    result = await LanguageList("file")
    print("Result:", result)


if __name__ == "__main__":
    asyncio.run(main())