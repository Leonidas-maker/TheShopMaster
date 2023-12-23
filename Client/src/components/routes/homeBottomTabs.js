import { createBottomTabNavigator } from '@react-navigation/bottom-tabs';
import Registration from '../../screens/registration/registration';
import Login from '../../screens/login/login';
import Dashboard from '../../screens/dashboard/dashboard';
import Settings from '../../screens/settings/settings';
import Overview from '../../screens/overview/overview';
import { StatusBar } from 'react-native';

import UserSVG from '../../../public/images/svg/userSVG';

const Tab = createBottomTabNavigator();

function HomeBottomTabs() {
    return (
        <>
            <StatusBar barStyle="light-content" />
            <Tab.Navigator
                initialRouteName="Dashboard"
                screenOptions={{
                    headerShown: true,
                    headerStyle: {
                        backgroundColor: '#0F0F0F',
                    },
                    tabBarStyle: { backgroundColor: '#0F0F0F' },
                    headerTintColor: '#008170',
                    tabBarActiveTintColor: '#005B41',
                    tabBarInactiveTintColor: '#008170'
                }}
            >
                <Tab.Screen 
                    name="Dashboard" 
                    component={Dashboard} 
                    options={{
                        headerTitle: 'TheShopMaster',
                        tabBarIcon: ({ color, size }) => (
                            <UserSVG width={size} height={size} fill={color} />
                        )
                    }}
                />
                <Tab.Screen 
                    name="Login" 
                    component={Login} 
                    options={{
                        headerTitle: 'TheShopMaster',
                    }}
                />
                <Tab.Screen 
                    name="Registration" 
                    component={Registration} 
                    options={{
                        headerTitle: 'TheShopMaster',
                    }}
                />
                <Tab.Screen 
                    name="Settings" 
                    component={Settings} 
                    options={{
                        headerTitle: 'TheShopMaster',
                    }}
                />
                <Tab.Screen 
                    name="Overview" 
                    component={Overview} 
                    options={{
                        headerTitle: 'Page navigator',
                    }}
                />
            </Tab.Navigator>
        </>
    );
}

export default HomeBottomTabs;
