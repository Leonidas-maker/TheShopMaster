import { createBottomTabNavigator } from '@react-navigation/bottom-tabs';
import Registration from '../../pages/registration/registration';
import Login from '../../pages/login/login';
import Dashboard from '../../pages/dashboard/dashboard';
import Settings from '../../pages/settings/settings';

const Tab = createBottomTabNavigator();

function HomeBottomTabs() {
    return (
        <Tab.Navigator initialRouteName="Dashboard">
        <Tab.Screen name="Dashboard" component={Dashboard} />
        <Tab.Screen name="Login" component={Login} />
        <Tab.Screen name="Registration" component={Registration} />
        <Tab.Screen name="Settings" component={Settings} />
        </Tab.Navigator>
  );
}

export default HomeBottomTabs;