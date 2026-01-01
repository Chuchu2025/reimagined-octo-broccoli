# 🥦 Reimagined Octo Broccoli

A clean and simple starter project template for web development with Node.js.

## What is this?

This is a **good starting project** that provides a solid foundation for building web applications. It includes:

- ✅ Simple Node.js HTTP server
- ✅ Clean project structure with separation of concerns
- ✅ Built-in testing with Node.js test runner
- ✅ Responsive HTML/CSS template
- ✅ API endpoint examples
- ✅ Modern development workflow

## Quick Start

### Prerequisites

- Node.js 18.0.0 or higher

### Installation

1. Clone this repository:
```bash
git clone https://github.com/Chuchu2025/reimagined-octo-broccoli.git
cd reimagined-octo-broccoli
```

2. Start the server:
```bash
npm start
```

3. Open your browser and navigate to `http://localhost:3000`

## Available Scripts

- **`npm start`** - Start the production server
- **`npm test`** - Run all tests
- **`npm run dev`** - Start the development server with auto-reload (Node.js 18+)

## Project Structure

```
reimagined-octo-broccoli/
├── src/
│   ├── index.js         # Main server file with HTTP server and API
│   └── index.test.js    # Unit tests
├── public/
│   ├── index.html       # Main HTML page
│   └── styles.css       # Stylesheet
├── package.json         # Project dependencies and scripts
├── .gitignore          # Git ignore rules
└── README.md           # This file
```

## Features

### HTTP Server
A simple HTTP server built with Node.js core modules that serves static files and API endpoints.

### API Endpoints
- `GET /` - Serves the main HTML page
- `GET /api/greet` - Returns a JSON greeting message
- `GET /styles.css` - Serves the stylesheet

### Testing
Uses Node.js built-in test runner (available in Node.js 18+). Tests are located alongside source files with `.test.js` extension.

### Responsive Design
The included HTML template is responsive and works well on desktop and mobile devices.

## Development

### Adding New Features

1. Add your server-side code in the `src/` directory
2. Add corresponding tests in `src/*.test.js` files
3. Add static assets (HTML, CSS, images) in the `public/` directory
4. Run tests with `npm test` to verify everything works

### Customization

- **Port**: Set the `PORT` environment variable (default: 3000)
- **Server logic**: Edit `src/index.js`
- **UI/Styling**: Edit files in the `public/` directory

## Why This Starter?

This project is designed to be:

- **Simple**: Uses only Node.js core modules, no external dependencies
- **Educational**: Clear code structure that's easy to understand
- **Practical**: Includes real-world features like routing, API endpoints, and testing
- **Extensible**: Easy to build upon and customize for your needs

## Next Steps

From here, you can:

1. Add a database (e.g., SQLite, MongoDB)
2. Implement user authentication
3. Add more API endpoints
4. Integrate a frontend framework (React, Vue, etc.)
5. Add a build system (Webpack, Vite, etc.)
6. Deploy to a cloud service (Heroku, Vercel, Railway, etc.)

## License

MIT

## Contributing

Feel free to fork this project and customize it for your needs!
