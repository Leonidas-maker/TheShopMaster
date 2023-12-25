import React from "react";
import { useTranslation } from "react-i18next";
import { Text, View } from "react-native";

function Imprint() {

    const { t } = useTranslation();

    return (
        <View>
            <Text>Welcome to the Imprint page</Text>
        </View>
    );
}

export default Imprint;