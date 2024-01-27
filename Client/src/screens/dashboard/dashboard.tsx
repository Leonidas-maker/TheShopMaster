import React from "react";
import { useTranslation } from "react-i18next";
import { Text, View, Image, ScrollView, TouchableOpacity } from "react-native";
import { styled } from "nativewind";
import { useNavigation } from "@react-navigation/native";

import ProductTile from "../../components/productTile/productTile";
import Settings from "../settings/settings";

const StyledView = styled(View);
const StyledText = styled(Text);
const StyledScrollView = styled(ScrollView);
const StyledImage = styled(Image);
const StyledTouchableOpacity = styled(TouchableOpacity);

function Dashboard(props: any) {
  const { t } = useTranslation();

  const { navigation } = props;

  const handlePress = () => {
    navigation.navigate('ProfileStack', { screen: 'Settings' })
  };

  //TODO: Add logic to insert products from database
  //TODO: Edit Styling of Web Version (too much tiles in one row)
  return (
    <StyledScrollView className={`h-screen bg-darkBlue relative`}>
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
      <StyledView className={`my-6 mr-16 ml-5`}>
        <StyledText className={`text-4xl text-babyBlue font-bold mr-20`}>
          Hello, User
        </StyledText>
        <StyledText className={`text-2xl text-babyBlue font-bold`}>
          we have some new products with the best prices for you!
        </StyledText>
      </StyledView>
      <StyledView className={`flex flex-row flex-wrap justify-around px-4`}>
        <ProductTile
          image={require('../../../public/images/defaultProduct.png')}
          priceType="regular"
          price="10,00€"
        />
        <ProductTile
          image={require('../../../public/images/defaultProduct.png')}
          priceType="sale"
          price="5,00€"
        />
        <ProductTile
          image={require('../../../public/images/defaultProduct.png')}
          priceType="sale"
          price="1,99€"
        />
      </StyledView>
    </StyledScrollView>
  );
}

export default Dashboard;