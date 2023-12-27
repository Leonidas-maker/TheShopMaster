import React from "react";
import { useTranslation } from "react-i18next";
import { Text, View, TextInput } from "react-native";
import { styled } from "nativewind";

const StyledText = styled(Text);
const StyledView = styled(View);
const StyledTextInput = styled(TextInput);

function Login() {

    const { t } = useTranslation();

    return (
        <StyledView>
            <StyledText>Welcome to the Registration page</StyledText>
			<StyledTextInput 
				className={`border-2 border-gray-800 rounded-md p-2`}
				placeholder="Username"
				placeholderTextColor={'#000000'}
			/>
        </StyledView>
    );
}

export default Login;