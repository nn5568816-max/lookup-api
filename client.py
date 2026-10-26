
import json
import os
import urllib.error
import urllib.parse
import urllib.request

BASE_URL = os.getenv(
    "LOOKUP_API_BASE",
    "https://YOUR-PROJECT.vercel.app"
)


def lookup(endpoint, params):
    query = urllib.parse.urlencode(params)
    url = f"{BASE_URL.rstrip('/')}/api/{endpoint}?{query}"

    request = urllib.request.Request(
        url,
        headers={"Accept": "application/json"},
        method="GET"
    )

    try:
        with urllib.request.urlopen(request, timeout=15) as response:
            result = json.loads(response.read().decode("utf-8"))
            print(json.dumps(result, indent=2))
            return result
    except urllib.error.HTTPError as exc:
        print(f"API error: HTTP {exc.code}")
        return None
    except (urllib.error.URLError, TimeoutError, ValueError) as exc:
        print(f"Request failed: {exc}")
        return None


if __name__ == "__main__":
    print("\n--- IFSC ---")
    lookup("ifsc", {"ifsc": "SBIN0000001"})

    print("\n--- Aadhaar format check ---")
    # Use only a test value or your own number.
    # This endpoint returns a masked value, not identity details.
    lookup("aadhaar", {"id": "234567890124"})

    print("\n--- Vehicle ---")
    lookup("vehicle", {"registration": "HR55AL0051"})
