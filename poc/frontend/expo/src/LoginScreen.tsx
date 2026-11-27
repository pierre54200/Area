import React, {useState} from "react";
import {View, Text, TextInput, Pressable} from "react-native";
export default function LoginScreen() {
 const [email,setEmail]=useState(""); const [password,setPassword]=useState("");
 return <View style={{padding:24,gap:12}}>
  <Text accessibilityRole="header">AREA — Sign in</Text>
  <Text>Email address</Text><TextInput accessibilityLabel="Email address" value={email} onChangeText={setEmail} autoCapitalize="none" keyboardType="email-address"/>
  <Text>Password</Text><TextInput accessibilityLabel="Password" value={password} onChangeText={setPassword} secureTextEntry/>
  <Pressable accessibilityRole="button" onPress={()=>{}}><Text>Sign in</Text></Pressable>
 </View>;
}
