# Audio Mashup Project

## Overview

This project is a web application that allows users to create audio mashups by combining audio from multiple YouTube videos of a given singer. Users can specify the singer's name, the number of videos to include, and the duration of each audio clip. The final mashup is then generated and sent to the user's email as a zip file.

## Features

- **User Input Form:**

  - Enter the singer's name.
  - Specify the number of videos to include in the mashup.
  - Set the duration (in seconds) for each audio clip.
  - Provide an email address to receive the final mashup.

- **YouTube Integration:**

  - Retrieve YouTube video IDs based on the singer's name.
  - Download audio streams from randomly selected videos.

- **Audio Processing:**

  - Combine audio clips to create a final mashup.
  - Allow users to customize the duration of each audio clip.

- **Email Notification:**
  - Send the final mashup as a zip file to the user's email.

## Technologies Used

- Django
- PyTube
- PyDub
- Google API Client

# Contributors

- [Nikhil Chadha](https://github.com/nikhil697)
