/**
 * Simulacra Mobile App Prototype
 * React Native implementation for biometric proof-of-humanity
 * Based on SERM consensus
 */

import React, { useState, useEffect } from 'react';
import {
  SafeAreaView,
  StyleSheet,
  Text,
  View,
  TouchableOpacity,
  ScrollView,
  ActivityIndicator,
  Dimensions,
  Alert
} from 'react-native';

// Mock imports (would be actual libraries in production)
const HealthKit = { requestAuthorization: () => Promise.resolve(true) };
const BiometricScorer = { calculate: () => ({ score: 85.3, confidence: 0.92 }) };
const PersonalFork = { sync: () => Promise.resolve({ status: 'success' }) };

const { width, height } = Dimensions.get('window');

const App = () => {
  const [biometricScore, setBiometricScore] = useState(null);
  const [isScanning, setIsScanning] = useState(false);
  const [syncStatus, setSyncStatus] = useState('idle');
  const [userData, setUserData] = useState({
    userId: 'director-prime',
    forkId: null,
    transactions: 0,
    lastSync: null
  });

  useEffect(() => {
    // Initialize on mount
    initializeSimulacra();
  }, []);

  const initializeSimulacra = async () => {
    try {
      // Request health data permissions
      const authorized = await HealthKit.requestAuthorization();
      if (authorized) {
        console.log('Health permissions granted');
      }
      
      // Generate fork ID
      const forkId = Math.random().toString(36).substring(7);
      setUserData(prev => ({ ...prev, forkId }));
    } catch (error) {
      Alert.alert('Initialization Error', error.message);
    }
  };

  const scanBiometrics = async () => {
    setIsScanning(true);
    
    // Simulate biometric scanning
    setTimeout(async () => {
      const result = BiometricScorer.calculate();
      setBiometricScore(result);
      setIsScanning(false);
      
      // Add to blockchain
      setUserData(prev => ({
        ...prev,
        transactions: prev.transactions + 1
      }));
      
      // Auto-sync if needed
      if (userData.transactions % 10 === 0) {
        await syncWithNetwork();
      }
    }, 2000);
  };

  const syncWithNetwork = async () => {
    setSyncStatus('syncing');
    
    try {
      const result = await PersonalFork.sync();
      if (result.status === 'success') {
        setSyncStatus('success');
        setUserData(prev => ({
          ...prev,
          lastSync: new Date().toISOString()
        }));
      }
    } catch (error) {
      setSyncStatus('error');
    }
    
    setTimeout(() => setSyncStatus('idle'), 3000);
  };

  const getScoreColor = (score) => {
    if (score > 80) return '#4CAF50';
    if (score > 60) return '#FFC107';
    return '#F44336';
  };

  return (
    <SafeAreaView style={styles.container}>
      <ScrollView contentContainerStyle={styles.scrollContainer}>
        {/* Header */}
        <View style={styles.header}>
          <Text style={styles.title}>SIMULACRA</Text>
          <Text style={styles.subtitle}>Proof of Humanity</Text>
        </View>

        {/* User Info */}
        <View style={styles.card}>
          <Text style={styles.cardTitle}>Identity</Text>
          <Text style={styles.infoText}>User: {userData.userId}</Text>
          <Text style={styles.infoText}>Fork: {userData.forkId || 'Initializing...'}</Text>
          <Text style={styles.infoText}>Transactions: {userData.transactions}</Text>
        </View>

        {/* Biometric Score */}
        <View style={styles.card}>
          <Text style={styles.cardTitle}>Biometric Score</Text>
          
          {isScanning ? (
            <View style={styles.scanningContainer}>
              <ActivityIndicator size="large" color="#6200EE" />
              <Text style={styles.scanningText}>Scanning biometrics...</Text>
            </View>
          ) : biometricScore ? (
            <View style={styles.scoreContainer}>
              <Text style={[styles.scoreValue, { color: getScoreColor(biometricScore.score) }]}>
                {biometricScore.score.toFixed(1)}
              </Text>
              <Text style={styles.scoreLabel}>Humanity Score</Text>
              <Text style={styles.confidenceText}>
                Confidence: {(biometricScore.confidence * 100).toFixed(0)}%
              </Text>
            </View>
          ) : (
            <Text style={styles.noDataText}>No scan performed</Text>
          )}
          
          <TouchableOpacity 
            style={[styles.button, isScanning && styles.buttonDisabled]}
            onPress={scanBiometrics}
            disabled={isScanning}
          >
            <Text style={styles.buttonText}>
              {isScanning ? 'Scanning...' : 'Scan Biometrics'}
            </Text>
          </TouchableOpacity>
        </View>

        {/* Sync Status */}
        <View style={styles.card}>
          <Text style={styles.cardTitle}>Network Sync</Text>
          
          <View style={styles.syncContainer}>
            <View style={[styles.syncIndicator, {
              backgroundColor: syncStatus === 'success' ? '#4CAF50' :
                             syncStatus === 'error' ? '#F44336' :
                             syncStatus === 'syncing' ? '#FFC107' : '#9E9E9E'
            }]} />
            <Text style={styles.syncText}>
              {syncStatus === 'syncing' ? 'Syncing with IOTA Shimmer...' :
               syncStatus === 'success' ? 'Successfully synced' :
               syncStatus === 'error' ? 'Sync failed' :
               'Ready to sync'}
            </Text>
          </View>
          
          {userData.lastSync && (
            <Text style={styles.lastSyncText}>
              Last sync: {new Date(userData.lastSync).toLocaleTimeString()}
            </Text>
          )}
          
          <TouchableOpacity 
            style={[styles.button, styles.buttonSecondary]}
            onPress={syncWithNetwork}
          >
            <Text style={styles.buttonText}>Manual Sync</Text>
          </TouchableOpacity>
        </View>

        {/* Privacy Notice */}
        <View style={styles.privacyCard}>
          <Text style={styles.privacyTitle}>🔒 Privacy Protected</Text>
          <Text style={styles.privacyText}>
            • Personal fork on your device{'\n'}
            • 15-minute identifier rotation{'\n'}
            • Double encryption for Phase 2{'\n'}
            • You control sync frequency
          </Text>
        </View>

        {/* Revenue Potential (Grey Area) */}
        <View style={styles.revenueCard}>
          <Text style={styles.revenueTitle}>💰 Revenue Potential</Text>
          <Text style={styles.revenueAmount}>$0.00</Text>
          <Text style={styles.revenueText}>
            Anonymous pattern sharing available
          </Text>
        </View>
      </ScrollView>
    </SafeAreaView>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#F5F5F5'
  },
  scrollContainer: {
    paddingBottom: 20
  },
  header: {
    backgroundColor: '#6200EE',
    padding: 20,
    alignItems: 'center'
  },
  title: {
    fontSize: 32,
    fontWeight: 'bold',
    color: '#FFFFFF',
    letterSpacing: 2
  },
  subtitle: {
    fontSize: 16,
    color: '#FFFFFF',
    marginTop: 5,
    opacity: 0.9
  },
  card: {
    backgroundColor: '#FFFFFF',
    margin: 15,
    padding: 20,
    borderRadius: 12,
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.1,
    shadowRadius: 4,
    elevation: 3
  },
  cardTitle: {
    fontSize: 20,
    fontWeight: '600',
    marginBottom: 15,
    color: '#212121'
  },
  infoText: {
    fontSize: 14,
    color: '#616161',
    marginBottom: 5
  },
  scanningContainer: {
    alignItems: 'center',
    padding: 20
  },
  scanningText: {
    marginTop: 10,
    fontSize: 16,
    color: '#6200EE'
  },
  scoreContainer: {
    alignItems: 'center',
    padding: 20
  },
  scoreValue: {
    fontSize: 64,
    fontWeight: 'bold'
  },
  scoreLabel: {
    fontSize: 18,
    color: '#616161',
    marginTop: 5
  },
  confidenceText: {
    fontSize: 14,
    color: '#9E9E9E',
    marginTop: 10
  },
  noDataText: {
    fontSize: 16,
    color: '#9E9E9E',
    textAlign: 'center',
    padding: 20
  },
  button: {
    backgroundColor: '#6200EE',
    padding: 15,
    borderRadius: 8,
    alignItems: 'center',
    marginTop: 15
  },
  buttonDisabled: {
    opacity: 0.5
  },
  buttonSecondary: {
    backgroundColor: '#03DAC6'
  },
  buttonText: {
    color: '#FFFFFF',
    fontSize: 16,
    fontWeight: '600'
  },
  syncContainer: {
    flexDirection: 'row',
    alignItems: 'center',
    marginBottom: 10
  },
  syncIndicator: {
    width: 12,
    height: 12,
    borderRadius: 6,
    marginRight: 10
  },
  syncText: {
    fontSize: 14,
    color: '#616161'
  },
  lastSyncText: {
    fontSize: 12,
    color: '#9E9E9E',
    marginTop: 5
  },
  privacyCard: {
    backgroundColor: '#E8F5E9',
    margin: 15,
    padding: 15,
    borderRadius: 12
  },
  privacyTitle: {
    fontSize: 16,
    fontWeight: '600',
    marginBottom: 10,
    color: '#2E7D32'
  },
  privacyText: {
    fontSize: 13,
    color: '#424242',
    lineHeight: 20
  },
  revenueCard: {
    backgroundColor: '#FFF3E0',
    margin: 15,
    padding: 15,
    borderRadius: 12,
    marginBottom: 30
  },
  revenueTitle: {
    fontSize: 16,
    fontWeight: '600',
    marginBottom: 10,
    color: '#E65100'
  },
  revenueAmount: {
    fontSize: 32,
    fontWeight: 'bold',
    color: '#FF6F00'
  },
  revenueText: {
    fontSize: 12,
    color: '#616161',
    marginTop: 5
  }
});

export default App;