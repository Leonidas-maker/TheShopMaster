import React from "react";
import { useTranslation } from "react-i18next";
import { Image, ImageSourcePropType } from "react-native";
import { styled } from "nativewind";

const StyledImage = styled(Image);

// Prop imagePath expects a location to an image
// with the following format: require('../../../public/images/test_image.png')
interface ProductImageProps {
  imagePath: ImageSourcePropType;
}

function ProductImage({ imagePath }: ProductImageProps) {
  const { t } = useTranslation();

  return (
    <StyledImage
      source={imagePath}
      className={`w-5/6 h-5/6 rounded-md z-20`}
      resizeMode="contain"
    />
  );
}

export default ProductImage;
