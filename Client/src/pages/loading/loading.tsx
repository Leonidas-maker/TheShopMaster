import React from "react";
import { useTranslation } from "react-i18next";
import { Text, View } from "react-native";

import Registration from "../registration/registration";
import Login from "../login/login";
import Dashboard from "../dashboard/dashboard";
import LoadingSVG from "../../components/svg/loadingSVG";

const Loading = (props:any) => {
    const { navigation } = props;

    const { t } = useTranslation();

    return (
        <View>
            <Text>
                {`Loading...
This will be the initial page where the app checks if you are already logged in or not
This is just a menu to test some basic functions: 

`}
<LoadingSVG />
<button type="button" onClick={() => navigation.navigate(Registration)} className="text-white bg-blue-700 hover:bg-blue-800 focus:outline-none focus:ring-4 focus:ring-blue-300 font-medium rounded-full text-sm px-5 py-2.5 text-center me-2 mb-2 dark:bg-blue-600 dark:hover:bg-blue-700 dark:focus:ring-blue-800">Registration</button>
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