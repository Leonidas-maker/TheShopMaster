import { createBottomTabNavigator } from '@react-navigation/bottom-tabs';
import Registration from '../../pages/registration/registration';
import Login from '../../pages/login/login';
import Dashboard from '../../pages/dashboard/dashboard';
import Settings from '../../pages/settings/settings';
import { StatusBar } from 'react-native';

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
            </Tab.Navigator>
        </>
    );
}

export default HomeBottomTabs;
