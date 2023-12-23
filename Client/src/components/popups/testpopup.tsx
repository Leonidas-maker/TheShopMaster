import React from 'react';
import { Modal, Pressable, View, Text, TouchableWithoutFeedback } from 'react-native';
import { styled } from 'nativewind';

const StyledView = styled(View);
const StyledText = styled(Text);
const StyledPressable = styled(Pressable);

interface PopupModalProps {
  visible: boolean;
  onClose: () => void;
}

const PopupModal: React.FC<PopupModalProps> = ({ visible, onClose }) => {
    return (
        <Modal
            animationType="fade"
            transparent={true}
            visible={visible}
            onRequestClose={onClose}
        >
            <TouchableWithoutFeedback onPress={onClose}>
                <StyledView className={`flex-1 items-center justify-center`} style={{ backgroundColor: 'rgba(0, 0, 0, 0.5)' }}>
                    <TouchableWithoutFeedback onPress={(e) => e.stopPropagation()}>
                        <StyledView className={`m-4 bg-white p-5 rounded-lg shadow-lg max-w-xs w-full`}>
                            <StyledText className={`mb-4`}>Hier werden Produktinfos angezeigt</StyledText>
                            <StyledPressable className={`bg-red-500 rounded-md p-2`} onPress={onClose}>
                                <StyledText className={`text-white`}>Schließe Popup</StyledText>
                            </StyledPressable>
                        </StyledView>
                    </TouchableWithoutFeedback>
                </StyledView>
            </TouchableWithoutFeedback>
        </Modal>
    );
};

export default PopupModal;
