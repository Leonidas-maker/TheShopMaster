/// <reference types="nativewind/types" />
import 'react-native-gesture-handler';
import React from 'react';

import Navigator from './components/routes/testStack';
import { NavigationContainer } from '@react-navigation/native';

export default function App() {
  return (
    <NavigationContainer>
      <Navigator />
    </NavigationContainer>
  );
}
