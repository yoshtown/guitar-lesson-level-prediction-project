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
from src.text_classifiers import classify_text

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

		for i in range(0, len(video_ids), BATCH):
			batch = video_ids[i:i+BATCH]
			resp = self.youtube.videos().list(
					part="snippet,statistics,contentDetails",
					id=",".join(batch)
				).execute()

			items = resp.get("items", [])
			logger.info("Recieved %d items in metadata batch %d", len(items), i // BATCH + 1)

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

				classification = classify_text(title, description)

				level = classification["level"]
				topic = classification["topic"]

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
