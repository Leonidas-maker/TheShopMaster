import React from "react";
import { useTranslation } from "react-i18next";
import { Text, View } from "react-native";

function Dashboard() {

    const { t } = useTranslation();

    return (
        <View>
            <Text>Welcome to the Dashboard page</Text>
        </View>
    );
}

export default Dashboard;