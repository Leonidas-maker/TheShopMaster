import React from "react";
import { useTranslation } from "react-i18next";
import { Text, View } from "react-native";

function Request() {

    const { t } = useTranslation();

    return (
        <View>
            <Text>Welcome to the Request page</Text>
        </View>
    );
}

export default Request;