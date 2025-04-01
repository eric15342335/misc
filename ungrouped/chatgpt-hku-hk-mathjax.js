// Create and load MathJax
var script = document.createElement('script');
script.src = 'https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-mml-chtml.js';

// Configure MathJax with all needed delimiters
window.MathJax = {
  tex: {
    inlineMath: [['$', '$'], ['\\(', '\\)']],
    displayMath: [['$$', '$$'], ['\\[', '\\]'], ['[', ']']]
  },
  startup: {
    typeset: false // Disable initial typeset to reduce lag
  }
};

// Add script to document
document.head.appendChild(script);

// Set up observer to detect new messages
script.onload = function() {
  // Initial typeset
  MathJax.typeset();
  
  // Debounce function to limit typeset calls
  let timeoutId = null;
  const debounceTypeset = function() {
    if (timeoutId) {
      clearTimeout(timeoutId);
    }
    timeoutId = setTimeout(function() {
      MathJax.typeset();
      timeoutId = null;
    }, 1000); // Wait ?ms before processing to batch changes
  };
  
  // Create observer for new content
  new MutationObserver(function(mutations) {
    let hasNewNodes = false;
    
    // Check if any of the mutations contain new nodes
    for (let i = 0; i < mutations.length; i++) {
      if (mutations[i].addedNodes.length > 0) {
        hasNewNodes = true;
        break;
      }
    }
    
    if (hasNewNodes) {
      // Use debounced typeset
      debounceTypeset();
    }
  }).observe(document.body, {
    childList: true,
    subtree: true,
    characterData: false
  });
};