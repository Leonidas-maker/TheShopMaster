import React from "react";
import { useTranslation } from "react-i18next";
import { Text, View } from "react-native";

function Login() {

    const { t } = useTranslation();

    return (
        <View>
            <Text>Welcome to the Login page</Text>
        </View>
    );
}

export default Login;