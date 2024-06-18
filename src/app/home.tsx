import React from 'react';
import {
  View,
  Text,
  ImageBackground,
  TouchableOpacity,
  SafeAreaView,
  ScrollView,
} from 'react-native';
import { NativeStackScreenProps } from '@react-navigation/native-stack';
import styles from './style/home_style';
import { RootStackParamList } from './types';

type HomeProps = NativeStackScreenProps<RootStackParamList, 'Home'>;

const Home: React.FC<HomeProps> = ({ navigation }) => {
  return (
    <SafeAreaView>
      <ScrollView
        scrollEnabled={true}
        contentInsetAdjustmentBehavior='automatic'
      >
        <View style={styles.container}>
          <View style={styles.header}>
            <Text style={styles.headerText} numberOfLines={1}>
              BI Lab
            </Text>
            <ImageBackground
              style={styles.profileImage}
              source={require('./assets/profile.png')}
              resizeMode='cover'
            />
          </View>
          <View style={styles.newsSection}>
            <Text style={styles.newsTitle} numberOfLines={1}>
              BI Lab News
            </Text>
            <Text style={styles.newsSubtitle} numberOfLines={1}>
              ☄ Supernova
            </Text>
          </View>
          <ImageBackground
            style={styles.backgroundImage}
            source={require('./assets/background.png')}
            resizeMode='cover'
          >
            <Text style={styles.backgroundText} numberOfLines={1}>
              2024 smmr JEJU
            </Text>
          </ImageBackground>
          <View style={styles.serviceSection}>
            <Text style={styles.serviceTitle} numberOfLines={1}>
              BI Service
            </Text>
            <Text style={styles.serviceSubtitle} numberOfLines={1}>
              BI LAB is the best
            </Text>
          </View>
          <View style={styles.iconRow}>
            <TouchableOpacity
              onPress={() => navigation.navigate('WebApp')}
            >
              <ImageBackground
                style={styles.iconImage}
                source={require('./assets/chatbot.png')}
                resizeMode='cover'
              />
              <View style={styles.iconTextContainer}>
                <Text style={styles.iconText}>Bivis chatbot</Text>
              </View>
            </TouchableOpacity>
            <TouchableOpacity
              onPress={() => navigation.navigate('IotInfo')}
            >
              <ImageBackground
                style={styles.iconImage}
                source={require('./assets/iot.png')}
                resizeMode='cover'
              />
              <View style={styles.iconTextContainer}>
                <Text style={styles.iconText} numberOfLines={1}>
                  IoT Graph
                </Text>
              </View>
            </TouchableOpacity>
          </View>
          <View style={styles.iconRow}>
          <TouchableOpacity
              onPress={() => navigation.navigate('LabCCTV')}  
            >
              <ImageBackground
                style={styles.iconImage}
                source={require('./assets/cctv.png')}
                resizeMode='cover'
              />
              <View style={styles.iconTextContainer}>
                <Text style={styles.iconText}>Lab CCTV</Text>
              </View>
            </TouchableOpacity>

            <TouchableOpacity
              onPress={() => navigation.navigate('LabInfo')}
            >
              <ImageBackground
                style={styles.iconImage}
                source={require('./assets/member.png')}
                resizeMode='cover'
              />
              <View style={styles.iconTextContainer}>
                <Text style={styles.iconText}>Member</Text>
              </View>
            </TouchableOpacity>
          </View>
        </View>
      </ScrollView>
    </SafeAreaView>
  );
};

export default Home;
