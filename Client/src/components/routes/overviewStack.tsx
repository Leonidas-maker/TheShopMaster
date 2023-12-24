import { createStackNavigator } from '@react-navigation/stack';
import { StatusBar } from 'react-native';
import Dashboard from '../../screens/dashboard/dashboard';
import Loading from '../../screens/loading/loading';
import Login from '../../screens/login/login';
import Registration from '../../screens/registration/registration';
import Settings from '../../screens/settings/settings';
import ShoppingList from '../../screens/shoppingList/shoppingList';
import Overview from '../../screens/overview/overview';

const Stack = createStackNavigator();

function OverviewStack() {
    return (
        <>
            <StatusBar barStyle="light-content" />
            <Stack.Navigator initialRouteName="Overview">
                <Stack.Screen 
                    name="Overview" 
                    component={Overview} 
                    options={{ headerShown: false }} 
                />
                <Stack.Screen name="Dashboard" component={Dashboard} />
                <Stack.Screen name="Loading" component={Loading} />
                <Stack.Screen name="Login" component={Login} />
                <Stack.Screen name="Registration" component={Registration} />
                <Stack.Screen name="Settings" component={Settings} />
                <Stack.Screen name="ShoppingList" component={ShoppingList} />
            </Stack.Navigator>
        </>
    );
}

export default OverviewStack;
