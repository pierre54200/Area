import React, {useState} from "react";
import {View, Text, TextInput, Pressable} from "react-native";

export default function Login() {
  const [email,setEmail]=useState("");
  const [password,setPassword]=useState("");
  const [error,setError]=useState("");
  return <View accessibilityRole="main" style={{maxWidth:420, padding:32, margin:"auto"}}>
    <Text accessibilityRole="header" style={{fontSize:28,fontWeight:"700"}}>AREA — Sign in</Text>
    <Text>Email address</Text>
    <TextInput accessibilityLabel="Email address" autoComplete="email" keyboardType="email-address"
      value={email} onChangeText={setEmail} />
    <Text>Password</Text>
    <TextInput accessibilityLabel="Password" secureTextEntry autoComplete="password"
      value={password} onChangeText={setPassword} />
    {error ? <Text accessibilityRole="alert">{error}</Text> : null}
    <Pressable accessibilityRole="button" accessibilityLabel="Sign in"
      onPress={()=>setError("Invalid credentials (demo).")}>
      <Text>Sign in</Text>
    </Pressable>
    <Pressable accessibilityRole="link"><Text>Forgot password?</Text></Pressable>
  </View>;
}
