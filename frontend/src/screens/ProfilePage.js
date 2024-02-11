import {View, Text, TouchableOpacity, Image, StyleSheet} from 'react-native'
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
                </View>
                <View>
                    <Text style={titleText}>Профиль</Text>
                </View>
            </SafeAreaView>
            <View
                style={card}>
                <View>
                    <Image style={avatar} source={require('../../assets/images/avatar.png')}></Image>
                    <Text style={styles.text}>Имя пользователя: Владимир Путин</Text>
                    <Text style={styles.text}>Роль: Активист/Пользователь/Админ</Text>
                    <Text style={styles.text}>Решенные проблемы:</Text>
                    <TouchableOpacity style={infoTroublesText}><Text>Незаконная свалка АО "Ямалэкосервис"</Text></TouchableOpacity>
                    <TouchableOpacity style={infoTroublesText}><Text>Свалка на Забалканском пр-де</Text></TouchableOpacity>
                    <TouchableOpacity style={infoTroublesText}><Text>Перегруз отходов на Московском шоссе</Text></TouchableOpacity>
                    <TouchableOpacity style={infoMoreText}><Text>Больше</Text></TouchableOpacity>
                </View>
            </View>
        </View>
    )
}

const styles = StyleSheet.create({
    text: {
        marginLeft: 2,
        marginTop: 10,
    },
})