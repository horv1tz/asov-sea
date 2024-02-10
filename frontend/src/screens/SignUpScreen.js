import {View, Text, TouchableOpacity, Image, TextInput, StyleSheet} from 'react-native'
import React from 'react'
import { themeColors } from '../../theme'
import { SafeAreaView } from 'react-native-safe-area-context'
import {ArrowLeftIcon} from 'react-native-heroicons/solid';
import { useNavigation } from '@react-navigation/native';

export default function SignUpScreen() {
    const navigation = useNavigation();
  return (
    <View style={{backgroundColor: themeColors.background}}>
      <SafeAreaView>
          <View style={styles.header}>
              <Image style={styles.image} source={require('../../assets/images/logo.png')}></Image>
          </View>
        <View>
            <TouchableOpacity 
                onPress={()=> navigation.goBack()}>
                <ArrowLeftIcon size="20" color="black" />
            </TouchableOpacity>
        </View>
        <View>
            <Image source={require('../../assets/images/signup.png')}
                style={{width: 165, height: 110}} />
        </View>
      </SafeAreaView>
      <View
        style={{borderTopLeftRadius: 50, borderTopRightRadius: 50}}>
        <View>
            <Text>Full Name</Text>
            <TextInput
                value="john snow"
                placeholder='Enter Name'
            />
            <Text>Email Address</Text>
            <TextInput
                value="john@gmail.com"
                placeholder='Enter Email'
            />
            <Text>Password</Text>
            <TextInput
                secureTextEntry
                value="test12345"
                placeholder='Enter Password'
            />
            <TouchableOpacity>
                <Text>
                    Sign Up
                </Text>
            </TouchableOpacity>
        </View>
        <Text>
            Or
        </Text>
        <View>
            <TouchableOpacity>
                <Image source={require('../../assets/icons/google.png')}/>
            </TouchableOpacity>
            <TouchableOpacity>
                <Image source={require('../../assets/icons/apple.png')}/>
            </TouchableOpacity>
            <TouchableOpacity>
                <Image source={require('../../assets/icons/facebook.png')}/>
            </TouchableOpacity>
        </View>
        <View>
            <Text>Already have an account?</Text>
            <TouchableOpacity onPress={()=> navigation.navigate('Login')}>
                <Text> Login</Text>
            </TouchableOpacity>
        </View>
      </View>
    </View>
  )
}

const styles = StyleSheet.create({
    image: {
        width: 50,
        height: 50,
        margin: 'auto',
    },

    header: {
        backgroundColor: themeColors.backgroundHeaderFooter
    }
})
