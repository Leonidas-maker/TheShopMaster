import React from "react";
import { useTranslation } from "react-i18next";
import { Text, View } from "react-native";

function Registration() {

    const { t } = useTranslation();

    return (
        <View>
            <Text>Welcome to the Registration page</Text>
        </View>
    );
}

export default Registration;