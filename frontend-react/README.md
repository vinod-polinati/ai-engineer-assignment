# Excel Interview React Frontend

A minimal, modern React frontend for the Excel Mock Interview application.

## Features

- Clean, modern chat interface
- Real-time conversation with AI interviewer
- Typing indicators
- Auto-scroll to latest messages
- Restart interview functionality
- Responsive design
- TypeScript support

## Setup

1. Make sure your FastAPI backend is running on `http://localhost:8000`

2. Install dependencies:
   ```bash
   npm install
   ```

3. Start the development server:
   ```bash
   npm start
   ```

4. Open [http://localhost:3000](http://localhost:3000) to view it in the browser.

## Usage

1. The app will automatically connect to your FastAPI backend
2. Type your responses in the input field and press Enter or click Send
3. The AI interviewer will guide you through the Excel interview process
4. Use the "Restart Interview" button to start a new session

## Development

- Built with React 18 and TypeScript
- Uses Axios for API communication
- Styled with CSS (no external UI libraries)
- Proxy configuration handles CORS automatically

## Available Scripts

- `npm start` - Runs the app in development mode
- `npm run build` - Builds the app for production
- `npm test` - Launches the test runner
- `npm run eject` - Ejects from Create React App (one-way operation)
