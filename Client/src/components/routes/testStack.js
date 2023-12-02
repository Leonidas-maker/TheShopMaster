import { createStackNavigator } from '@react-navigation/stack';
import Loading from '../../pages/loading/loading';
import Registration from '../../pages/registration/registration';
import Login from '../../pages/login/login';
import Dashboard from '../../pages/dashboard/dashboard';

const Stack = createStackNavigator();

function Navigator() {
  return (
    <Stack.Navigator>
        <Stack.Screen name="Loading" component={Loading} />
        <Stack.Screen name="Registration" component={Registration} />
        <Stack.Screen name="Login" component={Login} />
        <Stack.Screen name="Dashboard" component={Dashboard} />
    </Stack.Navigator>
  );
}

export default Navigator;