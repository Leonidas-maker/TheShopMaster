import React from "react";
import { Text, View } from "react-native";
import { styled } from "nativewind";

const StyledView = styled(View);
const StyledText = styled(Text);

//* Prop prodPrice expects a string of the price of a product
//* with the following format: xx,xx€
interface ProductPriceProps {
    prodPrice: string;
}

function ProductSalePrice({ prodPrice }: ProductPriceProps) {
  return (
    <StyledView className={`bg-red-400 absolute bottom-0 right-0 w-1/2 aspect-square z-30 rounded-full mb-[-10px] mr-[-10px] items-center justify-center`}>
        <StyledText className={`text-black font-bold text-xl`}>{prodPrice}</StyledText>
    </StyledView>
  );
}

export default ProductSalePrice;
