import * as React from 'react';
import { WebView } from 'react-native-webview';
import { NativeStackScreenProps } from '@react-navigation/native-stack';
import { RootStackParamList } from '../types';

type LabInfoProps = NativeStackScreenProps<RootStackParamList, 'LabInfo'>;

const LabInfo: React.FC<LabInfoProps> = () => {
  return (
    <WebView source={{ uri: 'https://slime-death-220.notion.site/2e9cf85ca96242c99320ba5cc728a472' }} style={{ marginTop: 20 }} />
  );
};

export default LabInfo;
