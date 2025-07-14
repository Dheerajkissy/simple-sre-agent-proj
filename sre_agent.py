import os
import datetime
import requests
from dotenv import load_dotenv

def parse_log(file_path):
    errors = []
    warnings = []
    with open(file_path, 'r') as file:
        for line in file:
            if 'ERROR' in line:
                errors.append(line.strip())
            elif 'WARNING' in line:
                warnings.append(line.strip())
    return errors, warnings

def summarize_logs(errors, warnings):
    summary = f"🔍 Log Summary:\n  Errors: {len(errors)}\n  Warnings: {len(warnings)}\n"
    if errors:
        summary += "\n  Error Lines:\n" + "\n".join(f"    - {e}" for e in errors)
    if warnings:
        summary += "\n\n  Warning Lines:\n" + "\n".join(f"    - {w}" for w in warnings)
    return summary

def call_openrouter_gpt(prompt):
    load_dotenv()
    api_key = os.getenv("OPENROUTER_API_KEY")

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
        "HTTP-Referer": "https://github.com/Dheerajkissy/simple-sre-agent-proj",
        "X-Title": "Simple SRE Agent"
    }

    payload = {
	"model": "mistralai/mistral-7b-instruct",
        "messages": [
            {
                "role": "system",
                "content": "You are an SRE assistant. Provide concise, helpful suggestions based on the following log summary."
            },
            {
                "role": "user",
                "content": prompt
            }
        ]
    }

    try:
        response = requests.post("https://openrouter.ai/api/v1/chat/completions", headers=headers, json=payload)
        print(f"\n🔍 Status code: {response.status_code}")
        print(f"🔍 Raw response (first 500 chars):\n{response.text[:500]}")

        if response.status_code == 200 and "application/json" in response.headers.get("content-type", ""):
            result = response.json()
            return result["choices"][0]["message"]["content"].strip()
        else:
            return f"❌ GPT Error: {response.text}"
    except Exception as e:
        return f"❌ GPT Error: {str(e)}"

def save_summary(summary_text):
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    filename = f"summary_{timestamp}.txt"
    with open(filename, "w") as f:
        f.write(summary_text)
    print(f"\n✅ Summary saved to {filename}")

if __name__ == "__main__":
    import sys
    if len(sys.argv) != 2:
        print("Usage: python sre_agent.py <log_file_path>")
        exit(1)

    log_file = sys.argv[1]
    errors, warnings = parse_log(log_file)
    summary = summarize_logs(errors, warnings)
    print(summary)

    gpt_output = call_openrouter_gpt(summary)
    print(f"\n🤖 GPT Suggestion:\n{gpt_output}")

    save_summary(summary + "\n\n🤖 GPT Suggestion:\n" + gpt_output)
