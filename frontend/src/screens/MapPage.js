import {View, Text, Image, StyleSheet, TouchableOpacity} from 'react-native'
import React from 'react'
import { SafeAreaView } from 'react-native-safe-area-context'
import {image, regButton, titleText, header, button} from '../theme/theme'
import { useNavigation } from '@react-navigation/native'
import WebView from "react-native-webview";

export default function WelcomeScreen() {
    const navigation = useNavigation();
        return (
            <SafeAreaView>
                <View>
                    <View style={header}>
                        <Image style={image} source={require('../../assets/images/logo.png')}></Image>
                        <TouchableOpacity style={regButton} onPress={() => navigation.navigate('SignUp')}>
                            <Text style={styles.text}>Регистрация</Text>
                        </TouchableOpacity>
                    </View>
                    <Text style={titleText}>
                        Карта экологических нарушений Богудонии.
                    </Text>
                    <View style={{
                        alignItems: 'center',
                        justifyContent: 'center',
                    }}>
                        <TouchableOpacity style={styles.button} onPress={() => navigation.navigate('MapTest')}>
                            <Text style={styles.text}>Перейти к карте</Text>
                        </TouchableOpacity>
                    </View>
                </View>
            </SafeAreaView>
        )
    }

    const styles = StyleSheet.create({
        text: {
            color: '#000000',
            fontSize: 15,
            padding: 10,
            fontWeight: 'bold',
            letterSpacing: 0.25,
        },

        map: {
            height: 'auto',
            width: 'auto',
            marginVertical: 20,
        },

        button: {
            backgroundColor: "#69BFE3",
            borderRadius: 15,
            alignItems: 'center',
            width: 150,
            marginTop: 15,
            display: 'block',
            margin: 'auto',
        },

    })