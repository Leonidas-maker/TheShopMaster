import React from "react";
import { useTranslation } from "react-i18next";
import { Text, View, Image, ScrollView } from "react-native";
import { styled } from "nativewind";

import ProductTile from "../../components/productTile/productTile";

const StyledView = styled(View);
const StyledText = styled(Text);
const StyledScrollView = styled(ScrollView);

function Dashboard() {

  const { t } = useTranslation();

  //TODO: Add logic to insert products from database
  //TODO: Edit Styling of Web Version (too much tiles in one row)
  return (
    <StyledScrollView className={`bg-gray-800 h-screen`}>
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
