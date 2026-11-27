import React, { useState } from "react";
import { createRoot } from "react-dom/client";
import "./style.css";

function Login() {
  const [language, setLanguage] = useState("en");
  const [error, setError] = useState("");
  const fr = language === "fr";
  function submit(event) {
    event.preventDefault();
    setError(fr ? "Identifiants invalides (démonstration)." : "Invalid credentials (demo).");
  }
  return <main>
    <header><p className="brand">AREA</p><label htmlFor="language">{fr ? "Langue" : "Language"}</label>
      <select id="language" value={language} onChange={e => setLanguage(e.target.value)}>
        <option value="en">English</option><option value="fr">Français</option>
      </select>
    </header>
    <section aria-labelledby="title">
      <h1 id="title">{fr ? "Connexion" : "Sign in"}</h1>
      <p>{fr ? "Connectez-vous pour gérer vos automatisations." : "Sign in to manage your workflows."}</p>
      <form onSubmit={submit}>
        <label htmlFor="email">{fr ? "Adresse e-mail" : "Email address"}</label>
        <input id="email" name="email" type="email" autoComplete="username" required />
        <label htmlFor="password">{fr ? "Mot de passe" : "Password"}</label>
        <input id="password" name="password" type="password" autoComplete="current-password" required />
        {error && <p role="alert">{error}</p>}
        <button type="submit">{fr ? "Se connecter" : "Sign in"}</button>
      </form>
      <a href="#forgot">{fr ? "Mot de passe oublié ?" : "Forgot password?"}</a>
    </section>
  </main>;
}
createRoot(document.getElementById("root")).render(<Login />);
