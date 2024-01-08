import React, { useState } from "react";
import { useTranslation } from "react-i18next";
import { View, Platform, TouchableWithoutFeedback, Keyboard } from "react-native";
import { SearchBar } from 'react-native-elements';

//TODO: Add logic to search for products in database
//TODO: Make it possible to dismiss keyboard by clicking outside of searchbar
//? At the moment, the keyboard can only be dismissed by clicking the searchbar border 
//! onChangeText is throwing an error, probably because it has no proper function at the moment
//! searchQuery and setSearchQuery are just placeholders to display searchbar
function SearchBarShop() {
    const { t } = useTranslation();
    const [searchQuery, setSearchQuery] = useState("");

    const dismissKeyboard = () => {
        Keyboard.dismiss();
        console.log("Keyboard dismissed");
    };

    const renderSearchBar = () => {
        return (
            <SearchBar
                platform={Platform.OS === "ios" ? "ios" : "android"}
                onChangeText={setSearchQuery}
                value={searchQuery}
                placeholder="Suchen"
            />
        );
    };

    return (
        <TouchableWithoutFeedback onPress={dismissKeyboard}>
            <View>
                {renderSearchBar()}
            </View>
        </TouchableWithoutFeedback>
    );
}

export default SearchBarShop;