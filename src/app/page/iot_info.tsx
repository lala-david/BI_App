import React, { useEffect, useState } from 'react';
import { View, Text, ScrollView, StyleSheet, Dimensions } from 'react-native';
import { LineChart } from 'react-native-chart-kit';
import { NativeStackScreenProps } from '@react-navigation/native-stack';
import { RootStackParamList } from '../types';

const { width } = Dimensions.get('window');

type IotInfoProps = NativeStackScreenProps<RootStackParamList, 'IotInfo'>;

const IotInfo: React.FC<IotInfoProps> = ({ navigation }) => {
  const [data, setData] = useState<any[]>([]);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const jsonData = require('./polo/polo_data.json');
        const sanitizedData = jsonData.filter((item: any) => 
          isFinite(item.temperature) &&
          isFinite(item.humidity) &&
          isFinite(item.mq2_ppm) &&
          isFinite(item.mq7_ppm) &&
          isFinite(item.dust_density) &&
          isFinite(item.mq135_ppm)
        );
        setData(prevData => {
          const updatedData = [...prevData, ...sanitizedData];
          return updatedData.length > 6 ? updatedData.slice(-6) : updatedData;
        });
      } catch (error) {
        console.error('Error fetching data', error);
      }
    };

    fetchData();
    const interval = setInterval(fetchData, 3600000);
    return () => clearInterval(interval);
  }, []);

  const formatDataForChart = (key: string) => {
    if (data.length === 0) {
      return {
        labels: ["No data"],
        datasets: [{
          data: [0]
        }],
        hour: ''
      };
    }

    const labels = data.map(item => new Date(item.timestamp).toLocaleTimeString([], { minute: '2-digit' }));
    const startHour = new Date(data[0].timestamp).toLocaleTimeString([], { hour: '2-digit' });
    const endHour = new Date(data[data.length - 1].timestamp).toLocaleTimeString([], { hour: '2-digit' });
    const dataset = data.map(item => item[key]);

    return {
      labels: labels,
      datasets: [{
        data: dataset
      }],
      hour: `${startHour} - ${endHour}`
    };
  };

  const calculateAverage = (key: string) => {
    const values = data.map(item => item[key]);
    const sum = values.reduce((acc, curr) => acc + curr, 0);
    return (sum / values.length).toFixed(2);
  };

  const temperatureData = formatDataForChart('temperature');
  const humidityData = formatDataForChart('humidity');
  const mq2Data = formatDataForChart('mq2_ppm');
  const mq7Data = formatDataForChart('mq7_ppm');
  const dustDensityData = formatDataForChart('dust_density');
  const mq135Data = formatDataForChart('mq135_ppm');

  const avgTemperature = calculateAverage('temperature');
  const avgHumidity = calculateAverage('humidity');
  const avgMq2 = calculateAverage('mq2_ppm');
  const avgMq7 = calculateAverage('mq7_ppm');
  const avgDustDensity = calculateAverage('dust_density');
  const avgMq135 = calculateAverage('mq135_ppm');

  const chartConfig = {
    backgroundGradientFrom: "#fff",
    backgroundGradientTo: "#fff",
    color: (opacity = 1) => `rgba(0, 0, 0, ${opacity})`,
    labelColor: (opacity = 1) => `rgba(0, 0, 0, ${opacity})`,
    style: {
      borderRadius: 16,
      borderColor: '#000',
      borderWidth: 1,
      shadowColor: '#000',
      shadowOffset: { width: 0, height: 2 },
      shadowOpacity: 0.1,
      shadowRadius: 4,
      elevation: 3,
    },
    propsForDots: {
      r: "6",
      strokeWidth: "2",
      stroke: "#ffa726"
    },
    decimalPlaces: 2
  };

  return (
    <ScrollView style={styles.container}>
      <View style={styles.header}>
        <Text style={styles.headerTitle}>IOT Service</Text>
      </View>
      <View style={styles.card}>
        <Text style={styles.chartTitle}>온도</Text>
        <Text style={styles.chartSubtitle}>
          평균 온도: {avgTemperature}°C
        </Text>
        <Text style={styles.chartHour}>{temperatureData.hour}</Text>
        <View style={styles.chartBox}>
          <LineChart
            data={temperatureData}
            width={width - 48} // Adjusted width
            height={220}
            chartConfig={{
              ...chartConfig,
              color: (opacity = 1) => `rgba(255, 99, 132, ${opacity})`,
            }}
            bezier
            fromZero={true}
            yAxisLabel=""
            yLabelsOffset={5}
            formatYLabel={(value) => `${value}°C`}
            yAxisInterval={1}
          />
        </View>
      </View>
      <View style={styles.card}>
        <Text style={styles.chartTitle}>습도</Text>
        <Text style={styles.chartSubtitle}>
          평균 습도: {avgHumidity}%
        </Text>
        <Text style={styles.chartHour}>{humidityData.hour}</Text>
        <View style={styles.chartBox}>
          <LineChart
            data={humidityData}
            width={width - 48} // Adjusted width
            height={220}
            chartConfig={{
              ...chartConfig,
              color: (opacity = 1) => `rgba(54, 162, 235, ${opacity})`,
            }}
            bezier
            fromZero={true}
            yAxisLabel=""
            yLabelsOffset={5}
            formatYLabel={(value) => `${value}%`}
            yAxisInterval={1}
          />
        </View>
      </View>
      <View style={styles.card}>
        <Text style={styles.chartTitle}>유해 가스</Text>
        <Text style={styles.chartSubtitle}>
          평균 유해 가스: {avgMq2} ppm
        </Text>
        <Text style={styles.chartHour}>{mq2Data.hour}</Text>
        <View style={styles.chartBox}>
          <LineChart
            data={mq2Data}
            width={width - 48} // Adjusted width
            height={220}
            chartConfig={{
              ...chartConfig,
              color: (opacity = 1) => `rgba(255, 165, 0, ${opacity})`,
            }}
            bezier
            fromZero={true}
            yAxisLabel=""
            yLabelsOffset={5}
            formatYLabel={(value) => `${value} ppm`}
            yAxisInterval={1}
          />
        </View>
      </View>
      <View style={styles.card}>
        <Text style={styles.chartTitle}>이산화탄소 (CO2)</Text>
        <Text style={styles.chartSubtitle}>
          평균 CO2: {avgMq7} ppm
        </Text>
        <Text style={styles.chartHour}>{mq7Data.hour}</Text>
        <View style={styles.chartBox}>
          <LineChart
            data={mq7Data}
            width={width - 48} // Adjusted width
            height={220}
            chartConfig={{
              ...chartConfig,
              color: (opacity = 1) => `rgba(54, 162, 235, ${opacity})`,
            }}
            bezier
            fromZero={true}
            yAxisLabel=""
            yLabelsOffset={5}
            formatYLabel={(value) => `${value} ppm`}
            yAxisInterval={1}
          />
        </View>
      </View>
      <View style={styles.card}>
        <Text style={styles.chartTitle}>먼지 밀도</Text>
        <Text style={styles.chartSubtitle}>
          평균 먼지 밀도: {avgDustDensity} µg/m³
        </Text>
        <Text style={styles.chartHour}>{dustDensityData.hour}</Text>
        <View style={styles.chartBox}>
          <LineChart
            data={dustDensityData}
            width={width - 48} // Adjusted width
            height={220}
            chartConfig={{
              ...chartConfig,
              color: (opacity = 1) => `rgba(255, 159, 64, ${opacity})`,
            }}
            bezier
            fromZero={true}
            yAxisLabel=""
            yLabelsOffset={5}
            formatYLabel={(value) => `${value} µg/m³`}
            yAxisInterval={1}
          />
        </View>
      </View>
      <View style={styles.card}>
        <Text style={styles.chartTitle}>대기오염 가스</Text>
        <Text style={styles.chartSubtitle}>
          평균 유해 가스: {avgMq135} ppm
        </Text>
        <Text style={styles.chartHour}>{mq135Data.hour}</Text>
        <View style={styles.chartBox}>
          <LineChart
            data={mq135Data}
            width={width - 48} 
            height={220}
            chartConfig={{
              ...chartConfig,
              color: (opacity = 1) => `rgba(75, 192, 192, ${opacity})`,
            }}
            bezier
            fromZero={true}
            yAxisLabel=""
            yLabelsOffset={5}
            formatYLabel={(value) => `${value} ppm`}
            yAxisInterval={1}
          />
        </View>
      </View>
    </ScrollView>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    padding: 8, 
    backgroundColor: '#fff',
  },
  header: {
    alignItems: 'center',
    marginBottom: 16,
    paddingTop: 60,
  },
  headerTitle: {
    fontSize: 24,
    fontWeight: 'bold',
  },
  card: {
    backgroundColor: '#fff',
    borderRadius: 12,
    padding: 16,
    marginBottom: 20,
    borderColor: '#FFFFFF',
    borderWidth: 1,
    shadowColor: '#000',
    shadowOffset: {
      width: 0,
      height: 2,
    },
    shadowOpacity: 0.1,
    shadowRadius: 4,
    elevation: 3,
  },
  chartTitle: {
    fontSize: 18,
    fontWeight: 'bold',
    marginBottom: 8,
  },
  chartSubtitle: {
    fontSize: 14,
    marginBottom: 8,
    color: '#555',
  },
  chartHour: {
    position: 'absolute',
    top: 10,
    right: 10,
    fontSize: 14,
    color: '#555',
  },
  chartBox: {
    backgroundColor: '#fff',
    borderRadius: 12,
    padding: 16,
  },
});

export default IotInfo;