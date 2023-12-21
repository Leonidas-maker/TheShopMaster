import React from "react";
import { useTranslation } from "react-i18next";
import { Text, View, Pressable, ActivityIndicator, StyleSheet } from "react-native";
import { styled, useColorScheme } from "nativewind";

import { StyledComponent } from "nativewind";

import Registration from '../registration/registration';
import Login from "../login/login";
import Dashboard from "../dashboard/dashboard";
import LoadingSVG from "../../components/svg/loadingSVG";
import { RectButton } from "react-native-gesture-handler";

const StyledPressable = styled(Pressable);
const StyledView = styled(View);
const StyledActivityIndicator = styled(ActivityIndicator);
const StyledText = styled(Text);

const Loading = (props: any) => {
	const { navigation } = props;

	const { t } = useTranslation();

	return (
		<StyledView className={`flex h-screen items-center justify-center`}>
			<StyledActivityIndicator className={`content-center`} size="large" />
			<StyledText className={`text-black font-bold p-5`}>Loading...</StyledText>
			<Text>
				{`Loading...
This will be the initial page where the app checks if you are already logged in or not
This is just a menu to test some basic functions: 

`}
				<StyledPressable
					className={`font-bold text-white bg-blue-500 rounded-md p-2`}
					onPress={() => navigation.navigate(Registration)}
				>
					<Text>Registration</Text>
				</StyledPressable>

				{`

`}
				<Text onPress={() => navigation.navigate(Login)}>Login</Text>
				{`

`}
				<Text onPress={() => navigation.navigate(Dashboard)}>Dashboard</Text>
			</Text>
		</StyledView>
	);
};

export default Loading;
