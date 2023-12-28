import React from "react";
import { TextInput } from "react-native";
import { styled } from "nativewind";
import { useTranslation } from "react-i18next";

const StyledTextInput = styled(TextInput);

function PasswordInput() {
    const { t } = useTranslation();

  return (
    <StyledTextInput 
		className={`border-2 border-gray-400 rounded-md p-3 text-xl text-white mt-5`}
		placeholder="Passwort"
		placeholderTextColor={'#FFFFFF'}
	    secureTextEntry={true}
	/>
  );
}

export default PasswordInput;