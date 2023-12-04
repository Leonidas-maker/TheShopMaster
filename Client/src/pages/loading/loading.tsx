import React from "react";
import { useTranslation } from "react-i18next";
import { Text, View, Pressable, Button } from "react-native";
import { styled, useColorScheme } from "nativewind";

import { StyledComponent } from "nativewind";

import Registration from '../registration/registration';
import Login from "../login/login";
import Dashboard from "../dashboard/dashboard";
import LoadingSVG from "../../components/svg/loadingSVG";

const StyledPressable = styled(Button)
const StyledText = styled(Text)

const Loading = (props:any) => {
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
<StyledPressable title="Registration" className="text-black font-bold" onPress={() => navigation.navigate(Registration)}></StyledPressable>

{`

`}
<Text onPress={() => navigation.navigate(Login)}>Login</Text>
{`

`}
<Text onPress={() => navigation.navigate(Dashboard)}>Dashboard</Text>
            </Text>
        </View>
    );
}

export default Loading;