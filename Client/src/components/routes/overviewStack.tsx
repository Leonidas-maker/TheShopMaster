import { createStackNavigator } from '@react-navigation/stack';
import { StatusBar } from 'react-native';
import Dashboard from '../../screens/dashboard/dashboard';
import Loading from '../../screens/loading/loading';
import Login from '../../screens/login/login';
import Registration from '../../screens/registration/registration';
import Settings from '../../screens/settings/settings';
import ShoppingList from '../../screens/shoppingList/shoppingList';
import Overview from '../../screens/overview/overview';
import Report from '../../screens/report/report';
import ProductInfo from '../../screens/productInfo/productInfo';
import Imprint from '../../screens/imprint/imprint';
import Credits from '../../screens/credits/credits';
import Debug from '../../screens/devScreens/debug/debug';
import MFA from '../../screens/mfa/mfa';
import Request from '../../screens/request/request';
import About from '../../screens/about/about';

const Stack = createStackNavigator();

function OverviewStack() {
    return (
        <>
            <StatusBar barStyle="light-content" />
            <Stack.Navigator initialRouteName="Overview"
            screenOptions={{
                headerStyle: {
                    backgroundColor: '#171717'
                },
                headerTintColor: '#E0E0E2'
            }} >
                <Stack.Screen
                    name="Overview"
                    component={Overview}
                    options={{ headerShown: true }}
                />
                <Stack.Screen name="Dashboard" component={Dashboard} />
                <Stack.Screen name="Loading" component={Loading} />
                <Stack.Screen name="Login" component={Login} />
                <Stack.Screen name="Registration" component={Registration} />
                <Stack.Screen name="Settings" component={Settings} />
                <Stack.Screen name="ShoppingList" component={ShoppingList} />
                <Stack.Screen name="Credits" component={Credits} />
                <Stack.Screen name="Imprint" component={Imprint} />
                <Stack.Screen name="ProductInfo" component={ProductInfo} />
                <Stack.Screen name="Report" component={Report} />
                <Stack.Screen name="Debug" component={Debug} />
                <Stack.Screen name="MFA" component={MFA} />
                <Stack.Screen name="Request" component={Request} />
                <Stack.Screen name="About" component={About} />
            </Stack.Navigator>
        </>
    );
}

export default OverviewStack;
