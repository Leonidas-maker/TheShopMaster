import React from "react";
import { useTranslation } from "react-i18next";
import { View } from "react-native";
import SearchBarShop from "../../components/searchBar/searchBarShop";
import { styled } from "nativewind";

const StyledView = styled(View);

function Search() {
    const { t } = useTranslation();

    return (
        <StyledView className={`bg-primary h-full`}>
            <SearchBarShop />
        </StyledView>
    );
}

export default Search;