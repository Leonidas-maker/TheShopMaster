import React, { useState } from "react";
import { View, TouchableHighlight } from "react-native";
import { styled } from "nativewind";
import InfoSVG from "../../../public/images/svg/navigatorIcons/inactive/infoSVG";
import ActiveInfoSVG from "../../../public/images/svg/navigatorIcons/active/activeInfoSVG";
import { usePopup } from "../../context/scannerInfoPopupContext";

function InfoButton() {
    const StyledView = styled(View);
    const [isPressed, setIsPressed] = useState(false);
    const { setPopupVisible } = usePopup();

    return (
        <TouchableHighlight
            underlayColor="transparant"
            onPressIn={() => {
                setIsPressed(true);
            }}
            onPressOut={() => {
                setIsPressed(false);
            }}
            onPress={() => {
                setPopupVisible(true);
            }}
        >
            <StyledView>
                {isPressed ? <ActiveInfoSVG width={30} height={30} fill="#E0E0E2" /> : <InfoSVG width={30} height={30} fill="#E0E0E2" />}
            </StyledView>
        </TouchableHighlight>
    );
}

export default InfoButton;
