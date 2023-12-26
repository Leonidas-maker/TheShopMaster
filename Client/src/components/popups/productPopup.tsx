import React from 'react';
import {
    Modal,
    TouchableHighlight,
    View,
    Text,
    TouchableWithoutFeedback,
    Image,
    ImageSourcePropType,
} from 'react-native';
import { styled } from 'nativewind';
import AddFavoriteButton from '../buttons/addFavoriteButton';

const StyledView = styled(View);
const StyledText = styled(Text);
const StyledImage = styled(Image);

//* Prop imagePath expects a location to an image (optional - default: defaultProduct.png)
//* with the following format: require('../../../public/images/defaultProduct.png')
interface ProductPopupProps {
    visible: boolean;
    onClose: () => void;
    imagePath?: ImageSourcePropType;
}

//TODO: Add onPress functionality to buttons
const ProductPopup: React.FC<ProductPopupProps> = ({
    visible,
    onClose,
    imagePath = require('../../../public/images/defaultProduct.png'),
}) => {
    return (
        <Modal
            animationType="fade"
            transparent={true}
            visible={visible}
            onRequestClose={onClose}
        >
            <TouchableWithoutFeedback onPress={onClose}>
                <StyledView
                    className={`flex-1 items-center justify-center`}
                    style={{ backgroundColor: 'rgba(0, 0, 0, 0.5)' }}
                >
                    <TouchableWithoutFeedback onPress={(e) => e.stopPropagation()}>
                        <StyledView
                            className={`m-4 bg-white p-5 rounded-lg shadow-lg max-w-sm w-full`}
                        >
                            <StyledView className={`relative`}>
                                <StyledImage
                                source={imagePath}
                                className={`aspect-square h-40 rounded-lg mx-auto`}
                                />
                                <StyledView className={`absolute z-10 bottom-10 left-20`}>
                                    <AddFavoriteButton />
                                </StyledView>
                            </StyledView>
                            <StyledText className="mt-4 mb-4">
                                Hier werden Produktinfos angezeigt, wie z.B. der günstigste Preis und Laden, die Mengenangaben, etc.
                                Der Nutzer kann hier auch das Produkt zu seiner Einkaufsliste hinzufügen und zu seinen Favoriten hinzufügen
                                als auch zur Produktseite mit allen Infos gelangen.
                            </StyledText>
                            <TouchableHighlight
                                underlayColor="green"
                                className={`bg-red-600 rounded-md p-3 mb-2 items-center justify-center`}
                                onPress={onClose}
                            >
                                <StyledText className={`text-white font-bold`}>
                                    In den Einkaufswagen
                                </StyledText>
                            </TouchableHighlight>
                            <StyledView className={`flex-row justify-center space-x-2`}>
                                <TouchableHighlight
                                    underlayColor="green"
                                    className={`flex-1 bg-red-600 rounded-md p-3 items-center justify-center`}
                                    onPress={onClose}
                                >
                                    <StyledText className={`text-white font-bold`}>
                                        Zurück
                                    </StyledText>
                                </TouchableHighlight>
                                <TouchableHighlight
                                    underlayColor="green"
                                    className={`flex-1 bg-red-600 rounded-md p-3 items-center justify-center`}
                                    onPress={onClose}
                                >
                                    <StyledText className={`text-white font-bold`}>
                                        Zur Produktseite
                                    </StyledText>
                                </TouchableHighlight>
                            </StyledView>
                        </StyledView>
                    </TouchableWithoutFeedback>
                </StyledView>
            </TouchableWithoutFeedback>
        </Modal>
    );
};

export default ProductPopup;
