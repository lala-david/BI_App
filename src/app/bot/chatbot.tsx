import * as React from 'react';
import { WebView } from 'react-native-webview';

const Chatbot: React.FC = () => {
  return (
    <WebView source={{ uri: 'http://..' }} style={{ marginTop: 20 }} />
  );
};
export default Chatbot;