import React from "react";
import { useTranslation } from "react-i18next";
import { Text, View } from "react-native";

function About() {

    const { t } = useTranslation();

    return (
        <View>
            <Text>Welcome to the About page</Text>
        </View>
    );
}

export default About;