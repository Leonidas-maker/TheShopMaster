import React from "react";
import { useTranslation } from "react-i18next";
import { Text, View, Image } from "react-native";
import { styled } from "nativewind";

const StyledView = styled(View);
const StyledText = styled(Text);
const StyledImage = styled(Image);

function Dashboard() {

    const { t } = useTranslation();

    return (
        <StyledView className={`bg-gray-800 h-screen items-center`}>
            <StyledView className={`w-max h-max relative`}>
                <StyledView className={`bg-red-800 w-1/3 mt-5 aspect-square shadow-md rounded-md flex justify-center items-center z-10`}>
                    <StyledImage 
                        source={require('../../../public/images/test_image.png')}
                        className={`w-5/6 h-5/6 rounded-md z-20`}
                        resizeMode="contain"
                    />
                </StyledView>
                <StyledView className={`bg-yellow-300 absolute bottom-0 right-0 w-1/6 aspect-square z-30 rounded-full mb-[-10px] mr-[-10px] items-center justify-center`}>
                    <StyledText className={`text-black font-bold text-xl`}>1,99€</StyledText>
                </StyledView>
            </StyledView>
        </StyledView>
    );
}

export default Dashboard;
