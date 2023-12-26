import React from "react";
import { View, TouchableHighlight } from "react-native";
import { styled } from "nativewind";
import FavoriteSVG from "../../../public/images/svg/popupIcons/inactive/favoriteSVG";

const StyledView = styled(View);
const StyledTouchableHighlight = styled(TouchableHighlight);

//TODO: Add functionality to add favorites
//TODO: Add functionality to remove favorites
//TODO: Add functionality to check if product is already in favorites
//TODO: Add functionality to change color of favorite button if product is already in favorites
function AddFavoriteButton() {
  const svgSize = {
    width: '30',
    height: '30',
  };

  return (
    <StyledTouchableHighlight
        onPress={() => console.log('AddFavoriteButton pressed')}
    >
        <StyledView className="relative">
        <StyledView className="absolute inset-0 flex items-center justify-center bg-black rounded-full" style={{ width: 50, height: 50 }}>
            <FavoriteSVG fill={'#FFBF00'} {...svgSize} />
        </StyledView>
        </StyledView>
    </StyledTouchableHighlight>
  );
}

export default AddFavoriteButton;
