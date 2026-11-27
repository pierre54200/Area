import React from 'react';
import ReactDOM from 'react-dom/client';
import { AppRegistry } from 'react-native';
import Login from './Login';

AppRegistry.registerComponent('AreaApp', () => Login);

AppRegistry.runApplication('AreaApp', {
  rootTag: document.getElementById('root'),
});
