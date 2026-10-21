import re


def find_emotional_evidence(text):

    text_lower = text.lower()

    evidence = []

    # Anger
    anger_words = [
        "angry",
        "very angry",
        "furious",
        "rage",
        "mad",
        "annoyed",
        "irritated",
        "hate",
        "hateful"
    ]

    # Negative / sadness
    negative_words = [
        "bad",
        "very bad",
        "not good",
        "sad",
        "very sad",
        "unhappy",
        "terrible",
        "horrible",
        "worst",
        "not well",
        "feeling bad",
        "feeling very bad",
        "disappointed",
        "upset"
    ]

    # Happiness
    happy_words = [
        "happy",
        "very happy",
        "glad",
        "excited",
        "excellent",
        "wonderful",
        "amazing",
        "great",
        "good",
        "love",
        "enjoy",
        "enjoyed",
        "pleased"
    ]

    # Fear
    fear_words = [
        "afraid",
        "scared",
        "fear",
        "frightened",
        "terrified",
        "worried",
        "nervous"
    ]

    # Check longest phrases first
    all_words = (
        anger_words +
        negative_words +
        happy_words +
        fear_words
    )

    all_words = sorted(
        all_words,
        key=len,
        reverse=True
    )

    for word in all_words:

        if word in text_lower:

            # Avoid duplicate evidence
            if word not in evidence:
                evidence.append(word)

    return evidence


def explain_emotion(text, emotion):

    evidence = find_emotional_evidence(text)

    # -----------------------------------------
    # No emotional evidence
    # -----------------------------------------

    if not evidence:

        return (
            f'The transcript does not contain strong emotional '
            f'words that clearly explain the prediction. '
            f'The audio emotion model classified the speech as '
            f'{emotion}.'
        )

    # -----------------------------------------
    # Convert evidence to readable text
    # -----------------------------------------

    evidence_text = ", ".join(
        '"' + word + '"'
        for word in evidence[:4]
    )

    # -----------------------------------------
    # Anger
    # -----------------------------------------

    anger_evidence = [
        word for word in evidence
        if word in [
            "angry",
            "very angry",
            "furious",
            "rage",
            "mad",
            "annoyed",
            "irritated",
            "hate",
            "hateful"
        ]
    ]

    if anger_evidence:

        anger_text = ", ".join(
            '"' + word + '"'
            for word in anger_evidence
        )

        return (
            f'The speech may express anger because the speaker '
            f'uses words such as {anger_text}. '
            f'These words suggest strong negative feelings toward '
            f'the person being discussed. The audio emotion model '
            f'classified the speech as {emotion}.'
        )

    # -----------------------------------------
    # Negative / sadness
    # -----------------------------------------

    negative_evidence = [
        word for word in evidence
        if word in [
            "bad",
            "very bad",
            "not good",
            "sad",
            "very sad",
            "unhappy",
            "terrible",
            "horrible",
            "worst",
            "not well",
            "feeling bad",
            "feeling very bad",
            "disappointed",
            "upset"
        ]
    ]

    if negative_evidence:

        negative_text = ", ".join(
            '"' + word + '"'
            for word in negative_evidence
        )

        return (
            f'The speech may express negative feelings because '
            f'the speaker uses words such as {negative_text}. '
            f'These words describe an unpleasant or negative '
            f'situation. The audio emotion model classified the '
            f'speech as {emotion}.'
        )

    # -----------------------------------------
    # Happiness
    # -----------------------------------------

    happy_evidence = [
        word for word in evidence
        if word in [
            "happy",
            "very happy",
            "glad",
            "excited",
            "excellent",
            "wonderful",
            "amazing",
            "great",
            "good",
            "love",
            "enjoy",
            "enjoyed",
            "pleased"
        ]
    ]

    if happy_evidence:

        happy_text = ", ".join(
            '"' + word + '"'
            for word in happy_evidence
        )

        return (
            f'The speech may express positive feelings because '
            f'the speaker uses words such as {happy_text}. '
            f'These words suggest a positive or pleasant feeling. '
            f'The audio emotion model classified the speech as '
            f'{emotion}.'
        )

    # -----------------------------------------
    # Fear
    # -----------------------------------------

    fear_evidence = [
        word for word in evidence
        if word in [
            "afraid",
            "scared",
            "fear",
            "frightened",
            "terrified",
            "worried",
            "nervous"
        ]
    ]

    if fear_evidence:

        fear_text = ", ".join(
            '"' + word + '"'
            for word in fear_evidence
        )

        return (
            f'The speech may express fear or worry because '
            f'the speaker uses words such as {fear_text}. '
            f'These words suggest concern or fear. The audio '
            f'emotion model classified the speech as {emotion}.'
        )

    # -----------------------------------------
    # General evidence
    # -----------------------------------------

    return (
        f'The transcript contains emotional evidence such as '
        f'{evidence_text}. These words may indicate an emotional '
        f'response. The audio emotion model classified the speech '
        f'as {emotion}.'
    )