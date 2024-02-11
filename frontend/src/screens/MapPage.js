import {View, Text, Image, StyleSheet, TouchableOpacity} from 'react-native'
import React from 'react'
import { SafeAreaView } from 'react-native-safe-area-context'
import {image, regButton, titleText, header} from '../theme/theme'
import { useNavigation } from '@react-navigation/native'
import MapboxGL from '@react-native-mapbox-gl/maps';

export default function WelcomeScreen() {
    const navigation = useNavigation();

    return (
        <SafeAreaView>
            <View>
                <View style={header}>
                    <Image style={image} source={require('../../assets/images/logo.png')}></Image>
                    <TouchableOpacity style={regButton} onPress={()=> navigation.navigate('SignUp')}>
                        <Text style={styles.text}>Регистрация</Text>
                    </TouchableOpacity>
                </View>
                <Text style={titleText}>
                    Карта экологических нарушений Богудонии.
                </Text>
                <View style={{flex: 1, justifyContent: 'center', alignItems: 'center'}}>
                    <MapboxGL.MapView style={{ flex: 1 }}>
                        <MapboxGL.Camera zoomLevel={10} centerCoordinate={[11.256, 43.770]} />
                    </MapboxGL.MapView>
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
        flex: 1,
        width: '100%',
        height: '100%',
    }
})