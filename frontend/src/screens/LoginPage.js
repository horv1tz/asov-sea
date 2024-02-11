import { View, Text, TouchableOpacity, TextInput } from 'react-native'
import React, {useState} from 'react'
import { SafeAreaView } from 'react-native-safe-area-context'
import {button, card, input, titleText} from '../theme/theme'
import {ArrowLeftIcon} from 'react-native-heroicons/solid'
import { useNavigation } from '@react-navigation/native'

export default function LoginScreen() {
    const navigation = useNavigation();
    return (
        <View>
            <SafeAreaView>
                <View>
                    <TouchableOpacity onPress={()=> navigation.goBack()}>
                        <ArrowLeftIcon size="20" color="black" />
                    </TouchableOpacity>
                </View>
                <View>
                    <Text style={titleText}>Войдите в свой аккаунт</Text>
                </View>
            </SafeAreaView>
            <View
                style={card}>
                <View>
                    <TextInput
                        style={input}
                        placeholder='E-mail'
                    />
                    <TextInput
                        style={input}
                        secureTextEntry
                        placeholder='Пароль'
                    />
                    <TouchableOpacity>
                        <Text style={button}>
                            Войти
                        </Text>
                    </TouchableOpacity>

                </View>
                <View>
                    <Text style={{textAlign: 'center', marginTop: 10}}>
                        Ещё нет аккаунта?
                    </Text>
                    <TouchableOpacity style={button} onPress={()=> navigation.navigate('SignUp')}>
                        <Text>Регистрация</Text>
                    </TouchableOpacity>
                </View>
            </View>
        </View>

    )
}