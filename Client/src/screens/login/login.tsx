import React from "react";
import { useTranslation } from "react-i18next";
import { Text, View, TextInput, TouchableHighlight } from "react-native";
import { styled } from "nativewind";
import UsernameInput from "../../components/textInputs/usernameInput";
import PasswordInput from "../../components/textInputs/passwordInput";
import Registration from "../registration/registration";

const StyledText = styled(Text);
const StyledView = styled(View);
const StyledTextInput = styled(TextInput);
const StyledTouchableHighlight = styled(TouchableHighlight);

//TODO: Make own component for text input
//!: Not final design - just for testing the login function
function Login(props: any) {
    const { t } = useTranslation();

	const { navigation } = props;

	const handlePress = () => {
		console.log("Login pressed");
	}

    return (
        <StyledView className={`bg-primary h-screen`}>
			<StyledView className={`w-max items-center mb-5 mt-5`}>
            	<StyledText className={`text-font_primary font-bold text-4xl`}>Login</StyledText>
			</StyledView>
			<StyledView className={`mx-10`}>
				<UsernameInput />
				<PasswordInput />
			</StyledView>
			<StyledTouchableHighlight
				onPress={handlePress}
				className={`rounded-md p-3 mt-5 items-center justify-center mx-10 bg-red-500`}
				underlayColor={'red'}
				>
				<StyledView>
					<StyledText className={`text-white font-bold text-2xl`}>Login</StyledText>
				</StyledView>
			</StyledTouchableHighlight>
			<StyledTouchableHighlight
				onPress={() => navigation.navigate(Registration)}
				className={`rounded-md p-3 mt-5 items-center justify-center mx-10 bg-green-500`}
				underlayColor={'green'}
				>
				<StyledView>
					<StyledText className={`text-white font-bold text-2xl`}>Noch kein Account?</StyledText>
				</StyledView>
			</StyledTouchableHighlight>
        </StyledView>
    );
}

export default Login;