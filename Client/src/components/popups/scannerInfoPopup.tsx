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

interface ScannerInfoPopupProps {
    visible: boolean;
    onClose: () => void;
}

const ScannerInfoPopup: React.FC<ScannerInfoPopupProps> = ({
    visible,
    onClose,
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
                            <StyledText className={`mb-4`}>
                                - EAN-8 wie zum Beispiel: 20123451
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

export default ScannerInfoPopup;