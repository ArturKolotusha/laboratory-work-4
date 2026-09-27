from googletrans import Translator
from googletrans.constants import LANGUAGES


async def TransLate(text: str, scr: str, dest: str) -> str:
    try:
        async with Translator(raise_exception=True) as translator:
            result = await translator.translate(text, src=scr, dest=dest)

        return result.text

    except Exception as error:
        return f"Error: {error}"
    
async def CodeLang(lang: str) -> str:
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
    
async def LangDetect(text: str, set: str = "all") -> str:
    try:
        async with Translator(raise_exception=True) as translator:
            result = await translator.detect(text)

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

async def LanguageList(out: str = "screen", text: str = "") -> str:
    try:
        out = out.lower().strip()

        if out not in ("screen", "file"):
            return "Error: incorrect out parameter"

        rows = []

        if text:
            header = f"{'Code':<10}{'Language':<25}{'Translation'}"
            rows.append(header)
            rows.append("-" * 70)

            for code, language in LANGUAGES.items():
                translation = await TransLate(text, "auto", code)

                if translation.startswith("Error:"):
                    return translation

                rows.append(
                    f"{code:<10}{language:<25}{translation}"
                )

        else:
            header = f"{'Code':<10}{'Language':<25}"
            rows.append(header)
            rows.append("-" * 35)

            for code, language in LANGUAGES.items():
                rows.append(
                    f"{code:<10}{language:<25}"
                )

        table = "\n".join(rows)

        if out == "screen":
            print(table)

        else:
            with open("languages.txt", "w", encoding="utf-8") as file:
                file.write(table)

        return "Ok"

    except Exception as error:
        return f"Error: {error}"