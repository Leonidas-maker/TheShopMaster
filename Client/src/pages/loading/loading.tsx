import React from "react";
import { useTranslation } from "react-i18next";
import { Text, View, Pressable } from "react-native";
import { styled, useColorScheme } from "nativewind";

import { StyledComponent } from "nativewind";

import Registration from "../registration/registration";
import Login from "../login/login";
import Dashboard from "../dashboard/dashboard";
import LoadingSVG from "../../components/svg/loadingSVG";
import { RectButton } from "react-native-gesture-handler";

const StyledPressable = styled(Pressable);
const StyledText = styled(Text);

const Loading = (props: any) => {
	const { navigation } = props;

	const { t } = useTranslation();

	return (
		<View>
			<Text>
				{`Loading...
This will be the initial page where the app checks if you are already logged in or not
This is just a menu to test some basic functions: 

`}
				<LoadingSVG />
				<StyledPressable
					className={`font-bold text-white`}
					onPress={() => navigation.navigate(Registration)}
				>
					Registration
				</StyledPressable>

				{`

`}
				<Text onPress={() => navigation.navigate(Login)}>Login</Text>
				{`

`}
				<Text onPress={() => navigation.navigate(Dashboard)}>Dashboard</Text>
			</Text>
		</View>
	);
};

export default Loading;
