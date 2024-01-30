import React, { useEffect }  from "react";
import { useTranslation } from "react-i18next";
import { Text, View, ActivityIndicator } from "react-native";
import { styled } from "nativewind";

const StyledView = styled(View);
const StyledActivityIndicator = styled(ActivityIndicator);
const StyledText = styled(Text);

const Loading = (props: any) => {
	const { navigation } = props;

	const { t } = useTranslation();

	const navigateAndReset = () => {
		navigation.reset({
		  index: 0,
		  routes: [{ name: 'HomeBottomTabs' }],
		});
	  }

	  //! This is a temporary solution while we do not have any checks for the user being logged in or not
	  useEffect(() => {
		setTimeout(() => {
		  navigateAndReset();
		}, 2000);
	  }, []);

	return (
		<StyledView className={`flex h-screen items-center justify-center bg-primary`}>
			<StyledActivityIndicator size="large" />
			<StyledText className={`text-font_primary font-bold p-5`}>Loading...</StyledText>
		</StyledView>
	);
};

export default Loading;
