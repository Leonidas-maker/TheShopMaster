import { createBottomTabNavigator } from '@react-navigation/bottom-tabs';
import { StatusBar } from 'react-native';

import UserSVG from '../../../public/images/svg/userSVG';
import DashboardSVG from '../../../public/images/svg/dashboardSVG';
import ScannerSVG from '../../../public/images/svg/scannerSVG';
import SearchSVG from '../../../public/images/svg/searchSVG';
import ShoppingCartSVG from '../../../public/images/svg/shoppingCartSVG';
import SettingsSVG from '../../../public/images/svg/settingsSVG';

import Dashboard from '../../screens/dashboard/dashboard';
import OverviewStack from './overviewStack';
import Scanner from '../../screens/scanner/scanner';
import Search from '../../screens/search/search';
import ShoppingList from '../../screens/shoppingList/shoppingList';

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
                    name="Aktuelles" 
                    component={Dashboard} 
                    options={{
                        headerTitle: 'TheShopMaster',
                        tabBarIcon: ({ color, size }) => (
                            <DashboardSVG width={size} height={size} fill={color} />
                        )
                    }}
                />
                <Tab.Screen 
                    name="QR Code" 
                    component={Scanner} 
                    options={{
                        headerTitle: 'TheShopMaster',
                        tabBarIcon: ({ color, size }) => (
                            <ScannerSVG width={size} height={size} fill={color} />
                        )
                    }}
                />
                <Tab.Screen 
                    name="Suche" 
                    component={Search} 
                    options={{
                        headerTitle: 'TheShopMaster',
                        tabBarIcon: ({ color, size }) => (
                            <SearchSVG width={size} height={size} fill={color} />
                        )
                    }}
                />
                <Tab.Screen 
                    name="Einkaufswagen" 
                    component={ShoppingList} 
                    options={{
                        headerTitle: 'TheShopMaster',
                        tabBarIcon: ({ color, size }) => (
                            <ShoppingCartSVG width={size} height={size} fill={color} />
                        )
                    }}
                />
                <Tab.Screen 
                    name="Einstellungen" 
                    component={OverviewStack} 
                    options={{
                        headerTitle: 'Page navigator',
                        tabBarIcon: ({ color, size }) => (
                            <SettingsSVG width={size} height={size} fill={color} />
                        )
                    }}
                />
            </Tab.Navigator>
        </>
    );
}

export default HomeBottomTabs;
