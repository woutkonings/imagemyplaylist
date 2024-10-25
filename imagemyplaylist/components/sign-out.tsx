// components/sign-out.tsx
import { signOut } from "@/auth"
import React from "react"

export default function SignOut() {
  return (
    <form
      action={async () => {
        "use server"
        await signOut()
      }}
    >
      <button type="submit" className="px-4 py-2 text-white bg-red-500 rounded">
        Sign Out
      </button>
    </form>
  )
}
