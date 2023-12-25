import React from "react";
import { useTranslation } from "react-i18next";
import { Text, View } from "react-native";

function Credits() {

    const { t } = useTranslation();

    return (
        <View>
            <Text>Welcome to the Credits page</Text>
        </View>
    );
}

export default Credits;