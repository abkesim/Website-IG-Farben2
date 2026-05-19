import anthropic
import os
from datetime import date
from pathlib import Path


def generate_newsletter():
    client = anthropic.Anthropic()

    today = date.today().strftime("%B %d, %Y")
    today_iso = date.today().isoformat()

    response = client.messages.create(
        model="claude-opus-4-7",
        max_tokens=4096,
        tools=[
            {
                "type": "web_search_20250305",
                "name": "web_search",
                "max_uses": 15,
            }
        ],
        messages=[
            {
                "role": "user",
                "content": (
                    f"Research and write a daily AI newsletter for {today}.\n\n"
                    "Cover these three topics specifically:\n"
                    "1. **Data center power supply** — new energy deals, infrastructure announcements, power consumption news\n"
                    "2. **New local / open-source AI models** — models released to run locally (Ollama, HuggingFace, llama.cpp compatible, etc.)\n"
                    "3. **Big company model releases** — new models from Google, Anthropic, OpenAI, Meta, xAI, Mistral, etc.\n\n"
                    "Structure the output as Markdown with exactly these three sections:\n\n"
                    "## What's New Today\n"
                    "(News from the last 24 hours)\n\n"
                    "## What's New This Week\n"
                    "(Key developments from the last 7 days)\n\n"
                    "## What's New This Month\n"
                    "(Major trends and releases from the last 30 days)\n\n"
                    "Under each section, cover all three topics where relevant with 2–4 bullet points.\n"
                    "Be specific: include model names, benchmark numbers, company names, and dates.\n"
                    "Keep each bullet to 2–3 sentences max.\n"
                    "Do not add any commentary outside the three sections."
                ),
            }
        ],
    )

    text_blocks = [block.text for block in response.content if hasattr(block, "text")]
    newsletter_body = "\n\n".join(text_blocks)

    newsletters_dir = Path("newsletters")
    newsletters_dir.mkdir(exist_ok=True)

    output_path = newsletters_dir / f"{today_iso}.md"
    output_path.write_text(
        f"# AI Newsletter — {today}\n\n{newsletter_body}\n",
        encoding="utf-8",
    )

    index_path = newsletters_dir / "README.md"
    existing_entries = []
    if index_path.exists():
        for line in index_path.read_text(encoding="utf-8").splitlines():
            if line.startswith("- ["):
                existing_entries.append(line)

    new_entry = f"- [{today_iso}]({today_iso}.md)"
    if new_entry not in existing_entries:
        existing_entries.insert(0, new_entry)

    index_path.write_text(
        "# AI Newsletter Archive\n\n" + "\n".join(existing_entries[:60]) + "\n",
        encoding="utf-8",
    )

    print(f"Newsletter saved: {output_path}")


if __name__ == "__main__":
    generate_newsletter()
