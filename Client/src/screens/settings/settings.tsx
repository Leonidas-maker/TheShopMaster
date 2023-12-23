import React from "react";
import { useTranslation } from "react-i18next";
import { Text, View } from "react-native";

function Settings() {

    const { t } = useTranslation();

    return (
        <View>
            <Text>Welcome to the Settings page</Text>
        </View>
    );
}

export default Settings;