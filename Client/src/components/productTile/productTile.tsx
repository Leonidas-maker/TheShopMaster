import React, { useState } from "react";
import { useTranslation } from "react-i18next";
import { Text, View, TouchableOpacity, ImageSourcePropType } from "react-native";
import { styled } from "nativewind";

import ProductPopup from "../popups/productPopup";
import ProductPrice from "./productPrice/productPrice";
import ProductSalePrice from "./productPrice/productSalePrice";
import ProductImage from "./productImage";

const StyledView = styled(View);
const StyledTouchableOpacity = styled(TouchableOpacity);

//* Prop image expects a location to an image (optional - default: defaultProduct.png)
//* with the following format: require('../../../public/images/defaultProduct.png')
//* Prop priceType expects a string of the price type of a product (optional - default: 'regular')
//* with the following format: 'regular' | 'sale'
//* Prop price expects a string of the price of a product (optional - default: 'N/A')
//* with the following format: xx,xx€
interface ProductTileProps {
  image?: ImageSourcePropType;
  priceType?: 'regular' | 'sale';
  price?: string;
}

function ProductTile({ image = require('../../../public/images/defaultProduct.png'),
  priceType = "regular",
  price = "N/A" }: ProductTileProps) {

  const [isPopupVisible, setPopupVisible] = useState(false);

  const { t } = useTranslation();

  return (
    <StyledView className={`h-max flex`}>
      <ProductPopup visible={isPopupVisible} onClose={() => setPopupVisible(false)} />
      <StyledView className={`items-center`}>
        <StyledTouchableOpacity className={`w-max h-max p-2 relative mb-4`} onPress={() => setPopupVisible(true)}>
          <StyledView className={`bg-neutral-400 w-36 aspect-square shadow-md rounded-md justify-center items-center z-10`}>
            <ProductImage imagePath={image} />
          </StyledView>
          {priceType === 'regular' && <ProductPrice prodPrice={price} />}
          {priceType === 'sale' && <ProductSalePrice prodPrice={price} />}
        </StyledTouchableOpacity>
      </StyledView>
    </StyledView>
  );
}

export default ProductTile;
