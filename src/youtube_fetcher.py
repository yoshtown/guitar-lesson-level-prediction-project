"""
youtube_fetcher.py
Functions:
- search_video_ids(query, max_results)
- get_videos_metadata(video_ids)
- search_and_fetch(query, max_results, transcripts=True)
"""

import os
import time
import math
import logging
from typing import List, Dict, Optional
from googleapiclient.discovery import build
import json
from rapidfuzz import fuzz, process

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = "v3"
SEARCH_PAGE_SIZE = 50 # YouTube max per search page

class YouTubeFetcher:
	def __init__(self, api_key: str, rate_limit_pause: float = 0.8):
		if not api_key:
			raise ValueError("YouTube API key required")
		self.api_key = api_key
		self.youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION, developerKey=api_key)
		self.rate_limit_pause = rate_limit_pause

	def search_video_ids(self, query: str, max_results: int = 200) -> List[str]:
		video_ids = []
		next_page_token = None
		total_pages = math.ceil(max_results / SEARCH_PAGE_SIZE)
		fetched = 0

		for _ in range(total_pages):
			to_fetch = min(SEARCH_PAGE_SIZE, max_results - fetched)
			req = self.youtube.search().list(
					q=query,
					part="id",
					type="video",
					maxResults=to_fetch,
					pageToken=next_page_token
				)
			resp = req.execute()
			for item in resp.get("items", []):
				vid = item.get("id", {}).get("videoId")
				if vid:
					video_ids.append(vid)
				fetched = len(video_ids)
				next_page_token = resp.get("nextPageToken")
				logger.info("Collected %d/%d ids", fetched, max_results)
				if not next_page_token or fetched >= max_results:
					break
				time.sleep(self.rate_limit_pause)

		return video_ids[:max_results]

	def get_videos_metadata(self, video_ids: List[str]) -> List[Dict]:
		out = []
		BATCH = 50

		if not video_ids:
			logger.warning("get_videos_metadata called with empty video_ids list")
			return out

		logger.info("Fetching metadata for %d video IDs", len(video_ids))

		# print("before first loop in get_videos_metadata()")
		for i in range(0, len(video_ids), BATCH):
			batch = video_ids[i:i+BATCH]
			resp = self.youtube.videos().list(
					part="snippet,statistics,contentDetails",
					id=",".join(batch)
				).execute()

			# is_full = bool(resp.get("items", []))
			items = resp.get("items", [])
			logger.info("Recieved %d items in metadata batch %d", len(items), i // BATCH + 1)

			# print(f"Inside first loop in get_videos_metadata(), resp: {is_full}")
			for item in items:
				# print("Inside nested loop in get_videos_metadata()")
				snippet = item.get("snippet", {})
				stats = item.get("statistics", {})
				content = item.get("contentDetails", {})

				logger.info("Fetched video: %s (%s)",
							snippet.get("title"),
							snippet.get("publishedAt"))

				title = snippet.get("title", "") or ""
				description = snippet.get("description", "") or ""

				levels = {
					"beginner": ["beginner", "basic", "fundamental", "easy" "open chord", "sus"],
					"intermediate": ["intermediate", "bar chord", 
								"7th", "seventh", "add9",
								"beautiful chord", "add6/9"],
					"advance": ["advance", "4th chord", "fourth chord" "Drop 2 voicings"]
				}

				priority = {
					"advanced": 3,
					"intermediate": 2,
					"beginner": 1
				}

				level = detect_level(title, description, levels, priority)

				# beginner = ["beginner", "basic", "open chord", "sus"]
				# intermediate = ["intermediate", "bar chord", 
				# 				"7th", "seventh", "add9",
				# 				"beautiful chord", "add6/9"]
				# advanced = ["advance", "4th chord", "fourth chord" "Drop 2 voicings"]

				# level = "unknown"
				topic = ""

				# title_1 = title.lower()
				# description_1 = description.lower()
				# text = f"{title} {description}".lower()


				# for lvl_name, keywords in levels.items():
				# 	if any(fuzzy_contains(kw, text) for kw in keywords):
				# 		level = lvl_name
				# 		break

				# for lvl_name, keywords in levels.items():
				# 	if any(kw in title_1 or kw in description_1 for kw in keywords):
				# 		level = lvl_name
				# 		break

				# if beginner in title.lower() or beginner in description.lower():
				# 	level = beginner
				# elif intermediate in title.lower() or intermediate in description.lower():
				# 	level = intermediate
				# elif advanced in title.lower() or advanced in description.lower():
				# 	level = advanced
				# else:	level = "unknown"
				# 

				out.append({
						"video_id": item.get("id"),
						"title": snippet.get("title"),
						"description": snippet.get("description"),
						"tags": snippet.get("tags", []),
						"publishedAt": snippet.get("publishedAt"),
						"channelTitle": snippet.get("channelTitle"),

						"viewCount": int(stats.get("viewCount")) if stats.get("viewCount") else None,
						"likeCount": int(stats.get("likeCount")) if stats.get("likeCount") else None,

						"duration" : content.get("duration"),

						"raw_snippet": snippet,
						"raw_statistics": stats,
						#"raw_contentDetails": content,

						"level": level,
						"topic": topic
					})
				time.sleep(self.rate_limit_pause)

		logger.info("Finished collecting metadata for %d videos", len(out))
		return out


	def search_and_fetch(self, query: str, max_results: int = 200, transcripts: bool = False):
		ids = self.search_video_ids(query, max_results=max_results)
		meta = self.get_videos_metadata(ids)
		# transcripts handled externally to keep single responsibility
		return meta

def fuzzy_contains(keyword: str, text: str, threshold=80):
	# threshold 0-100; higher means stricter
	return fuzz.partial_ratio(keyword.lower(), text) >= threshold

def detect_level(title, description, levels, priority, fuzzy_threshold=80):
	"""
	Detect difficulty level based on fuzzy keyword matching
	with prioritization rules.

	Parameters:
		title (str): Video title.
		description (str): Video description.
		levels (dict): Mapping of level_name -> list of keywords.
		priority (dict): Mapping of level_name -> priority score (higher = more important).
		fuzzy_threshold (int): Minimum fuzzy match (0-100) for keyword acceptance.

	Returns:
		str: Detected level name or "unknown".
	"""

	text = f"{title} {description}".lower()

	matches = []

	for lvl_name, keywords in levels.items():
		best_score = 0

		for kw in keywords:
			score = fuzz.partial_ratio(kw.lower(), text)
			if score > best_score:
				best_score = score

		if best_score >= fuzzy_threshold:
			matches.append((lvl_name, best_score))

	if not matches:
		return "unknown"

	matches.sort(
		key=lambda x: (priority.get(x[0], 0), x[1]),
		reverse=True
	)

	return matches[0][0]
