import React from "react";
import { useTranslation } from "react-i18next";
import { Text, View, TextInput, TouchableHighlight } from "react-native";
import { styled } from "nativewind";

const StyledText = styled(Text);
const StyledView = styled(View);
const StyledTextInput = styled(TextInput);
const StyledTouchableHighlight = styled(TouchableHighlight);

//TODO: Make own component for text input
//!: Not final design - just for testing the login function
function Login() {
    const { t } = useTranslation();

	const handlePress = () => {
		console.log("Login pressed");
	}

    return (
        <StyledView className={`bg-gray-800 h-screen`}>
			<StyledView className={`w-max items-center mb-5 mt-5`}>
            	<StyledText className={`text-white font-bold text-4xl`}>Login</StyledText>
			</StyledView>
			<StyledView className={`mx-10`}>
				<StyledTextInput 
					className={`border-2 border-gray-400 rounded-md p-3 text-xl text-white`}
					placeholder="Benutzername / E-Mail"
					placeholderTextColor={'#FFFFFF'}
				/>
				<StyledTextInput 
					className={`border-2 border-gray-400 rounded-md p-3 text-xl text-white mt-5`}
					placeholder="Passwort"
					placeholderTextColor={'#FFFFFF'}
					secureTextEntry={true}
				/>
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
        </StyledView>
    );
}

export default Login;