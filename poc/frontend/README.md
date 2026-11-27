# Front-end POCs

Tous les écrans utilisent le même cas de test : formulaire de connexion e-mail/mot de passe,
lien de récupération, choix de langue EN/FR et message d'erreur accessible.

## A1 — React DOM
`react-dom/` : HTML sémantique, labels explicites, `main`, `form`, `autocomplete` et annonce d'erreur.
À lancer avec Vite/React en installant les dépendances du `package.json`.

## B1 — React Native Web
`rn-web/` : même formulaire avec `View`, `TextInput`, `Pressable` et propriétés d'accessibilité.
Comparer l'arbre rendu et le score axe/Lighthouse avec A1 à viewport identique.

## A2 — React Native Expo
`expo/` : écran mobile minimal ; `npx expo run:android` nécessite Android SDK.

## B2 — Mini builder
`builder/` : exemple web-only React Flow (`.web.tsx`), séparé de l'interface native.

## C1 — Angular + Ionic / D1 — Flutter
Squelettes de comparaison et critères d'exécution dans `ionic/` et `flutter/`.
