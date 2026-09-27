from deep_translator import GoogleTranslator, MyMemoryTranslator
from langdetect import detect_langs

def _to_mymemory_language(lang: str, text: str = "") -> str:
    lang = lang.lower().strip()

    # MyMemory не покладаємося на "auto":
    # визначаємо мову самі через langdetect
    if lang == "auto":
        if not text.strip():
            raise ValueError("Cannot detect language from empty text")

        lang = detect_langs(text)[0].lang.lower()

    # Отримуємо таблицю мов MyMemory.
    # en-GB та en-US гарантовано є допустимими кодами.
    supported = MyMemoryTranslator(
        source="en-GB",
        target="en-US"
    ).get_supported_languages(as_dict=True)

    # Якщо передана назва: "english", "ukrainian"...
    if lang in supported:
        return supported[lang]

    # Якщо вже переданий повний код: "en-US", "uk-UA"...
    for code in supported.values():
        if code.lower() == lang:
            return code

    # Якщо короткий код: "en", "uk", "de"...
    for code in supported.values():
        if code.lower().split("-")[0] == lang:
            return code

    raise ValueError(f"Unsupported MyMemory language: {lang}")

def TransLate(text: str, scr: str, dest: str) -> str:
    try:
        return GoogleTranslator(
            source=scr,
            target=dest
        ).translate(text)

    except Exception as google_error:
        try:
            source = _to_mymemory_language(scr, text)
            target = _to_mymemory_language(dest)

            return MyMemoryTranslator(
                source=source,
                target=target
            ).translate(text)

        except Exception as memory_error:
            return (
                f"Error: GoogleTranslator: {google_error}; "
                f"MyMemoryTranslator: {memory_error}"
            )

def LangDetect(text: str, set: str = "all") -> str:
    try:
        results = detect_langs(text)

        if not results:
            return "Error: language not detected"

        best = results[0]
        lang = best.lang
        confidence = best.prob

        set = set.lower().strip()

        if set == "lang":
            return lang

        if set == "confidence":
            return str(confidence)

        if set == "all":
            return f"Language: {lang}, Confidence: {confidence}"

        return "Error: incorrect set parameter"

    except Exception as error:
        return f"Error: {error}"

def CodeLang(lang: str) -> str:
    try:
        lang = lang.lower().strip()

        languages = GoogleTranslator(
            source="auto",
            target="en"
        ).get_supported_languages(as_dict=True)

        # Назва мови -> код
        if lang in languages:
            return languages[lang]

        # Код -> назва мови
        for name, code in languages.items():
            if code.lower() == lang:
                return name

        return "Error: language not found"

    except Exception as error:
        return f"Error: {error}"

def LanguageList(out: str = "screen", text: str = "") -> str:
    try:
        out = out.lower().strip()

        if out not in ("screen", "file"):
            return "Error: incorrect out parameter"

        languages = GoogleTranslator(
            source="auto",
            target="en"
        ).get_supported_languages(as_dict=True)

        rows = []

        if text:
            rows.append(f"{'Code':<10}{'Language':<25}{'Translation'}")
            rows.append("-" * 70)

            for language, code in languages.items():
                translation = TransLate(text, "auto", code)

                if translation.startswith("Error:"):
                    return translation

                rows.append(
                    f"{code:<10}{language:<25}{translation}"
                )

        else:
            rows.append(f"{'Code':<10}{'Language':<25}")
            rows.append("-" * 35)

            for language, code in languages.items():
                rows.append(
                    f"{code:<10}{language:<25}"
                )

        table = "\n".join(rows)

        if out == "screen":
            print(table)

        else:
            with open(
                "languages_deeptr.txt",
                "w",
                encoding="utf-8"
            ) as file:
                file.write(table)

        return "Ok"

    except Exception as error:
        return f"Error: {error}"