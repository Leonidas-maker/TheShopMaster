import React from "react";
import { useTranslation } from "react-i18next";
import { Text, View } from "react-native";

function Search() {

    const { t } = useTranslation();

    return (
        <View>
            <Text>Welcome to the Search page</Text>
        </View>
    );
}

export default Search;