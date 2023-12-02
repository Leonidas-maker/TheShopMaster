import React from "react";
import { useTranslation } from "react-i18next";
import { Text, View } from "react-native";

import Registration from "../registration/registration";
import Login from "../login/login";
import Dashboard from "../dashboard/dashboard";

const Loading = (props) => {
    const { navigation } = props;

    const { t } = useTranslation();

    return (
        <View>
            <Text>
                {`Loading...
This will be the initial page where the app checks if you are already logged in or not
This is just a menu to test some basic functions: 

`}
<Text onPress={() => navigation.navigate(Registration)}>Registration</Text>
{`

`}
<Text onPress={() => navigation.navigate(Login)}>Login</Text>
{`

`}
<Text onPress={() => navigation.navigate(Dashboard)}>Dashboard</Text>
            </Text>
        </View>
    );
}

export default Loading;