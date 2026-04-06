from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json

from .utils import generate_regex_from_ai, validate_regex
from .models import tablelog, generated_patterns


def home(request):
    return render(request, "index.html")


@csrf_exempt
def generate_regex(request):
    if request.method == "POST":
        data = json.loads(request.body)
        filename = data.get("filename")

        # 1️⃣ Generate regex for user input
        regex = generate_regex_from_ai(filename)
        valid = validate_regex(regex)

        if valid:
            generated_patterns.objects.get_or_create(
                filename=filename,
                client="webuser",   # replace with actual client if available
                regex=regex
            )

        # 2️⃣ Scan the entire tablelog for new entries
        for entry in tablelog.objects.all():
            # Skip duplicates: only process if filename not already in generated_patterns
            if not generated_patterns.objects.filter(filename=entry.filename, regex=entry.regex).exists():
                regex_entry = generate_regex_from_ai(entry.filename)
                if validate_regex(regex_entry):
                    generated_patterns.objects.create(
                        filename=entry.filename,
                        client=entry.client,
                        regex=regex_entry
                    )

        return JsonResponse({"regex": regex, "valid": valid})
