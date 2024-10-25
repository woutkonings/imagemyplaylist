// app/page.tsx
import { auth } from "@/auth"
import SignIn from "@/components/sign-in"
import SignOut from "@/components/sign-out"
import Link from "next/link"
import { GetServerSideProps } from "next"

export default async function Home() {
  const session = await auth()

  return (
    <div className="flex items-center justify-center min-h-screen bg-gray-900 text-white">
      {!session ? (
        <SignIn />
      ) : (
        <div>
          <p>Welcome, {session.user?.name}</p>
          <Link href="/playlists" className="px-4 py-2 mt-4 font-bold text-white bg-blue-500 rounded">
            View My Playlists
          </Link>
          <SignOut />
        </div>
      )}
    </div>
  )
}
