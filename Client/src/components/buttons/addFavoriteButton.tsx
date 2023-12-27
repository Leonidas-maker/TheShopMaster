import React, { useState } from "react";
import { View, TouchableHighlight } from "react-native";
import { styled } from "nativewind";
import FavoriteSVG from "../../../public/images/svg/popupIcons/inactive/favoriteSVG";
import ActiveFavoriteSVG from "../../../public/images/svg/popupIcons/active/activeFavoriteSVG";

const StyledView = styled(View);
const StyledTouchableHighlight = styled(TouchableHighlight);

//TODO: Add functionality to add favorites
//TODO: Add functionality to remove favorites
//TODO: Add functionality to check if product is already in favorites
//TODO: Add functionality to change color of favorite button if product is already in favorites
function AddFavoriteButton() {
    const [isFavorite, setIsFavorite] = useState(false);

    const svgSize = {
        width: '30',
        height: '30',
    };

    const handlePress = () => {
        setIsFavorite(!isFavorite);
    }

    return (
        <StyledTouchableHighlight
            onPress={handlePress}
        >
            <StyledView className="relative">
                <StyledView className="absolute inset-0 flex items-center justify-center bg-black rounded-full" style={{ width: 50, height: 50 }}>
                    {isFavorite ? (
                        <ActiveFavoriteSVG fill={'#FFBF00'} {...svgSize} />
                    ) : (
                        <FavoriteSVG fill={'#FFBF00'} {...svgSize} />
                    )}
                </StyledView>
            </StyledView>
        </StyledTouchableHighlight>
    );
}

export default AddFavoriteButton;
