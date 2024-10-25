
import NextAuth from "next-auth"
import Spotify from "next-auth/providers/spotify"
 
export const { handlers, signIn, signOut, auth } = NextAuth({
  providers: [Spotify],
  callbacks: {
    async jwt({ token, account }) {
        if(account){
            token.access_token = account.access_token;
        }
        return token;
    },
      async session({ session, token }) {
          return {
              ...session,
              token
          };
      },
  }
})
