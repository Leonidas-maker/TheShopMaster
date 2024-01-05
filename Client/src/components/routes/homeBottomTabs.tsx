import { createBottomTabNavigator } from '@react-navigation/bottom-tabs';
import { StatusBar, Button , View} from 'react-native';
import { styled } from 'nativewind';

import DashboardSVG from '../../../public/images/svg/navigatorIcons/inactive/dashboardSVG';
import ScannerSVG from '../../../public/images/svg/navigatorIcons/inactive/scannerSVG';
import SearchSVG from '../../../public/images/svg/navigatorIcons/inactive/searchSVG';
import ShoppingCartSVG from '../../../public/images/svg/navigatorIcons/inactive/shoppingCartSVG';
import SettingsSVG from '../../../public/images/svg/navigatorIcons/inactive/settingsSVG';

import Dashboard from '../../screens/dashboard/dashboard';
import OverviewStack from './overviewStack';
import Scanner from '../../screens/scanner/scanner';
import Search from '../../screens/search/search';
import ShoppingList from '../../screens/shoppingList/shoppingList';
import ActiveDashboardSVG from '../../../public/images/svg/navigatorIcons/active/activeDashboardSVG';
import ActiveSearchSVG from '../../../public/images/svg/navigatorIcons/active/activeSearchSVG';
import ActiveShoppingCartSVG from '../../../public/images/svg/navigatorIcons/active/activeShoppingCartSVG';
import ActiveSettingsSVG from '../../../public/images/svg/navigatorIcons/active/activeSettingsSVG';

const Tab = createBottomTabNavigator();

function HomeBottomTabs() {
    const StyledView = styled(View);
    const StyledButton = styled(Button);

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
                        tabBarIcon: ({ color, size, focused }) => {
                            if (focused) {
                                return <ActiveDashboardSVG width={size} height={size} fill={color} />;
                            } else {
                                return <DashboardSVG width={size} height={size} fill={color} />;
                            }
                        },
                    }}
                />
                <Tab.Screen 
                    name="QR Code" 
                    component={Scanner} 
                    options={{
                        headerTitle: 'TheShopMaster',
                        tabBarIcon: ({ color, size }) => (
                            <ScannerSVG width={size} height={size} fill={color} />
                        ),
                        headerRight: () => (
                            <StyledView className={`mx-5`}>
                                <StyledButton
                                    onPress={() => alert('This is a button!')}
                                    title="Info"
                                    className={`bg-gray-800 text-white rounded-md p-3 mt-5 items-center justify-center mx-10`}
                                />
                            </StyledView>
                        ),
                    }}
                />
                <Tab.Screen 
                    name="Suche" 
                    component={Search} 
                    options={{
                        headerTitle: 'TheShopMaster',
                        tabBarIcon: ({ color, size, focused }) => {
                            if (focused) {
                                return <ActiveSearchSVG width={size} height={size} fill={color} />;
                            } else {
                                return <SearchSVG width={size} height={size} fill={color} />;
                            }
                        },
                    }}
                />
                <Tab.Screen 
                    name="Einkaufswagen" 
                    component={ShoppingList} 
                    options={{
                        headerTitle: 'TheShopMaster',
                        tabBarIcon: ({ color, size, focused }) => {
                            if (focused) {
                                return <ActiveShoppingCartSVG width={size} height={size} fill={color} />;
                            } else {
                                return <ShoppingCartSVG width={size} height={size} fill={color} />;
                            }
                        },
                    }}
                />
                <Tab.Screen 
                    name="Einstellungen" 
                    component={OverviewStack} 
                    options={{
                        headerTitle: 'Page navigator',
                        headerShown: false,
                        tabBarIcon: ({ color, size, focused }) => {
                            if (focused) {
                                return <ActiveSettingsSVG width={size} height={size} fill={color} />;
                            } else {
                                return <SettingsSVG width={size} height={size} fill={color} />;
                            }
                        },
                    }}
                />
            </Tab.Navigator>
        </>
    );
}

export default HomeBottomTabs;
