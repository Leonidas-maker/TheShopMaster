import { createStackNavigator } from '@react-navigation/stack';
import { StatusBar } from 'react-native';
import Login from '../../screens/login/login';
import Registration from '../../screens/registration/registration';

const Stack = createStackNavigator();

function CredentialStack() {
  return (
    <>
      <StatusBar barStyle="light-content" />
      <Stack.Navigator
        screenOptions={{
          headerShown: false,
          cardStyle: { backgroundColor: '#232D3F' }
        }}
      >
        <Stack.Screen name="Login" component={Login} />
        <Stack.Screen name="Registration" component={Registration} />
      </Stack.Navigator>
    </>
  );
}

export default CredentialStack;
