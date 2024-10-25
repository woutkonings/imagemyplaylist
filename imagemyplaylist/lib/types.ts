export interface Session {
    user: {
      name: string
      email: string
      image: string
    }
    token: {
      access_token: string
    }
    expires ?: string
  }


  export type Playlist = {
    id: string
    name: string
    images: { url: string }[]
    tracks: { total: number }
  }