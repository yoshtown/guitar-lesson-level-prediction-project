console.log('🎸 Extension loaded!');

// Main classifier function
function initClassifier() {
  console.log('🎸 initClassifier called');
  console.log('🎸 Current URL:', location.href);
  
  // IMPORTANT: Remove old badge first
  const oldBadge = document.getElementById('guitar-difficulty-badge');
  console.log('🎸 Old badge exists?', !!oldBadge);
  
  if (oldBadge) {
    oldBadge.remove();
    console.log('🎸 Old badge removed');
  }
  
  // Get video title
  const titleElement = document.querySelector('h1.ytd-watch-metadata yt-formatted-string');
  console.log('🎸 Title element found?', !!titleElement);
  
  if (!titleElement) {
    console.log('🎸 Not on a video page or page not loaded - waiting...');
    return;
  }
  
  const title = titleElement.textContent.trim();
  console.log('🎸 Video title:', title);
  
  // Get description
  const descriptionElement = document.querySelector('#description-inline-expander yt-formatted-string');
  const description = descriptionElement ? descriptionElement.textContent.trim() : '';
  console.log('🎸 Description length:', description.length);
  
  // Show loading state
  createBadge('Analyzing...', 'loading', titleElement);
  console.log('🎸 Loading badge created');
  
  // Call API
  classifyVideo(title, description, titleElement);
}

async function fetchWithRetry(url, options={}, retries=3, baseDelay=1500) {
  for (let attempt=0; attempt <= retries; attempt++) {
    const controller = new AbortController();
    const timeout = setTimeout(() => controller.abort(), 25000)

    try {
      const response = await fetch(url, {
        ...options,
        signal: controller.signal
      });

      clearTimeout(timeout);

      if (!response.ok){
        throw new Error('HTTP ${response.status}');
      }

      return response;
    } catch (err){
      clearTimeout(timeout);

      if (attempt === retries){
        throw err;
      }

      const delay = baseDelay * Math.pow(2, attempt);
      console.log('  Retry attempt ${attempt + 1}  in ${delay}ms');
      await new Promise(res => setTimeout(res, delay));
    }
  }
}

async function classifyVideo(title, description, titleElement) {
  console.log('🎸 Calling API...');
  
  try {
    updateBadge('reloading', 'loading')

    const response = await fetchWithRetry('https://guitar-lesson-classifier-api.onrender.com/predict', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ title, description })
    });
    
    console.log('🎸 API response status:', response.status);
    
    const data = await response.json();
    console.log('🎸 API response data:', data);
    
    if (data.error) {
      console.log('🎸 API returned error:', data.error);
      updateBadge('Error', 'error');
      return;
    }
    
    const level = data.prediction;
    const confidence = (data.confidence * 100).toFixed(0);
    
    console.log('🎸 Prediction:', level, 'Confidence:', confidence + '%');
    
    updateBadge(`${level} (${confidence}%)`, level.toLowerCase());
    
  } catch (error) {
    console.error('🎸 Classification error:', error);
    updateBadge('Server Unavailable', 'error');
  }
}

function createBadge(text, className, titleElement) {
  const badge = document.createElement('div');
  badge.id = 'guitar-difficulty-badge';
  badge.className = `difficulty-badge ${className}`;
  badge.textContent = text;
  
  // Add inline spacing to separate from title
  badge.style.marginLeft = '16px';
  badge.style.display = 'inline-block';
  badge.style.verticalAlign = 'middle';
  
  // Insert after title
  titleElement.parentElement.insertBefore(badge, titleElement.nextSibling);
}

function updateBadge(text, className) {
  const badge = document.getElementById('guitar-difficulty-badge');
  if (badge) {
    badge.textContent = text;
    badge.className = `difficulty-badge ${className}`;
    console.log('🎸 Badge updated to:', text);
  } else {
    console.log('🎸 Warning: Could not find badge to update');
  }
}

// // Run when page loads
// if (document.readyState === 'loading') {
//   document.addEventListener('DOMContentLoaded', initClassifier);
// } else {
//   initClassifier();
// }

// Run classifier on YouTube internal navigation events
window.addEventListener('yt-navigate-finish', () => {
  setTimeout(initClassifier, 1500)
});

// Re-run when navigating to new video (YouTube is a SPA)
let lastUrl = location.href;
new MutationObserver(() => {
  const url = location.href;
  if (url !== lastUrl) {
    lastUrl = url;
    console.log('🎸 URL changed to:', url);
    setTimeout(initClassifier, 1500); // Wait for YouTube to update DOM
  }
}).observe(document, { subtree: true, childList: true });