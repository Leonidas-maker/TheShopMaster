import { createStackNavigator } from '@react-navigation/stack';
import Loading from '../../pages/loading/loading';
import HomeBottomTabs from './homeBottomTabs';
import { StatusBar } from 'react-native';

const Stack = createStackNavigator();

function LoadingStack() {
  return (
    <>
      <StatusBar barStyle="light-content" />
      <Stack.Navigator
        screenOptions={{
          headerShown: false,
          cardStyle: { backgroundColor: '#232D3F' }
        }}
      >
        <Stack.Screen name="Loading" component={Loading} />
        <Stack.Screen name="HomeBottomTabs" component={HomeBottomTabs} />
      </Stack.Navigator>
    </>
  );
}

export default LoadingStack;
