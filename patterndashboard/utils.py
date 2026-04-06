from transformers import pipeline
import re


generator = None


def get_model():
    global generator
    if generator is None:
        generator = pipeline(
            "text-generation",   
            model="google/flan-t5-base",
            max_length=128
        )
    return generator



def build_prompt(filename):
    return f"Filename: {filename}\nRegex:"


def clean_output(output):
    if "Regex:" in output:
        output = output.split("Regex:")[-1]

    output = output.strip().split("\n")[0]
    return output.strip()


def fallback_regex(filename):
    parts = filename.split(".")

    new_parts = []

    for part in parts:
        # Detect date → generalize
        if re.match(r"\d{4}-\d{2}-\d{2}", part):
            new_parts.append("[0-9]{4}-[0-9]{2}-[0-9]{2}")

        # Keep everything else EXACT (including numbers like 10001)
        else:
            new_parts.append(part)

    return ".".join(new_parts)


#  Main function
def generate_regex_from_ai(filename):
    model = get_model()

    prompt = build_prompt(filename)

    try:
        result = model(prompt)
        output = result[0]["generated_text"]

        regex = clean_output(output)

        # Detect bad AI output
        if (
            not regex
            or "filename" in regex.lower()
            or len(regex) < 5
        ):
            regex = fallback_regex(filename)

    except Exception as e:
        print("AI Error:", e)
        regex = fallback_regex(filename)

    return regex


#  Validation
def validate_regex(regex):
    if not regex:
        return False
    try:
        re.compile(regex)
        return True
    except re.error:
        return False