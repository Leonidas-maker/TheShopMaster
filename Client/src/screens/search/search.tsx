import React from "react";
import { useTranslation } from "react-i18next";
import { View } from "react-native";
import SearchBarShop from "../../components/searchBar/searchBarShop";

function Search() {
    const { t } = useTranslation();

    return (
        <View>
            <SearchBarShop />
        </View>
    );
}

export default Search;