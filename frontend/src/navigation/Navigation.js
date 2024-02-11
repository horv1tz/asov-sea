import React from 'react'
import { NavigationContainer } from '@react-navigation/native';
import { createNativeStackNavigator } from '@react-navigation/native-stack';
import MapScreen from '../screens/MapPage';
import LoginScreen from '../screens/LoginPage';
import SignUpScreen from '../screens/SignUpPage';
import ProfileScreen from '../screens/ProfilePage';
import PrivateProfileScreen from '../screens/PrivateProfilePage'
import TroubleInfoScreen from '../screens/TroubleInfoPage'
import MapTest from '../screens/Map'

const Stack = createNativeStackNavigator();


export default function AppNavigation() {
    return (
        <NavigationContainer>
            <Stack.Navigator initialRouteName='Welcome'>
                <Stack.Screen name="Map" options={{headerShown: false}} component={MapScreen} />
                <Stack.Screen name="Login" options={{headerShown: false}} component={LoginScreen} />
                <Stack.Screen name="SignUp" options={{headerShown: false}} component={SignUpScreen} />
                <Stack.Screen name="Profile" options={{headerShown: false}} component={ProfileScreen} />
                <Stack.Screen name="PrivateProfile" options={{headerShown: false}} component={PrivateProfileScreen} />
                <Stack.Screen name="TroubleInfo" options={{headerShown: false}} component={TroubleInfoScreen} />
                <Stack.Screen name="MapTest" options={{headerShown: false}} component={MapTest} />
            </Stack.Navigator>
        </NavigationContainer>
    )
}