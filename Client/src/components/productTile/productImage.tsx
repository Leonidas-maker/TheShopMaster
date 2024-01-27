import React from "react";
import { Image, ImageSourcePropType } from "react-native";
import { styled } from "nativewind";

const StyledImage = styled(Image);

//* Prop imagePath expects a location to an image
//* with the following format: require('../../../public/images/test_image.png')
interface ProductImageProps {
  imagePath: ImageSourcePropType;
}
// className={`w-5/6 h-5/6 rounded-md z-20`}
function ProductImage({ imagePath }: ProductImageProps) {
  return (
    <StyledImage
      source={imagePath}
      className={`w-full h-full rounded-md z-20`}
      resizeMode="contain"
    />
  );
}

export default ProductImage;
