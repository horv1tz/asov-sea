import {View, Text, TouchableOpacity, Image, Pressable, StyleSheet} from 'react-native'
import React from 'react'
import {card, image, header, avatar, infoTroublesText, infoMoreText} from '../theme/theme'
import { SafeAreaView } from 'react-native-safe-area-context'
import { useNavigation } from '@react-navigation/native';
import { titleText } from "../theme/theme";

export default function SignUpScreen() {
    const navigation = useNavigation();
    return (
        <View>
            <SafeAreaView>
                <View style={header}>
                    <TouchableOpacity onPress={()=> navigation.navigate('Map')}>
                        <Image style={image} source={require('../../assets/images/logo.png')}></Image>
                    </TouchableOpacity>
                    <TouchableOpacity onPress={()=> navigation.navigate('PrivateProfile')}>
                        <Image style={image} source={require('../../assets/images/avatar.png')}></Image>
                    </TouchableOpacity>
                </View>
                <View>
                    <Text style={titleText}>Детали проблемы</Text>
                </View>
            </SafeAreaView>
            <View>
                <Text style={styles.textInfo}>Номер жалобы:</Text><Text style={styles.text}>2117</Text>
                <Text style={styles.textInfo}>Название:</Text><Text style={styles.text}>Незаконная свалка АО "Ямалэкосервис"</Text>
                <Text style={styles.textInfo}>Описание:</Text><Text style={styles.text}>Полигон АО "Ямалэкосервис" работает без лицензии.</Text>
                <Text style={styles.textInfo}>Категория:</Text><Text style={styles.text}>Свалки</Text>
                <Text style={styles.textInfo}>Широта:</Text><Text style={styles.text}>63.891018</Text>
                <Text style={styles.textInfo}>Долгота:</Text><Text style={styles.text}>40.869120</Text>
                <Text style={styles.textInfo}>Статус решения:</Text><Text style={styles.text}>Не решено/В процессе/Решено</Text>
                <Text style={styles.textInfo}>Дата:</Text><Text style={styles.text}>2023-11-17</Text>
                <Text style={styles.textInfo}>Фото:</Text>
                <Image style={styles.photoTrouble} source={require('../../assets/images/photoTrouble.png')}></Image>
            </View>
        </View>
    )
}

const styles = StyleSheet.create({
    photoTrouble: {
        width: '100%'
    },

    textInfo: {
        marginTop: 4,
        fontSize: 22,
        fontWeight: 'bold',
    },

    text: {
        fontSize: 19,
    }
})