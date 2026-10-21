from aksharamukha import transliterate


def hindi_to_roman(text):

    roman_text = transliterate.process(
        "Devanagari",
        "IAST",
        text
    )

    # Remove unwanted diacritics
    replacements = {
        "ā": "aa",
        "ī": "ee",
        "ū": "oo",
        "ṛ": "ri",
        "ṃ": "n",
        "ṁ": "n",
        "ñ": "n",
        "ś": "sh",
        "ṣ": "sh",
        "ṭ": "t",
        "ḍ": "d",
        "ṇ": "n",
        "ṭh": "th",
        "ḍh": "dh",
        "ḥ": "h"
    }

    for old, new in replacements.items():
        roman_text = roman_text.replace(old, new)

    # Fix common transliteration differences
    roman_text = roman_text.replace("bahuta", "bahut")

    # Capitalize first letter
    roman_text = roman_text.strip()

    if roman_text:
        roman_text = roman_text[0].upper() + roman_text[1:]

    return roman_text


def translate_to_english(text, source_language):
    """
    Keep this function for future NLLB translation.
    """

    from transformers import AutoTokenizer, AutoModelForSeq2SeqLM

    model_name = "facebook/nllb-200-distilled-600M"

    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForSeq2SeqLM.from_pretrained(model_name)

    tokenizer.src_lang = source_language

    inputs = tokenizer(
        text,
        return_tensors="pt",
        padding=True
    )

    translated_tokens = model.generate(
        **inputs,
        forced_bos_token_id=tokenizer.convert_tokens_to_ids("eng_Latn"),
        max_length=200
    )

    translation = tokenizer.batch_decode(
        translated_tokens,
        skip_special_tokens=True
    )[0]

    return translation