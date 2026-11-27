import { StyleSheet } from 'react-native';

export const styles = StyleSheet.create({
  container: {
    flex: 1,
    minHeight: '100vh',
    backgroundColor: '#f4f6fa',
    paddingHorizontal: 16,
  },

  main: {
    width: '100%',
    maxWidth: 560,
    alignSelf: 'center',
    marginTop: 64,
    padding: 32,
    backgroundColor: '#ffffff',
    borderRadius: 12,
  },

  header: {
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'flex-end',
    gap: 16,
  },

  brand: {
    marginRight: 'auto',
    fontWeight: '800',
    color: '#172033',
  },

  section: {
    width: '100%',
    maxWidth: 380,
    alignSelf: 'center',
    marginTop: 48,
  },

  form: {
    gap: 10,
  },

  input: {
    fontSize: 16,
    padding: 13,
    borderWidth: 1,
    borderColor: '#687386',
    borderRadius: 6,
    backgroundColor: '#ffffff',
    color: '#172033',
  },

  button: {
    backgroundColor: '#213d73',
    padding: 13,
    borderWidth: 1,
    borderColor: '#687386',
    borderRadius: 6,
    marginVertical: 10,
    alignItems: 'center',
    justifyContent: 'center',
  },

  buttonText: {
    fontSize: 16,
    color: '#ffffff',
  },

  link: {
    color: '#174c9a',
  },

  focus: {
    borderWidth: 3,
    borderColor: '#e08b00',
  },

  title: {
    fontSize: 28,
    fontWeight: '700',
    color: '#172033',
    marginBottom: 24,
  },

  label: {
    fontSize: 16,
    color: '#172033',
  },

  error: {
    color: '#b42318',
    fontSize: 14,
  },
});
