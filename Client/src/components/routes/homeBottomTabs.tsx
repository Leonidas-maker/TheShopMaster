import { createBottomTabNavigator } from '@react-navigation/bottom-tabs';
import { StatusBar, View } from 'react-native';
import { styled } from 'nativewind';
import { PopupProvider } from '../../context/scannerInfoPopupContext';

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
import InfoButton from '../buttons/infoButton';

const Tab = createBottomTabNavigator();

function HomeBottomTabs() {
    const StyledView = styled(View);

    return (
        <>
            <StatusBar barStyle="light-content" />
            <PopupProvider>
                <Tab.Navigator
                    initialRouteName="Dashboard"
                    screenOptions={{
                        headerShown: true,
                        headerStyle: {
                            backgroundColor: '#171717',
                        },
                        tabBarStyle: { backgroundColor: '#171717' },
                        headerTintColor: '#f5f5f5',
                        tabBarActiveTintColor: '#a3a3a3',
                        tabBarInactiveTintColor: '#f5f5f5'
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
                                    <InfoButton />
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
            </PopupProvider>
        </>
    );
}

export default HomeBottomTabs;
