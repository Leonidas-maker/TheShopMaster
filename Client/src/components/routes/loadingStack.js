import { createStackNavigator } from '@react-navigation/stack';
import Loading from '../../screens/loading/loading';
import HomeBottomTabs from './homeBottomTabs';
import ShoppingList from '../../screens/shoppingList/shoppingList';
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
        <Stack.Screen name="ShoppingList" component={ShoppingList} />
      </Stack.Navigator>
    </>
  );
}

export default LoadingStack;
