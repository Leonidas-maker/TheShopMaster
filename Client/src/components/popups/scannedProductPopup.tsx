import React from 'react';
import {
    Modal,
    TouchableHighlight,
    View,
    Text,
    TouchableWithoutFeedback
} from 'react-native';
import { styled } from 'nativewind';

const StyledView = styled(View);
const StyledText = styled(Text);

//* Prop productEAN expects a EAN Code from a product (optional - default: N/A product not found)
//* with the following format: 5901234123457 (EAN13) or 20123451 (EAN8)
interface ScannedProductPopupProps {
    visible: boolean;
    onClose: () => void;
    productEAN?: String;
}

//TODO: Add logic to get product information from database based on productEAN
//TODO: Add styling for product informations
const ScannedProductPopup: React.FC<ScannedProductPopupProps> = ({
    visible,
    onClose,
    productEAN = "5901234123457",
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
                            <StyledView className={`justify-center items-center`}>
                                <StyledText className={`text-xl font-bold`}>
                                    Barcode Scanner Info
                                </StyledText>
                            </StyledView>
                            <StyledText className="mt-4 mb-4">
                                Der Barcode Scanner kann verwendet werden, 
                                um Produkte zu scannen, damit man direkt zu den Produktdetails gelangt.
                                Es können folgende Barcodes gescannt werden:
                            </StyledText>
                            <StyledText>
                                - EAN-13 wie zum Beispiel: 5901234123457
                            </StyledText>
                            <StyledText>
                                - EAN-8 wie zum Beispiel: 20123451
                            </StyledText>
                            <StyledText className={`mb-4`}>
                                - QR-Codes
                            </StyledText>
                            <TouchableHighlight
                                underlayColor="green"
                                className={`bg-red-600 rounded-md p-3 mb-2 items-center justify-center`}
                                onPress={onClose}
                            >
                                <StyledText className={`text-white font-bold`}>
                                    Zurück
                                </StyledText>
                            </TouchableHighlight>
                        </StyledView>
                    </TouchableWithoutFeedback>
                </StyledView>
            </TouchableWithoutFeedback>
        </Modal>
    );
};

export default ScannedProductPopup;