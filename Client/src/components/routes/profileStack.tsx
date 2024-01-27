import { createStackNavigator, StackNavigationProp } from '@react-navigation/stack';
import { StatusBar } from 'react-native';
import Settings from '../../screens/settings/settings';

const Stack = createStackNavigator();

function ProfileStack() {
    return (
        <>
            <StatusBar barStyle="light-content" />
            <Stack.Navigator initialRouteName="Settings" >
                <Stack.Screen
                    name="Settings"
                    component={Settings}
                    options={{ headerShown: true, headerBackTitle: "Zurück" }}
                />
            </Stack.Navigator>
        </>
    );
}

export default ProfileStack;
