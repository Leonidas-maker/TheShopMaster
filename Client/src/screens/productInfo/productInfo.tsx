import React from "react";
import { useTranslation } from "react-i18next";
import { Text, View } from "react-native";

function ProductInfo() {

    const { t } = useTranslation();

    return (
        <View>
            <Text>Welcome to the Product Info page</Text>
        </View>
    );
}

export default ProductInfo;