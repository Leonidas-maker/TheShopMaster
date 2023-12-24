import React from "react";
import { useTranslation } from "react-i18next";
import { Text, View } from "react-native";

function Scanner() {

    const { t } = useTranslation();

    return (
        <View>
            <Text>Welcome to the Scanner page</Text>
        </View>
    );
}

export default Scanner;