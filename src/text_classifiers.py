from rapidfuzz import fuzz

# ------------------------------------
# Keyword Dictionaries
# ------------------------------------

levels = {
	"beginner": ["beginner", "basic", "fundamental", "easy" "open chord", "sus"],
	"intermediate": ["intermediate", "bar chord", 
				"7th", "seventh", "add9",
				"beautiful chord", "add6/9"],
	"advance": ["advance", "4th chord", "fourth chord" "Drop 2 voicings", "4th", "fourth"]
}

topics = {
	"Chords": ["chord", "bar", "7th", "seventh", "open chord"],
	"Scales": ["scale", "pentatonic"],
	"Technique": ["pick", "strumming", "alternate picking"],
	"Arpeggios": ["arp", "arpeggio"],
	"Learning songs": ["song", "play", "cover", ],
	"Improvisation": ["improv", "improvisation", "solo", "phrasing"],
	"Other Topics": []
}

priority = {
	"advanced": 3,
	"intermediate": 2,
	"beginner": 1
}

# ------------------------------------
# Helper Functions
# ------------------------------------

def fuzzy_score(keyword, text):
	return fuzz.partial_ratio(keyword.lower(), text.lower())

# ------------------------------------
# Level Detection
# ------------------------------------

def detect_level(title, description, fuzzy_threshold=80):
	"""
	Detect difficulty level based on fuzzy keyword matching
	with prioritization rules.

	Parameters:
		title (str): Video title.
		description (str): Video description.
		fuzzy_threshold (int): Minimum fuzzy match (0-100) for keyword acceptance.

	Returns:
		str: Detected level name or "unknown".
	"""

	text = f"{title} {description}".lower()

	matches = []

	for lvl_name, keywords in levels.items():
		best_score = 0

		for kw in keywords:
			score = fuzzy_score(kw, text)
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

# ------------------------------------
# Topic Detection
# ------------------------------------

def detect_topic(title, description, fuzzy_threshold=70):
	"""
	Detect main topic based on fuzzy keyword matching

	Parameters:
		title (str): Video title.
		description (str): Video description.
		fuzzy_threshold (int): Minimum fuzzy match (0-100) for keyword acceptance.

	Returns:
		str: Best topic name or "Other Topics".
	"""

	text = f"{title} {description}".lower()

	best_topic = None
	best_score = 0

	for topic, keywords in topics.items():
		for kw in keywords:
			score = fuzzy_score(kw, text)
			if score > best_score:
				best_score = score
				best_topic = topic

	if best_score < fuzzy_threshold:
		return "Other Topics"


	return best_topic

# ------------------------------------
# Unified Classification API
# ------------------------------------

def classify_text(title, description):
	"""
	Returns a dictionary with:
		- level (beginner, intermediate, advanced, unknown)
		- topic (e.g., Chords, Scales, Technique...)
	"""

	return{
		"level": detect_level(title, description),
		"topic": detect_topic(title, description)
	}
