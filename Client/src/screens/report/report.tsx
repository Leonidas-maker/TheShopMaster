import React from "react";
import { useTranslation } from "react-i18next";
import { Text, View } from "react-native";

function Report() {

    const { t } = useTranslation();

    return (
        <View>
            <Text>Welcome to the Report page</Text>
        </View>
    );
}

export default Report;