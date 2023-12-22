import { createStackNavigator } from '@react-navigation/stack';
import Loading from '../../pages/loading/loading';
import HomeBottomTabs from './homeBottomTabs';

const Stack = createStackNavigator();

function LoadingStack() {
  return (
    <Stack.Navigator screenOptions={{ headerShown: false }}>
        <Stack.Screen name="Loading" component={Loading} />
        <Stack.Screen name="HomeBottomTabs" component={HomeBottomTabs} />
    </Stack.Navigator>
  );
}

export default LoadingStack;