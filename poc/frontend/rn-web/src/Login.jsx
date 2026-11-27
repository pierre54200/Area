import React, { useState } from 'react';
import {
  View,
  Text,
  TextInput,
  Pressable,
} from 'react-native';
import { styles } from './styles';

export default function Login() {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');

  return (
    <View accessibilityRole="main" style={styles.container}>
      <View style={styles.main}>
        <View style={styles.header}>
          <Text style={styles.brand}>AREA</Text>
        </View>

        <View style={styles.section}>
          <Text accessibilityRole="header" style={styles.title}>
            AREA — Sign in
          </Text>

          <View style={styles.form}>
            <Text style={styles.label}>Email address</Text>
            <TextInput
              accessibilityLabel="Email address"
              autoComplete="email"
              keyboardType="email-address"
              autoCapitalize="none"
              value={email}
              onChangeText={setEmail}
              style={styles.input}
            />

            <Text style={styles.label}>Password</Text>
            <TextInput
              accessibilityLabel="Password"
              secureTextEntry
              autoComplete="password"
              value={password}
              onChangeText={setPassword}
              style={styles.input}
            />

            {error ? (
              <Text accessibilityRole="alert" style={styles.error}>
                {error}
              </Text>
            ) : null}

            <Pressable
              accessibilityRole="button"
              accessibilityLabel="Sign in"
              onPress={() => setError('Invalid credentials (demo).')}
              style={styles.button}
            >
              <Text style={styles.buttonText}>Sign in</Text>
            </Pressable>

            <Pressable accessibilityRole="link">
              <Text style={styles.link}>Forgot password?</Text>
            </Pressable>
          </View>
        </View>
      </View>
    </View>
  );
}

