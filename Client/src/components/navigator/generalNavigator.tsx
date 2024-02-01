import React from "react";
import { Text, View, TouchableOpacity } from "react-native";
import { styled } from "nativewind";
import { useTranslation } from "react-i18next";
import Icon from 'react-native-vector-icons/MaterialIcons';
import { useNavigation } from '@react-navigation/native';

import Dashboard from "../../screens/dashboard/dashboard";
import Loading from "../../screens/loading/loading";

const StyledText = styled(Text);
const StyledView = styled(View);
const StyledTouchableOpacity = styled(TouchableOpacity);

function GeneralNavigator() {
    const navigation = useNavigation<any>();

    const handleDashboardPress = () => {
        navigation.navigate('OverviewStack', { screen: 'Dashboard' })
    };

    const handleLoadingPress = () => {
        navigation.navigate('OverviewStack', { screen: 'Loading' })
    };

    const { t } = useTranslation();

    return (
        <StyledView className="m-4">
            <StyledText className="text-font_primary text-xl font-bold mb-2">Allgemein</StyledText>
            <StyledView className="bg-secondary rounded-lg shadow-md p-4 border border-gray-700">
                <StyledTouchableOpacity
                    onPress={handleDashboardPress}
                >
                    <StyledView className="flex-row justify-between items-center">
                        <StyledView className="flex-row items-center">
                            <Icon name="dashboard" size={20} color="#E0E0E2" />
                            <StyledText className="text-font_primary font-bold text-lg ml-2">Dashboard</StyledText>
                        </StyledView>
                        <Icon name="arrow-forward-ios" size={20} color="#E0E0E2" />
                    </StyledView>
                </StyledTouchableOpacity>
                <View className="border-b border-gray-700 my-2" />
                <StyledTouchableOpacity
                    onPress={handleLoadingPress}
                >
                    <StyledView className="flex-row justify-between items-center">
                        <StyledView className="flex-row items-center">
                            <Icon name="hourglass-empty" size={20} color="#E0E0E2" />
                            <StyledText className="text-font_primary font-bold text-lg ml-2">Loading</StyledText>
                        </StyledView>
                        <Icon name="arrow-forward-ios" size={20} color="#E0E0E2" />
                    </StyledView>
                </StyledTouchableOpacity>
            </StyledView>
        </StyledView>
    );
}

export default GeneralNavigator;
