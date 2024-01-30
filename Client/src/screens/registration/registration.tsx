import React from "react";
import { useTranslation } from "react-i18next";
import { Text, View, TextInput, TouchableHighlight } from "react-native";
import { styled } from "nativewind";
import { useNavigation } from "@react-navigation/native";
import Login from "../login/login";

const StyledText = styled(Text);
const StyledView = styled(View);
const StyledTextInput = styled(TextInput);
const StyledTouchableHighlight = styled(TouchableHighlight);

//TODO: Make own component for text input
//!: Not final design - just for testing the registration function
function Registration(props: any) {
    const { t } = useTranslation();

    const { navigation } = props;

	const handlePress = () => {
		console.log("Register pressed");
	}

    return (
        <StyledView className={`bg-primary h-screen`}>
			<StyledView className={`w-max items-center mb-5 mt-5`}>
            	<StyledText className={`text-font_primary font-bold text-4xl`}>Registrieren</StyledText>
			</StyledView>
			<StyledView className={`mx-10`}>
                <StyledTextInput 
                    className={`border-2 border-gray-400 rounded-md p-3 text-xl text-white`}
                    placeholder="Benutzername"
                    placeholderTextColor={'#FFFFFF'}
                />
                <StyledTextInput 
                    className={`border-2 border-gray-400 rounded-md p-3 text-xl text-white mt-5`}
                    placeholder="E-Mail Adresse"
                    placeholderTextColor={'#FFFFFF'}
                />
				<StyledTextInput 
                    className={`border-2 border-gray-400 rounded-md p-3 text-xl text-white mt-5`}
                    placeholder="Passwort"
                    placeholderTextColor={'#FFFFFF'}
                    secureTextEntry={true}
                />
                <StyledTextInput 
                    className={`border-2 border-gray-400 rounded-md p-3 text-xl text-white mt-5`}
                    placeholder="Passwort wiederholen"
                    placeholderTextColor={'#FFFFFF'}
                    secureTextEntry={true}
                />
                <StyledTextInput 
                    className={`border-2 border-gray-400 rounded-md p-3 text-xl text-white mt-5`}
                    placeholder="Adresse (optional)"
                    placeholderTextColor={'#FFFFFF'}
                />
			</StyledView>
			<StyledTouchableHighlight
				onPress={handlePress}
				className={`rounded-md p-3 mt-5 items-center justify-center mx-10 bg-red-500`}
				underlayColor={'red'}
			>
				<StyledView>
					<StyledText className={`text-white font-bold text-2xl`}>Registrieren</StyledText>
				</StyledView>
			</StyledTouchableHighlight>
            <StyledTouchableHighlight
				onPress={() => navigation.navigate(Login)}
				className={`rounded-md p-3 mt-5 items-center justify-center mx-10 bg-green-500`}
				underlayColor={'green'}
			>
				<StyledView>
					<StyledText className={`text-white font-bold text-2xl`}>Bereits ein Account?</StyledText>
				</StyledView>
			</StyledTouchableHighlight>
        </StyledView>
    );
}

export default Registration;