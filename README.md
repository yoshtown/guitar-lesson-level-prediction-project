# YouTube Guitar Lesson Difficulty Classifier

Classical machine learning system for classifying YouTube guitar lesson videos into **Beginner**, **Intermediate**, and **Advanced** levels using NLP and structured metadata.

![Python](https://img.shields.io/badge/Python-3.10-blue)
![scikit-learn](https://img.shields.io/badge/scikit--learn-ML-orange)
![NLP](https://img.shields.io/badge/NLP-TF--IDF-green)
![ML Type](https://img.shields.io/badge/ML-Supervised%20Classification-purple)
![Status](https://img.shields.io/badge/Status-Completed-success)
![License](https://img.shields.io/badge/License-MIT-lightgrey)

> This project intentionally uses classical machine learning methods to emphasize interpretability, feature engineering, and real-world data challenges.

---

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

## Labeling Strategy
- Manually labeled a seed dataset into three classes:
  - Beginner
  - Intermediate
  - Advanced
- Labels were informed by:
  - Instructional language
  - Technique complexity
  - Assumed prerequisite knowledge

This reflects real-world conditions where class boundaries are subjective and imperfect.

---

## Feature Engineering
### Text Features
- TF-IDF vectorization applied to:
  - Titles
  - Descriptions
  - Tags
- N-gram modeling used to capture multi-word techniques and learning cues

### Numerical Features
- Video duration
- Engagement metrics (normalized)

---

## Models Evaluated
- Multinomial Naive Bayes (baseline)
- Logistic Regression
- Random Forest Classifier

All models were implemented using scikit-learn with stratified train-test splits.

---

## Evaluation
Models were evaluated using:
- Accuracy
- Precision and recall per class
- Confusion matrices

### Key Findings
- Beginner content was the most consistently classified due to distinct instructional language
- Most misclassifications occurred between Intermediate and Advanced lessons
- Feature inspection showed strong alignment between domain-specific vocabulary and model predictions

These results highlight both model behavior and inherent ambiguity in difficulty labeling.

---

## Key Machine Learning Takeaways
This project reinforced that model performance alone is not sufficient when working with real-world data. Label ambiguity, overlapping class definitions, and feature selection significantly influence outcomes. Classical models paired with strong feature engineering and interpretability tools can surface meaningful insights in subjective classification tasks.

---

## Impact
This system demonstrates how classical machine learning can:
- Improve content discovery for self-directed learners
- Reduce ambiguity in educational progression
- Provide interpretable insights without black-box models

---

## Tech Stack
- Python
- scikit-learn
- pandas
- NumPy
- YouTube Data API

---

## Future Improvements
- Expand dataset size and improve class balance
- Incorporate linguistic complexity metrics
- Add channel-level priors
- Explore hierarchical classification (Beginner → Intermediate → Advanced)

---

## License
MIT License


