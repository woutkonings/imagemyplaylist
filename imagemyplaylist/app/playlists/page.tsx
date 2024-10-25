// app/playlists/page.tsx
import { auth } from "@/auth"
import PlaylistsClient from "@/components/playlist-client"
import { Playlist, Session } from "@/lib/types" // define Playlist type if needed
import axios from "axios"

export default async function PlaylistsPage() {
  const session = (await auth()) as Session // fetch session server-side

  console.log(session)

  if (!session || !session.token.access_token) {
    return <p>Please sign in to view your playlists.</p>
  }

  // Fetch playlists server-side
  const res = await axios.get(`https://api.spotify.com/v1/me/playlists`, {
    headers: {
      Authorization: `Bearer ${session.token.access_token}`,
    },
  })
  console.log(res.data)
  const playlists: Playlist[] = res.data.items

  return <PlaylistsClient playlists={playlists} />
}
