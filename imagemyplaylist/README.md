# Spotify Playlist Viewer and Image Editor

A web application to view and customize Spotify playlists. Users can authenticate with their Spotify account, view their playlists, and easily update playlist images by searching for relevant images online based on playlist content.

## Features

- **User Authentication**: Secure login using Spotify's OAuth via NextAuth.
- **Playlist Viewing**: Retrieve and display user playlists from Spotify, showing playlist images, names, and song counts.
- **Image Search and Update**: Allows users to search for new images based on playlist content and update playlist images directly.
- **Responsive Design**: Optimized layout for both desktop and mobile devices.

## Technologies Used

- **Next.js**: Framework for server-rendered React applications.
- **TypeScript**: For type safety and improved development experience.
- **NextAuth**: Authentication library, configured with Spotify as a provider.
- **Tailwind CSS**: For responsive styling.
- **Image Search API**: To implement...

## Setup and Installation

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/your-username/spotify-playlist-viewer.git
   cd spotify-playlist-viewer

2. **Install dependencies**:
`npm install`

3. **Environment Variables: Create a .env.local file in the root directory with the following variables**:

```
SPOTIFY_CLIENT_ID=your_spotify_client_id
SPOTIFY_CLIENT_SECRET=your_spotify_client_secret
NEXTAUTH_SECRET=your_nextauth_secret
NEXTAUTH_URL=http://localhost:3000
IMAGE_SEARCH_API_KEY=your_image_search_api_key

```
 - Replace your_spotify_client_id and your_spotify_client_secret with your Spotify API credentials.
 - Replace your_nextauth_secret with a random secret string for NextAuth.


4. **Run the development server**:
`npm run dev`
