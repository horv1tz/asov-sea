import {View, Text, TouchableOpacity, Image, TextInput, StyleSheet} from 'react-native'
import React, {useState} from 'react'
import {button, card, input} from '../theme/theme'
import { SafeAreaView } from 'react-native-safe-area-context'
import {ArrowLeftIcon} from 'react-native-heroicons/solid';
import { useNavigation } from '@react-navigation/native';
import { titleText } from "../theme/theme";

export default function SignUpScreen() {
    const navigation = useNavigation();
    return (
        <View>
            <SafeAreaView>
                <View>
                    <TouchableOpacity
                        onPress={()=> navigation.goBack()}>
                        <ArrowLeftIcon size="20" color="black" />
                    </TouchableOpacity>
                </View>
                <View>
                    <Text style={titleText}>Зарегистрируйте свой аккаунт</Text>
                </View>
            </SafeAreaView>
            <View
                style={card}>
                <View>
                    <TextInput
                        style={input}
                        placeholder='Имя'
                    />
                    <TextInput
                        style={input}
                        placeholder='Фамилия'
                    />
                    <TextInput
                        style={input}
                        placeholder='E-mail'
                    />
                    <TextInput
                        style={input}
                        secureTextEntry
                        placeholder='Пароль'
                    />
                    <TouchableOpacity style={button} onPress={()=> navigation.navigate('PrivateProfile')}>
                        <Text>
                            Регистрация
                        </Text>
                    </TouchableOpacity>
                </View>
                <Text style={{marginTop: 15, fontWeight: 700}}>
                    или
                </Text>
                <View>
                    <TouchableOpacity>
                        <Image source={require('../../assets/icons/google.png')} style={{width: 50, height: 50}}/>
                    </TouchableOpacity>
                </View>
                <View>
                    <Text style={{textAlign: 'center', marginTop: 15, fontSize: 15}}>Уже есть аккаунт?</Text>
                    <TouchableOpacity  style={button} onPress={()=> navigation.navigate('Login')}>
                        <Text>Войти</Text>
                    </TouchableOpacity>
                </View>
            </View>
        </View>
    )
}