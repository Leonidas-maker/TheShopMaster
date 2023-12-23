import React, { useState } from "react";
import { useTranslation } from "react-i18next";
import { Text, View, Image, ScrollView, TouchableOpacity, Pressable } from "react-native";
import { styled } from "nativewind";

import PopupModal from "../../components/popups/testpopup";

const StyledView = styled(View);
const StyledText = styled(Text);
const StyledImage = styled(Image);
const StyledScrollView = styled(ScrollView);
const StyledTouchableOpacity = styled(TouchableOpacity);

function Dashboard() {
  const [isPopupVisible, setPopupVisible] = useState(false);

  const { t } = useTranslation();

  return (
    <StyledScrollView className={`bg-gray-800 h-screen`}>
      <PopupModal visible={isPopupVisible} onClose={() => setPopupVisible(false)} />
      <StyledView className={`items-center`}>
        <StyledTouchableOpacity className={`w-max h-max relative`} onPress={() => setPopupVisible(true)}>
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
        </StyledTouchableOpacity>
      </StyledView>
    </StyledScrollView>
  );
}

export default Dashboard;
