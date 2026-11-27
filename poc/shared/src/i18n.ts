export const messages = {
  en: { signIn: "Sign in", email: "Email address", password: "Password" },
  fr: { signIn: "Se connecter", email: "Adresse e-mail", password: "Mot de passe" },
} as const;
export type Locale = keyof typeof messages;
