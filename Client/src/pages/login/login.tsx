import React from "react";
import { useTranslation } from "react-i18next";
import { Text, View, Pressable, ActivityIndicator, StyleSheet } from "react-native";
import { styled, useColorScheme } from "nativewind";

import Dashboard from "../dashboard/dashboard";

const StyledPressable = styled(Pressable);
const StyledView = styled(View);
const StyledActivityIndicator = styled(ActivityIndicator);
const StyledText = styled(Text);

function Login(props: any) {
    const { navigation } = props;

    const { t } = useTranslation();

	const { colorScheme, toggleColorScheme } = useColorScheme();

    return (
		<StyledView className={`flex h-screen items-center justify-center`}>
			<StyledText className={`text-black font-bold text-lg p-5`}>This is just a debug page at the moment</StyledText>
			<StyledActivityIndicator className={`content-center`} size="large" />
			<StyledText className={`text-black font-bold p-5`}>Loading...</StyledText>
			<StyledPressable
				onPress={toggleColorScheme}
				className={`${colorScheme === 'dark' ? 'bg-slate-800' : 'bg-gray-800'}`}
			>
				<StyledText
				selectable={false}
				className={`${colorScheme === 'dark' ? 'text-white' : 'text-black'}`}
				>
				{`Try clicking me! ${colorScheme === "dark" ? "🌙" : "🌞"}`}
				</StyledText>
			</StyledPressable>
			<StyledPressable className={`font-bold text-white bg-red-500 rounded-md p-2`}>
						<Text>New Stack</Text>
					</StyledPressable>
			<Text>
				{`Loading...
This will be the initial page where the app checks if you are already logged in or not
This is just a menu to test some basic functions: 

`}
				<StyledPressable
					className={`font-bold text-white bg-blue-500 rounded-md p-2`}
					onPress={() => navigation.navigate(Dashboard)}
				>
					<Text>Registration</Text>
				</StyledPressable>

				{`

`}
				<Text onPress={() => navigation.navigate(Dashboard)}>Login</Text>
				{`

`}
				<Text onPress={() => navigation.navigate(Dashboard)}>Dashboard</Text>
			</Text>
		</StyledView>
	);
}

export default Login;