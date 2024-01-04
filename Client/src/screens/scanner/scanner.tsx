import React, { useState, useEffect } from 'react';
import { Text, View, StyleSheet, Alert } from 'react-native';
import { Camera } from 'expo-camera';
import { BarCodeScanner, BarCodeScannerResult } from 'expo-barcode-scanner';
import { useTranslation } from 'react-i18next';

//TODO: Add logic to scan barcode and get product from database
//TODO: Unmount camera after switching to another screen
function Scanner() {
    const { t } = useTranslation();
    const [cameraPermission, requestPermission] = Camera.useCameraPermissions();
    const [scanned, setScanned] = useState(false);

    useEffect(() => {
        (async () => {
            if (!cameraPermission || cameraPermission.status === 'undetermined') {
                await requestPermission();
            }
        })();
    }, [cameraPermission]);

    const handleBarCodeScanned = ({ type, data }: BarCodeScannerResult) => {
        setScanned(true);
        Alert.alert(
            "Barcode Scanned",
            `Type: ${type}\nData: ${data}`,
            [
                {
                    text: "OK",
                    onPress: () => setScanned(false)
                }
            ]
        );
    };

    if (!cameraPermission) {
        // Permission request has not been resolved yet
        return <View />;
    }

    if (!cameraPermission.granted) {
        // No access to camera
        return <Text>No access to camera</Text>;
    }

    return (
        <View style={styles.container}>
            <BarCodeScanner
                onBarCodeScanned={scanned ? undefined : handleBarCodeScanned}
                style={StyleSheet.absoluteFillObject}
            />
        </View>
    );
}

const styles = StyleSheet.create({
    container: {
        flex: 1,
        justifyContent: 'center',
        alignItems: 'center',
    },
});

export default Scanner;