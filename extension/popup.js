// popup.js
document.addEventListener('DOMContentLoaded', function() {
  // Get current tab
  chrome.tabs.query({active: true, currentWindow: true}, function(tabs) {
    const currentTab = tabs[0];
    
    // Check if we're on YouTube
    if (currentTab.url && currentTab.url.includes('youtube.com/watch')) {
      document.getElementById('status').textContent = '✓ Active on this page';
      document.getElementById('status').style.color = '#4CAF50';
    } else {
      document.getElementById('status').textContent = 'Open a YouTube video to use this extension';
      document.getElementById('status').style.color = '#666';
    }
  });
  
  // Add click handler for settings (optional)
  const settingsBtn = document.getElementById('settings-btn');
  if (settingsBtn) {
    settingsBtn.addEventListener('click', function() {
      // Could open options page or do something else
      alert('Settings coming soon!');
    });
  }
});