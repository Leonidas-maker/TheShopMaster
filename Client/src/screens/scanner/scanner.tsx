import React, { useState, useEffect, useCallback } from 'react';
import { Text, View, StyleSheet, Alert } from 'react-native';
import { Camera } from 'expo-camera';
import { BarCodeScanner, BarCodeScannerResult } from 'expo-barcode-scanner';
import { useTranslation } from 'react-i18next';
import { useFocusEffect } from '@react-navigation/native';
import { styled } from 'nativewind';
import ScannerInfoPopup from '../../components/popups/scannerInfoPopup';
import { usePopup } from '../../context/scannerInfoPopupContext';

//TODO: Add logic to scan barcode and get product from database
function Scanner() {
    const { t } = useTranslation();
    const [cameraPermission, requestPermission] = Camera.useCameraPermissions();
    const [scanned, setScanned] = useState(false);
    const [isCameraActive, setIsCameraActive] = useState(true);

    const StyledView = styled(View);
    const StyledText = styled(Text);

    const { isPopupVisible, setPopupVisible } = usePopup();

    //Requests permission to use camera
    useEffect(() => {
        (async () => {
            if (!cameraPermission || cameraPermission.status === 'undetermined') {
                await requestPermission();
            }
            setIsCameraActive(true);
        })();

        return () => {
            setIsCameraActive(false);
        };
    }, [cameraPermission]);

    //Deactivates camera when screen is not focused and vice versa
    useFocusEffect(
        useCallback(() => {
            setIsCameraActive(true);

            return () => {
                setIsCameraActive(false);
            };
        }, [])
    );

    //Deactivates camera when popup is visible and vice versa
    useEffect(() => {
        if (isPopupVisible) {
            setIsCameraActive(false);
        } else {
            setIsCameraActive(true);
        }
    }, [isPopupVisible]);

    //Defines what happens when a barcode is scanned
    const handleBarCodeScanned = ({ type, data }: BarCodeScannerResult) => {
        setScanned(true);
        Alert.alert(
            "Barcode gescannt",
            `Typ: ${type}\nDaten: ${data}`,
            [
                {
                    text: "OK",
                    onPress: () => setScanned(false)
                }
            ]
        );
    };

    if (!cameraPermission) {
        //Permission request has not been resolved yet
        return <StyledView />;
    }

    if (!cameraPermission.granted) {
        //No access to camera
        return (
            <StyledView className={`h-full item-center justify-center`}>
                <StyledText className={`font-bold text-2xl`}>
                    Kein Zugriff auf die Kamera
                </StyledText>
            </StyledView>
        );
    }

    //Camera styling
    //Defines which barcode types are scannable (EAN-13, QR, EAN-8)
    //Defines that handleBarCodeScanned is called when a barcode is scanned
    return (
        <StyledView className={`h-full`}>
            <ScannerInfoPopup visible={isPopupVisible} onClose={() => setPopupVisible(false)} />
            {
                (() => {
                    if (isCameraActive) {
                        //Camera is active
                        return (
                            <StyledView className={`h-full item-center justify-center`}>
                                <BarCodeScanner
                                    onBarCodeScanned={scanned ? undefined : handleBarCodeScanned}
                                    barCodeTypes={[BarCodeScanner.Constants.BarCodeType.ean13,
                                    BarCodeScanner.Constants.BarCodeType.ean8]}
                                    style={StyleSheet.absoluteFillObject}
                                />
                                <StyledView className={`grid grid-rows-3 grid-flow-col`}>
                                    <StyledView className={`bg-black opacity-50 w-full h-1/3`} />
                                    <StyledView className={`w-full h-1/3`}>
                                        <StyledView className={`absolute top-0 left-0 w-10 h-0 border-b-4 border-r-4 border-white`} />
                                        <StyledView className={`absolute top-0 left-0 w-0 h-10 border-b-4 border-r-4 border-white`} />
                                        <StyledView className={`absolute top-0 right-0 w-10 h-0 border-b-4 border-l-4 border-white`} />
                                        <StyledView className={`absolute top-0 right-0 w-0 h-10 border-b-4 border-l-4 border-white`} />
                                        <StyledView className={`absolute bottom-0 left-0 w-10 h-0 border-t-4 border-r-4 border-white`} />
                                        <StyledView className={`absolute bottom-0 left-0 w-0 h-10 border-t-4 border-r-4 border-white`} />
                                        <StyledView className={`absolute bottom-0 right-0 w-10 h-0 border-t-4 border-l-4 border-white`} />
                                        <StyledView className={`absolute bottom-0 right-0 w-0 h-10 border-t-4 border-l-4 border-white`} />
                                    </StyledView>
                                    <StyledView className={`bg-black opacity-50 w-full h-1/3`} />
                                </StyledView>
                            </StyledView>
                        );
                    } else if (!isCameraActive && isPopupVisible) {
                        return (
                            <StyledView className={`h-full item-center justify-center bg-gray-800`} />
                        );
                    } else {
                        //Camera is not active
                        return (
                            <StyledView className={`h-full item-center justify-center`}>
                                <StyledText className={`text-2xl`}>Kamera deaktiviert</StyledText>
                            </StyledView>
                        );
                    }
                })()
            }
            
        </StyledView>
    );
}

export default Scanner;