import { createStackNavigator } from '@react-navigation/stack';
import Loading from '../../screens/loading/loading';
import HomeBottomTabs from './homeBottomTabs';
import { StatusBar } from 'react-native';
import OverviewStack from './overviewStack';

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
        <Stack.Screen name="OverviewStack" component={OverviewStack} />
      </Stack.Navigator>
    </>
  );
}

export default LoadingStack;
