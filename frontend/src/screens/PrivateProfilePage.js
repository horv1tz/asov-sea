import {View, Text, TouchableOpacity, Image, TextInput, StyleSheet} from 'react-native'
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
                <View style={styles.rowImages}>
                    <Image style={avatar} source={require('../../assets/images/avatar.png')}></Image>
                    <TouchableOpacity style={styles.avatarChange}>
                        <Image style={styles.avatarChange} source={require('../../assets/images/changeAvatar.png')}></Image>
                    </TouchableOpacity>
                </View>
                <View>
                    <Text style={styles.text}>Имя пользователя:</Text><Text style={{fontSize: 22}}>Владимир Путин</Text>
                    <Text style={styles.text}>Роль:</Text><Text style={{fontSize: 22}}>Активист/Пользователь/Админ</Text>
                    <Text style={styles.text}>Решенные проблемы:</Text>
                    <TouchableOpacity style={infoTroublesText} onPress={()=> navigation.navigate('TroubleInfo')}>
                        <Text style={styles.textLink}>Незаконная свалка АО "Ямалэкосервис" </Text>
                    </TouchableOpacity>
                    <TouchableOpacity style={infoTroublesText}>
                        <Text style={styles.textLink}>Свалка на Забалканском пр-де</Text>
                    </TouchableOpacity>
                    <TouchableOpacity style={infoTroublesText}>
                        <Text style={styles.textLink}>Перегруз отходов на Московском шоссе</Text>
                    </TouchableOpacity>
                    <TouchableOpacity style={infoMoreText}>
                        <Text style={styles.textLinkMore}>Больше решенных проблем</Text>
                    </TouchableOpacity>
                </View>
            </View>
        </View>
    )
}

const styles = StyleSheet.create({
    text: {
        fontSize: 22,
        marginTop: 7,
        fontWeight: 'bold',
    },

    textLink: {
        fontSize: 22,
        textDecorationLine: 'underline',
    },

    textLinkMore: {
        fontSize: 25,
        textDecorationLine: 'underline',
        fontWeight: 'bold'
    },

    avatarChange: {
        width: 20,
        height: 20,
        alignSelf: 'flex-end'
    },

    rowImages: {
        justifyContent: 'space-between',
        flexDirection: 'row',
        margin: 'auto'
    }
})