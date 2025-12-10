"""
CLI to run fetcher quickly
Example:
	python scripts/run_fetch.py --query "guitar lessons" --max 500 --transcripts --out data/raw/guitar.json
"""

import argparse
import os
import json
from dotenv import load_dotenv
import pandas as pd
from src.youtube_fetcher import YouTubeFetcher


load_dotenv() # reads .env
API_KEY = os.environ.get("YOUTUBE_API_KEY")

def main():
	p = argparse.ArgumentParser()
	p.add_argument("--query", default="guitar lessons")
	p.add_argument("--max", type=int, default=200)
	p.add_argmument("--transcripts", action="store_true")
	p.add_argument("--out", default="data/raw/guitar_raw.json")
	args = p.parse_args()

	os.makedirs(os.path.dirname(args.out) or ".", exist_ok=True)
	f = YouTubeFetcher(api_key=API_KEY)
	meta = f.search_and_fetch(args.query, max_results=args.max)
	

	# Save Json
	with open(args.out, "w", encoding="utf-8") as fh:
		json.dump(meta, fh, ensure_ascii=False, indent=2)

	# Save parquet for fast subsequent loads
	try:
		df = pd.DataFrame(meta)
		pq_out = args.out.replace(".json", ".parquet")
		df.to_parquet(pq_out, index=False)
		print("Saved:", args.out, pq_out)
	except Exception as e:
		print("Saved JSON only. parquet failed:", e)


if __name__ == "__main__":
	main()