import os
import json
from typing import List, Dict
from dotenv import load_dotenv

from src.youtube_fetcher import YouTubeFetcher


LEVEL_QUERIES = {
    "beginner": "beginner guitar lessons tutorial",
    "intermediate": "intermediate guitar lessons tutorial",
    "advanced": "advanced guitar lessons tutorial",
}

# Load variables from .env automatically
load_dotenv()

def fetch_all_levels(
    api_key: str,
    max_per_level: int = 200,
    transcripts: bool = False,
) -> List[Dict]:
    """
    Fetch YouTube video metadata for beginner, intermediate,
    and advanced guitar lessons and combine into one list.
    """

    fetcher = YouTubeFetcher(api_key=api_key)
    all_results: List[Dict] = []

    for level, query in LEVEL_QUERIES.items():
        print(f"\nFetching {level} videos...")
        results = fetcher.search_and_fetch(
            query=query,
            max_results=max_per_level,
            transcripts=transcripts,
        )

        # Tag each video with its level
        for video in results:
            video["lesson_level"] = level

        all_results.extend(results)
        print(f"{len(results)} videos fetched for {level}")

    return all_results


def main():
    api_key = os.getenv("YOUTUBE_API_KEY")
    if not api_key:
        raise RuntimeError("YOUTUBE_API_KEY not found in environment variables")

    combined_results = fetch_all_levels(
        api_key=api_key,
        max_per_level=2000,
        transcripts=True,
    )

    print(f"\nTotal videos collected: {len(combined_results)}")

    output_path = "data/raw/guitar_lessons_all_levels.json"
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(combined_results, f, ensure_ascii=False, indent=2)

    print(f"Saved to {output_path}")


if __name__ == "__main__":
    main()
