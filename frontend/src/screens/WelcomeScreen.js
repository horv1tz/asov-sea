import {View, Text, Image, StyleSheet, Pressable} from 'react-native'
import React from 'react'
import { SafeAreaView } from 'react-native-safe-area-context'
import { themeColors } from '../../theme'
import { useNavigation } from '@react-navigation/native'
import { YaMap, Marker } from 'react-native-yamap'

YaMap.init('dc9b5d8a-64f0-4562-8fa4-426d801cff54');

export default function WelcomeScreen() {
    const navigation = useNavigation();
  return (
    <SafeAreaView style={{backgroundColor: themeColors.background}}>
        <View>
            <View style={styles.header}>
                <Image style={styles.image} source={require('../../assets/images/logo.png')}></Image>
                <Pressable style={styles.button} onPress={()=> navigation.navigate('SignUp')}>
                    <Text style={styles.text}>Регистрация</Text>
                </Pressable>
            </View>
            <Text style={styles.title}>
                Карта экологических нарушений Богудонии.
            </Text>
            <View>
                <YaMap style={styles.map}></YaMap>
            </View>
        </View>
    </SafeAreaView>
  )
}

const styles = StyleSheet.create({
    image: {
        width: 50,
        height: 50,
        left: 10,
    },

    header: {
        justifyContent: 'space-between',
        flexDirection: 'row',
        alignItems: 'center',
        backgroundColor: themeColors.backgroundHeaderFooter,
    },

    button: {
        borderRadius: 15,
        backgroundColor: "#FFFFFF",
        alignItems: 'center',
        width: 50,
        shadowColor: '#000',
        shadowOffset: {width: 0, height: 2},
        shadowOpacity: 0.25,
        shadowRadius: 3.84,
    },

    text: {
        color: '#000000',
        fontSize: 7,
        lineHeight: 21,
        fontWeight: 'bold',
        letterSpacing: 0.25,
    },

    title: {
        textAlign: 'center',
        fontFamily: 'Arial',
        fontWeight: 700,
        marginTop: 15,
    },

    map: {
        width: 100,
        height: 100,
    }
})