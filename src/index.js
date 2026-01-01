const http = require('http');
const fs = require('fs');
const path = require('path');

const PORT = process.env.PORT || 3000;

// Simple utility function for demonstration
function greet(name = 'World') {
  return `Hello, ${name}!`;
}

// HTTP server
const server = http.createServer((req, res) => {
  if (req.url === '/' || req.url === '/index.html') {
    // Serve the HTML file
    fs.readFile(path.join(__dirname, '../public/index.html'), (err, data) => {
      if (err) {
        res.writeHead(500, { 'Content-Type': 'text/plain' });
        res.end('Internal Server Error');
        return;
      }
      res.writeHead(200, { 'Content-Type': 'text/html' });
      res.end(data);
    });
  } else if (req.url === '/api/greet') {
    // API endpoint
    const message = greet('Developer');
    res.writeHead(200, { 'Content-Type': 'application/json' });
    res.end(JSON.stringify({ message }));
  } else if (req.url === '/styles.css') {
    // Serve CSS file
    fs.readFile(path.join(__dirname, '../public/styles.css'), (err, data) => {
      if (err) {
        res.writeHead(404, { 'Content-Type': 'text/plain' });
        res.end('Not Found');
        return;
      }
      res.writeHead(200, { 'Content-Type': 'text/css' });
      res.end(data);
    });
  } else {
    res.writeHead(404, { 'Content-Type': 'text/plain' });
    res.end('Not Found');
  }
});

// Start server only if this file is run directly
if (require.main === module) {
  server.listen(PORT, () => {
    console.log(`Server running at http://localhost:${PORT}/`);
    console.log('Press Ctrl+C to stop the server');
  });
}

// Export for testing
module.exports = { greet, server };
