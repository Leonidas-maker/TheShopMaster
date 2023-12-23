import React from "react";
import { useTranslation } from "react-i18next";
import { Text, View } from "react-native";

function ShoppingList() {

    const { t } = useTranslation();

    return (
        <View>
            <Text>Welcome to the Shopping List page</Text>
        </View>
    );
}

export default ShoppingList;