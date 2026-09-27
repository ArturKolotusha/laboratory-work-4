import asyncio
import importlib
import inspect
import json
import os
import re
from pathlib import Path


async def call_function(func, *args):
    result = func(*args)

    if inspect.isawaitable(result):
        result = await result

    return result


async def main():
    try:
        # 1. Читаємо конфігураційний файл
        with open("config.json", "r", encoding="utf-8") as file:
            config = json.load(file)

        text_file = config["text_file"]
        target_language = config["target_language"]
        module_name = config["module"]
        output = config["output"].lower().strip()
        max_sentences = int(config["sentences"])

        # 2. Перевіряємо ім'я модуля
        allowed_modules = {
            "gtrans4_module",
            "gtrans3_module",
            "deeptr_module"
        }

        if module_name not in allowed_modules:
            print("Error: incorrect module name")
            return

        # 3. Перевіряємо існування текстового файла
        if not os.path.exists(text_file):
            print(f"Error: file '{text_file}' not found")
            return

        # 4. Читаємо весь текст
        with open(text_file, "r", encoding="utf-8") as file:
            text = file.read()

        # 5. Отримуємо інформацію про файл
        file_size = os.path.getsize(text_file)
        char_count = len(text)

        sentences = [
            sentence.strip()
            for sentence in re.findall(r"[^.!?]+[.!?]?", text)
            if sentence.strip()
        ]

        sentence_count = len(sentences)

        # 6. Завантажуємо модуль, вказаний у config.json
        module = importlib.import_module(
            f"translator.{module_name}"
        )

        LangDetect = getattr(module, "LangDetect")
        TransLate = getattr(module, "TransLate")
        CodeLang = getattr(module, "CodeLang")

        # 7. Визначаємо мову вхідного тексту
        language = await call_function(
            LangDetect,
            text,
            "lang"
        )

        print("=== File information ===")
        print("File name:", text_file)
        print("File size:", file_size, "bytes")
        print("Characters:", char_count)
        print("Sentences:", sentence_count)
        print("Language:", language)

        # 8. Беремо тільки задану кількість речень
        selected_sentences = sentences[:max_sentences]
        selected_text = " ".join(selected_sentences)

        print("\nSentences to translate:", len(selected_sentences))

        # 9. Перекладаємо
        translated_text = await call_function(
            TransLate,
            selected_text,
            "auto",
            target_language
        )

        if translated_text.startswith("Error:"):
            print(translated_text)
            return

        # 10. Отримуємо назву мови перекладу
        target_name = await call_function(
            CodeLang,
            target_language
        )

        # 11. Вивід на екран
        if output == "screen":
            print("\n=== Translation ===")
            print(
                f"Target language: "
                f"{target_name} ({target_language})"
            )
            print("Module:", module_name)
            print("Translated text:")
            print(translated_text)

        # 12. Вивід у файл
        elif output == "file":
            path = Path(text_file)

            output_file = (
                f"{path.stem}_{target_language}"
                f"{path.suffix}"
            )

            with open(
                output_file,
                "w",
                encoding="utf-8"
            ) as file:
                file.write(translated_text)

            print("Ok")
            print("Output file:", output_file)

        else:
            print("Error: incorrect output parameter")

    except Exception as error:
        print(f"Error: {error}")


if __name__ == "__main__":
    asyncio.run(main())