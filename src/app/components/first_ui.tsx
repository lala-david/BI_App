import React from 'react';
import {
  View,
  Text,
  ImageBackground,
  SafeAreaView,
  ScrollView,
  TouchableOpacity,
} from 'react-native';
import { NativeStackScreenProps } from '@react-navigation/native-stack';
import first from '../style/first_ui_style';
import { RootStackParamList } from '../types';

type FirstUIProps = NativeStackScreenProps<RootStackParamList, 'FirstUI'>;

const FirstUI: React.FC<FirstUIProps> = ({ navigation }) => {
  return (
    <SafeAreaView>
      <ScrollView
        scrollEnabled={true}
        contentInsetAdjustmentBehavior='automatic'
      >
        <View style={first.container}>
          <Text style={first.headerText} numberOfLines={1}>
            Blockchain Intelligence
          </Text>
          <ImageBackground
            style={first.firstImage}
            source={require('../assets/first.png')}
            resizeMode='cover'
          />
          <Text style={first.welcomeText}>
            Welcome{'\n'}BI Lab!
          </Text>
          <ImageBackground
            style={first.robotImage}
            source={require('../assets/robot_fi.png')}
            resizeMode='cover'
          />
          <TouchableOpacity onPress={() => navigation.navigate('Loading')}>
            <ImageBackground
              style={first.startImage}
              source={require('../assets/start.png')}
              resizeMode='cover'
            >
              <Text style={first.startText} numberOfLines={1}>
                Start
              </Text>
            </ImageBackground>
          </TouchableOpacity>
          <ImageBackground
            style={first.powerImage}
            source={require('../assets/power.png')}
            resizeMode='cover'
          />
        </View>
      </ScrollView>
    </SafeAreaView>
  );
};

export default FirstUI;
