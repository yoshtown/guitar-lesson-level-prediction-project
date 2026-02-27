# YouTube Guitar Lesson Difficulty Classifier

Automatically classifies YouTube guitar lessons as **Beginner**, **Intermediate**, or **Advanced** using NLP and machine learning.

[Live Demo - Chrome Extension](link) | [Try the API](link) | [Read Full Analysis](link-to-notebook)

## Overview
Learning guitar through YouTube is widely accessible, especially for self-taught players. However, instructional content on the platform lacks consistent difficulty labeling. As a result, learners often struggle to determine whether a lesson matches their current skill level or what the appropriate next step in their learning journey should be.

This project applies **classical supervised machine learning** to automatically classify YouTube guitar lesson videos into difficulty levels using video metadata.

---

## Problem Statement
While YouTube is a valuable resource for learning guitar, it presents several challenges:

- Difficulty levels are subjective or inconsistently labeled
- Learners may skip foundational skills or attempt advanced techniques prematurely
- Learning progression becomes unclear and inefficient
- Time is wasted navigating content that does not match current ability

The core challenge is to infer **instructional difficulty** from noisy, unstructured metadata.

---

## Data Collection
- Collected YouTube video metadata using the YouTube Data API
- Features included:
  - Video title
  - Description
  - Tags
  - Duration
  - View count and like count
  - Channel information

---

### Labeling Strategy: Programmatic Weak Supervision
Since no labeled dataset exists for guitar lesson difficulty, I developed a keyword-based labeling function using domain expertise:

- **Beginner keywords**: "beginner", "basic", "fundamental", "easy" "open chord", "sus"...
- **Intermediate keywords**: "intermediate", "barre chord"...  
- **Advanced keywords**: "advance", "fourth chord" "Drop 2 voicings"...

"Unknown" assigned to ambiguous cases.
---

### Feature Engineering
- Combined video title + description
- TF-IDF vectorization (max_features=20000, ngram_range=(1,2))

## Models Selection 
- Logistic Regression (baseline)
- Multinomial Naive Bayes
- Random Forest Classifier
- XGBoost Classifier

---

## Evaluation
Models were evaluated using:
- Accuracy
- Precision
- Confusion matrices

### Key Insights from Error Analysis
- Beginner classification: rarely misclassified
- Intermediate/Advanced boundary: Most confusion occurs here where advanced is identified as intermediate

Keyword still requires updating which will likely improve the Intermediate/Advance misclassification

## Deployment
- **Chrome Extension**: Real-time classification on YouTube
- **REST API**: Flask backend hosted on Render
- **Response time**: ~150ms average

## Tech Stack
- **ML**: scikit-learn, XGBoost, pandas, numpy, seaborn, matplotlib, tfidf
- **Deployment**: Flask, Gunicorn, Render
- **Extension**: Vanilla JavaScript, Chrome Extension API
- **Data**: YouTube Data API v3, Parquet

---

## Future Improvements
- Expand dataset size and improve class balance
- Expand keyword vocabulary
- Use topics feature to improve identification of lesson
- Upgrade retrieval of youtube description - drop details that are not the description of the video
- Badge display on search results page as well
- Badge only display only on guitar lesson vides

---