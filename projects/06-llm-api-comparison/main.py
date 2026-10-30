import argparse
import json
import os
import time
import urllib.error
import urllib.request
from pathlib import Path


def load_dotenv(path=Path(".env")):
    if path.exists():
        for raw in path.read_text(encoding="utf-8").splitlines():
            line = raw.strip()
            if line and not line.startswith("#") and "=" in line:
                key, value = line.split("=", 1)
                os.environ.setdefault(key.strip(), value.strip().strip('"').strip("'"))


def safe_provider(provider):
    return {key: value for key, value in provider.items() if "key" not in key.lower() and "secret" not in key.lower()}


def call(provider, prompt):
    base = os.environ.get(provider["base_url_env"], "").rstrip("/")
    model = os.environ.get(provider["model_env"], "")
    key_name = provider.get("api_key_env")
    key = os.environ.get(key_name, "") if key_name else ""
    if not base or not model:
        raise ValueError("Set the endpoint and model environment variables.")
    if key_name and (not key or key.startswith("replace-")):
        raise ValueError(f"Set {key_name} in the local .env file.")
    data = json.dumps({"model": model, "messages": [{"role": "user", "content": prompt}]}).encode()
    headers = {"Content-Type": "application/json"}
    if key:
        headers["Authorization"] = "Bearer " + key
    request = urllib.request.Request(base + "/chat/completions", data=data, headers=headers)
    with urllib.request.urlopen(request, timeout=30) as response:
        return json.loads(response.read().decode())["choices"][0]["message"]["content"]


def run(smoke=False):
    config = json.loads(Path("providers.example.json").read_text(encoding="utf-8"))
    if smoke:
        print("Providers:", [provider["name"] for provider in config["providers"]])
        print("Redaction check:", safe_provider({"name": "demo", "api_key": "secret"}))
        return config
    load_dotenv()
    prompt = "Explain why citations help document question answering in one sentence."
    for provider in config["providers"]:
        start = time.perf_counter()
        try:
            answer = call(provider, prompt)
            model = os.environ.get(provider["model_env"], "")
            print(f"{provider['name']} ({model}) in {time.perf_counter() - start:.2f}s: {answer}")
        except (ValueError, urllib.error.URLError, TimeoutError, KeyError, json.JSONDecodeError) as exc:
            print(f"{provider['name']}: unavailable ({exc})")
    return config


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--smoke", action="store_true")
    args = parser.parse_args()
    config = run(args.smoke)
    if args.smoke:
        assert len(config["providers"]) >= 2
        assert "api_key" not in safe_provider({"api_key": "secret"})
        print("SMOKE_OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
