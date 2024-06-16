[![License](https://img.shields.io/badge/license-MIT-blue.svg)](/LICENSE)

# Audio Transcription Service

This project is a web application that allows users to upload audio files and transcribe them using OpenAI's Whisper API. The application is built using FastAPI, and it processes large audio files by cropping them into 5-minute segments. The project uses Poetry for dependency management and Docker for containerization.

## Features

- Upload audio files for transcription.
- Validate user input with a text field.
- Split large audio files into 5-minute segments.
- Transcribe audio segments concurrently using OpenAI's Whisper API.
- Dockerized setup for easy deployment.

## Requirements

- Python 3.11
- Docker
- Docker Compose
- ffmpeg (for audio processing)

## Installation

1. **Clone the repository:**

   ```bash
   git clone https://github.com/DOUIF/audio-transcription.git
   cd audio-transcription
   ```

2. **Install Poetry:**

   ```bash
   pip install poetry
   ```

3. **Install dependencies:**

   ```bash
   poetry install
   ```

4. **Install ffmpeg:**
   - On Ubuntu:
     ```bash
     sudo apt install ffmpeg
     ```
   - On MacOS:
     ```bash
     brew install ffmpeg
     ```
   - On Windows:
     Follow the instructions on the [official FFmpeg website](https://ffmpeg.org/download.html) and add it to your PATH.

## Usage

### Running the Application Locally

1. **Set the .env file:**

   create .env file instead.

   ```txt
   OPENAI_API_KEY=sk-proj-***************************
   SECRET_KEY=**************************************
   ```

2. **Start the FastAPI server:**

   ```bash
   poetry run fastapi dev main.py --port 5001
   ```

3. **Open your browser and navigate to:**
   ```
   http://localhost:5001
   ```

### Running the Application with Docker

1. **Build the Docker image:**

   ```bash
   docker-compose build
   ```

2. **Run the Docker container:**

   ```bash
   docker-compose up
   ```

3. **Open your browser and navigate to:**
   ```
   http://localhost:5001
   ```

## Environment Variables

- `OPENAI_API_KEY`: Your OpenAI API key for accessing the Whisper API.
- `SECRET_KEY`: Your Secret key to validate user.

## API Endpoints

- **GET /**: Renders the upload form.
- **POST /upload**: Handles the file upload, processes the audio file, and returns the transcription.

## Contributing

Contributions are welcome! Please create an issue or pull request with your suggestions or improvements.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more details.
