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
import { expo } from "../../../app.json";
import Credits from "../credits/credits";
import Imprint from "../imprint/imprint";
import MFA from "../mfa/mfa";
import ProductInfo from '../productInfo/productInfo';
import Request from '../request/request';
import Report from "../report/report";
import About from "../about/about";

const StyledView = styled(View);
const StyledText = styled(Text);
const StyledTouchableOpacity = styled(TouchableOpacity);
const StyledScrollView = styled(ScrollView);

function Overview(props: any) {
    const { navigation } = props;
    const { t } = useTranslation();

    return (
        <StyledScrollView className={`h-screen bg-primary`}>
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
                <StyledTouchableOpacity onPress={() => navigation.navigate(MFA)}>
                    <StyledView className={`flex-row justify-between items-center h-full px-4`}>
                        <StyledText className={`text-white font-bold text-2xl`}>MFA</StyledText>
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
                <StyledTouchableOpacity onPress={() => navigation.navigate(ProductInfo)}>
                    <StyledView className={`flex-row justify-between items-center h-full px-4`}>
                        <StyledText className={`text-white font-bold text-2xl`}>Product Info</StyledText>
                        <StyledText className={`text-white font-bold text-2xl`}>{`>`}</StyledText>
                    </StyledView>
                </StyledTouchableOpacity>
            </StyledView>
            <StyledView className={`bg-black w-full h-20`}>
                <StyledTouchableOpacity onPress={() => navigation.navigate(Report)}>
                    <StyledView className={`flex-row justify-between items-center h-full px-4`}>
                        <StyledText className={`text-white font-bold text-2xl`}>Report</StyledText>
                        <StyledText className={`text-white font-bold text-2xl`}>{`>`}</StyledText>
                    </StyledView>
                </StyledTouchableOpacity>
            </StyledView>
            <StyledView className={`bg-black w-full h-20`}>
                <StyledTouchableOpacity onPress={() => navigation.navigate(Request)}>
                    <StyledView className={`flex-row justify-between items-center h-full px-4`}>
                        <StyledText className={`text-white font-bold text-2xl`}>Request</StyledText>
                        <StyledText className={`text-white font-bold text-2xl`}>{`>`}</StyledText>
                    </StyledView>
                </StyledTouchableOpacity>
            </StyledView>
            <StyledView className={`bg-black w-full h-20`}>
                <StyledTouchableOpacity onPress={() => navigation.navigate(Imprint)}>
                    <StyledView className={`flex-row justify-between items-center h-full px-4`}>
                        <StyledText className={`text-white font-bold text-2xl`}>Imprint</StyledText>
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
            <StyledView className={`bg-black w-full h-20`}>
                <StyledTouchableOpacity onPress={() => navigation.navigate(Credits)}>
                    <StyledView className={`flex-row justify-between items-center h-full px-4`}>
                        <StyledText className={`text-white font-bold text-2xl`}>Credits</StyledText>
                        <StyledText className={`text-white font-bold text-2xl`}>{`>`}</StyledText>
                    </StyledView>
                </StyledTouchableOpacity>
            </StyledView>
            <StyledView className={`bg-black w-full h-20`}>
                <StyledTouchableOpacity onPress={() => navigation.navigate(About)}>
                    <StyledView className={`flex-row justify-between items-center h-full px-4`}>
                        <StyledText className={`text-white font-bold text-2xl`}>About us</StyledText>
                        <StyledText className={`text-white font-bold text-2xl`}>{`>`}</StyledText>
                    </StyledView>
                </StyledTouchableOpacity>
            </StyledView>
            <StyledView className={`justify-center items-center my-2`}>
                <StyledText className={`text-white`}>App Version: {expo.version} ❤️</StyledText>
            </StyledView>
        </StyledScrollView>
    );
}

export default Overview;
