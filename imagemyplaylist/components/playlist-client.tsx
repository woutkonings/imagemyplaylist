"use client"
import { Playlist } from "@/lib/types"

type PlaylistsClientProps = {
  playlists: Playlist[]
}

export default function PlaylistsClient({ playlists }: PlaylistsClientProps) {
  return (
    <div className="min-h-screen bg-gray-900 text-white p-4">
      <h1 className="text-3xl font-bold mb-4">Your Spotify Playlists</h1>
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
        {playlists.map((playlist) => (
          <div key={playlist.id} className="p-4 bg-gray-800 rounded">
            {/* Check if images array exists and has at least one item */}
            {playlist.images && playlist.images.length > 0 ? (
              <img
                src={playlist.images[0].url}
                alt={playlist.name}
                className="w-full h-40 object-cover rounded"
              />
            ) : (
              <div className="w-full h-40 bg-gray-700 rounded flex items-center justify-center">
                <span className="text-gray-400">No Image</span>
              </div>
            )}
            <h2 className="text-xl font-bold mt-2">{playlist.name}</h2>
            {/* Safely access the tracks total */}
            <p>{playlist.tracks?.total ?? 0} songs</p>
          </div>
        ))}
      </div>
    </div>
  )
}
