import React from "react";
import { useTranslation } from "react-i18next";
import { Text, View } from "react-native";

function MFA() {

    const { t } = useTranslation();

    return (
        <View>
            <Text>Welcome to the MFA page</Text>
        </View>
    );
}

export default MFA;