// components/sign-in.tsx
import { signIn } from "@/auth"

export default function SignIn() {
  return (
    <form
      action={async () => {
        "use server"
        await signIn("spotify")
      }}
    >
      <button
        type="submit"
        className="px-4 py-2 font-bold text-white bg-green-500 rounded"
      >
        Sign in with Spotify
      </button>
    </form>
  )
}
