// Wait for page to load
function initClassifier() {
  // Get video title
  const titleElement = document.querySelector('h1.ytd-watch-metadata yt-formatted-string');
  
  // Get description (you may need to click "Show more" first)
  const descriptionElement = document.querySelector('#description-inline-expander yt-formatted-string');
  
  if (!titleElement) {
    console.log('Not on a video page or page not loaded');
    return;
  }
  
  const title = titleElement.textContent.trim();
  const description = descriptionElement ? descriptionElement.textContent.trim() : '';
  
  // Check if we've already added the badge
  if (document.getElementById('guitar-difficulty-badge')) {
    return;
  }
  
  // Show loading state
  createBadge('Analyzing...', 'loading');
  
  // Call API
  classifyVideo(title, description);
}

async function classifyVideo(title, description) {
  try {
    const response = await fetch('http://localhost:5000/predict', {  // Change to your deployed URL
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ title, description })
    });
    
    const data = await response.json();
    
    if (data.error) {
      updateBadge('Error', 'error');
      return;
    }
    
    const level = data.prediction;
    const confidence = (data.confidence * 100).toFixed(0);
    
    updateBadge(`${level} (${confidence}%)`, level.toLowerCase());
    
  } catch (error) {
    console.error('Classification error:', error);
    updateBadge('Error', 'error');
  }
}

function createBadge(text, className) {
  const badge = document.createElement('div');
  badge.id = 'guitar-difficulty-badge';
  badge.className = `difficulty-badge ${className}`;
  badge.textContent = text;
  
  // Insert badge near the title
  const titleElement = document.querySelector('h1.ytd-watch-metadata');
  if (titleElement) {
    titleElement.parentElement.insertBefore(badge, titleElement.nextSibling);
  }
}

function updateBadge(text, className) {
  const badge = document.getElementById('guitar-difficulty-badge');
  if (badge) {
    badge.textContent = text;
    badge.className = `difficulty-badge ${className}`;
  }
}

// Run when page loads
if (document.readyState === 'loading') {
  document.addEventListener('DOMContentLoaded', initClassifier);
} else {
  initClassifier();
}

// Re-run when navigating to new video (YouTube is a SPA)
let lastUrl = location.href;
new MutationObserver(() => {
  const url = location.href;
  if (url !== lastUrl) {
    lastUrl = url;
    setTimeout(initClassifier, 1000); // Wait for page to update
  }
}).observe(document, { subtree: true, childList: true });