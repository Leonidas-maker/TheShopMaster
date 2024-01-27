import React from "react";
import { TouchableOpacity, Image } from "react-native";
import { styled } from "nativewind";
import Settings from "../../screens/settings/settings";
import { useNavigation } from '@react-navigation/native';

function ProfileButton() {
    const StyledTouchableOpacity = styled(TouchableOpacity);
    const StyledImage = styled(Image);

    const navigation = useNavigation<any>();

    const handlePress = () => {
        navigation.navigate('ProfileStack', { screen: 'Settings' })
    };

    return (
        <StyledTouchableOpacity
            className={`absolute top-3 right-3 rounded-full w-14 h-14 overflow-hidden`}
            onPress={handlePress}
        >
            <StyledImage
                style={{ width: '100%', height: '100%' }}
                source={require("../../../public/images/TheShopMaster.png")}
                resizeMode="cover"
            />
        </StyledTouchableOpacity>
    );
}

export default ProfileButton;
