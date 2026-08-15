"""
Website Scraper Project - main entry point.

Fetches a website's text content and asks a local Llama 3.2 model
(served through Ollama's OpenAI-compatible API) to produce a short,
snarky summary of it.
"""

from openai import OpenAI

from scraper import fetch_website_contents

# Ollama exposes an OpenAI-compatible API locally, so we can reuse
# the OpenAI Python client without needing a paid OpenAI API key.
OLLAMA_BASE_URL = "http://localhost:11434/v1"
OLLAMA_API_KEY = "ollama"  # Required by the client, but ignored by Ollama.
MODEL = "llama3.2"

SYSTEM_PROMPT = """
You are a snarky assistant that analyzes the contents of a website,
and provides a short, snarky, humorous summary, ignoring text that might be navigation related.
Respond in markdown. Do not wrap the markdown in a code block - respond just with the markdown.
"""

USER_PROMPT_PREFIX = """
Here are the contents of a website.
Provide a short summary of this website.
If it includes news or announcements, then summarize these too.

"""


def messages_for(website_text):
    """Build the system/user message list expected by the chat API."""
    return [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": USER_PROMPT_PREFIX + website_text},
    ]


def summarize(client, url):
    """Fetch a website and ask the LLM to summarize its contents."""
    website_text = fetch_website_contents(url)

    response = client.chat.completions.create(
        model=MODEL,
        messages=messages_for(website_text),
    )

    return response.choices[0].message.content


def display_summary(client, url):
    """Print the LLM-generated summary for a given URL."""
    summary = summarize(client, url)
    print(summary)


def main():
    """Ask the user for a URL and print a snarky summary of it."""
    client = OpenAI(base_url=OLLAMA_BASE_URL, api_key=OLLAMA_API_KEY)

    url = input("Enter a URL to summarize: ").strip()
    if not url:
        print("No URL entered. Exiting.")
        return

    print("\nFetching and summarizing...\n")
    display_summary(client, url)


if __name__ == "__main__":
    main()