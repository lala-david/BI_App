import React, { useState, useEffect } from 'react';
import { NavigationContainer } from '@react-navigation/native';
import { createNativeStackNavigator } from '@react-navigation/native-stack';
import * as Font from 'expo-font';
import Home from './home';
import FirstUI from './components/first_ui';
import Loading from './components/loading';
import Chatbot from './bot/chatbot';
import LabInfo from './page/lab_info';
import IotInfo from './page/iot_info'; 
import LabCCTV from './page/lab_cctv';
import { RootStackParamList } from './types';

const Stack = createNativeStackNavigator<RootStackParamList>();

const App: React.FC = () => {
  const [fontsLoaded, setFontsLoaded] = useState(false);

  const loadFonts = async () => {
    await Font.loadAsync({
      'Inter': require('./assets/fonts/Inter-Regular.ttf'), 
      'Inter-Bold': require('./assets/fonts/Inter-Bold.ttf'),  
    });
    setFontsLoaded(true);
  };

  useEffect(() => {
    loadFonts();
  }, []);

  return (
    <NavigationContainer>
      <Stack.Navigator initialRouteName="FirstUI">
        <Stack.Screen 
          name="FirstUI" 
          component={FirstUI} 
          options={{ headerShown: false }}  
        />
        <Stack.Screen 
          name="Loading" 
          component={Loading} 
          options={{ headerShown: false }}  
        />
        <Stack.Screen 
          name="Home" 
          component={Home} 
          options={{ headerShown: false }}  
        />
        <Stack.Screen 
          name="WebApp" 
          component={Chatbot} 
          options={{ headerShown: false }}  
        />
        <Stack.Screen 
          name="LabInfo" 
          component={LabInfo} 
          options={{ headerShown: false }}  
        />
        <Stack.Screen 
          name="IotInfo" 
          component={IotInfo} 
          options={{ headerShown: false }} 
        />
          <Stack.Screen 
          name="LabCCTV" 
          component={LabCCTV} 
          options={{ headerShown: false }} 
        />
      </Stack.Navigator>
    </NavigationContainer>
  );
};

export default App;
