import React from "react";
import { useTranslation } from "react-i18next";
import { Text, View, TouchableOpacity, ScrollView } from "react-native";
import { styled } from "nativewind";

import Dashboard from "../dashboard/dashboard";
import Loading from "../loading/loading";
import Login from "../login/login";
import Registration from "../registration/registration";
import Settings from "../settings/settings";
import ShoppingList from "../shoppingList/shoppingList";
import Debug from "../devScreens/debug/debug";

const StyledView = styled(View);
const StyledText = styled(Text);
const StyledTouchableOpacity = styled(TouchableOpacity);
const StyledScrollView = styled(ScrollView);

function Overview(props: any) {
    const { navigation } = props;
    const { t } = useTranslation();

    return (
        <StyledScrollView className={`h-screen bg-gray-700`}>
            <StyledView className={`bg-black w-full h-20`}>
                <StyledTouchableOpacity onPress={() => navigation.navigate(Dashboard)}>
                    <StyledView className={`flex-row justify-between items-center h-full px-4`}>
                        <StyledText className={`text-white font-bold text-2xl`}>Dashboard</StyledText>
                        <StyledText className={`text-white font-bold text-2xl`}>{`>`}</StyledText>
                    </StyledView>
                </StyledTouchableOpacity>
            </StyledView>
            <StyledView className={`bg-black w-full h-20`}>
                <StyledTouchableOpacity onPress={() => navigation.navigate(Loading)}>
                    <StyledView className={`flex-row justify-between items-center h-full px-4`}>
                        <StyledText className={`text-white font-bold text-2xl`}>Loading</StyledText>
                        <StyledText className={`text-white font-bold text-2xl`}>{`>`}</StyledText>
                    </StyledView>
                </StyledTouchableOpacity>
            </StyledView>
            <StyledView className={`bg-black w-full h-20`}>
                <StyledTouchableOpacity onPress={() => navigation.navigate(Login)}>
                    <StyledView className={`flex-row justify-between items-center h-full px-4`}>
                        <StyledText className={`text-white font-bold text-2xl`}>Login</StyledText>
                        <StyledText className={`text-white font-bold text-2xl`}>{`>`}</StyledText>
                    </StyledView>
                </StyledTouchableOpacity>
            </StyledView>
            <StyledView className={`bg-black w-full h-20`}>
                <StyledTouchableOpacity onPress={() => navigation.navigate(Registration)}>
                    <StyledView className={`flex-row justify-between items-center h-full px-4`}>
                        <StyledText className={`text-white font-bold text-2xl`}>Registration</StyledText>
                        <StyledText className={`text-white font-bold text-2xl`}>{`>`}</StyledText>
                    </StyledView>
                </StyledTouchableOpacity>
            </StyledView>
            <StyledView className={`bg-black w-full h-20`}>
                <StyledTouchableOpacity onPress={() => navigation.navigate(Settings)}>
                    <StyledView className={`flex-row justify-between items-center h-full px-4`}>
                        <StyledText className={`text-white font-bold text-2xl`}>Settings</StyledText>
                        <StyledText className={`text-white font-bold text-2xl`}>{`>`}</StyledText>
                    </StyledView>
                </StyledTouchableOpacity>
            </StyledView>
            <StyledView className={`bg-black w-full h-20`}>
                <StyledTouchableOpacity onPress={() => navigation.navigate(ShoppingList)}>
                    <StyledView className={`flex-row justify-between items-center h-full px-4`}>
                        <StyledText className={`text-white font-bold text-2xl`}>Shopping List</StyledText>
                        <StyledText className={`text-white font-bold text-2xl`}>{`>`}</StyledText>
                    </StyledView>
                </StyledTouchableOpacity>
            </StyledView>
            <StyledView className={`bg-black w-full h-20`}>
                <StyledTouchableOpacity onPress={() => navigation.navigate(Debug)}>
                    <StyledView className={`flex-row justify-between items-center h-full px-4`}>
                        <StyledText className={`text-white font-bold text-2xl`}>Debug</StyledText>
                        <StyledText className={`text-white font-bold text-2xl`}>{`>`}</StyledText>
                    </StyledView>
                </StyledTouchableOpacity>
            </StyledView>
        </StyledScrollView>
    );
}

export default Overview;
