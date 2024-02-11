import React from 'react';
import { StyleSheet, View } from 'react-native';
import WebView from 'react-native-webview';

const MyMapComponent = () => (
    <View style={styles.container}>
        <WebView
            source={{ uri: 'https://www.openstreetmap.org' }}
            style={styles.webview}
        />
    </View>
);

const styles = StyleSheet.create({
    container: {
        flex: 1,
        marginTop: 20,
    },
    webview: {
        flex: 1,
    },
});

export default MyMapComponent;