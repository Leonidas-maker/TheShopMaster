import React from "react";
import { useTranslation } from "react-i18next";
import { Text, View, ScrollView } from "react-native";
import { styled } from "nativewind";

import ProductTile from "../../components/productTile/productTile";
import ProfileButton from "../../components/buttons/profileButton";

const StyledView = styled(View);
const StyledText = styled(Text);
const StyledScrollView = styled(ScrollView);

function Dashboard() {
  const { t } = useTranslation();

  //TODO: Add logic to insert products from database
  //TODO: Edit Styling of Web Version (too much tiles in one row)
  return (
    <StyledScrollView className={`h-screen bg-primary relative`}>
      <ProfileButton />
      <StyledView className={`my-6 mr-16 ml-5`}>
        <StyledText className={`text-4xl text-font_primary font-bold mr-20`}>
          Hello, User
        </StyledText>
        <StyledText className={`text-2xl text-font_secondary font-bold`}>
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