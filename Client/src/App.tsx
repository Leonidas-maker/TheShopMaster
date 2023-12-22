/// <reference types="nativewind/types" />
import 'react-native-gesture-handler';
import React from 'react';

import LoadingStack from './components/routes/loadingStack';
import { NavigationContainer } from '@react-navigation/native';

export default function App() {
  return (
    <NavigationContainer>
      <LoadingStack />
    </NavigationContainer>
  );
}
