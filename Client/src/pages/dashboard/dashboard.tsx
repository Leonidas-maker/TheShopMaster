import React from "react";
import { useTranslation } from "react-i18next";
import { Text, View } from "react-native";
import { styled } from "nativewind";

const StyledView = styled(View);
const StyledText = styled(Text);

function Dashboard() {

    const { t } = useTranslation();

    return (
        // Beispiel: bg-gray-800 für dunkelgrauen Hintergrund und text-white für weißen Text
        <StyledView className={`bg-gray-800 flex-1 justify-center items-center`}>
            <StyledText className={`text-white`}>Welcome to the Dashboard page</StyledText>
        </StyledView>
    );
}

export default Dashboard;
