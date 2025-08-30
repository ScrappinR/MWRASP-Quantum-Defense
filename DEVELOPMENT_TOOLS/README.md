# MWRASP Development Tools

This directory contains development utilities, debugging tools, and system maintenance scripts for the MWRASP Quantum Defense Platform.

## 🛠️ Development Tools

### Debugging and Testing Tools
- `debug_decap.py` - DECAP algorithm debugging utility
- `debug_kyber.py` - Kyber algorithm debugging and testing
- `debug_kyber_detailed.py` - Detailed Kyber algorithm analysis
- `test_kyber_fix.py` - Kyber algorithm fix and validation

### System Status and Monitoring
- `mwrasp_instance_status.py` - MWRASP system instance status monitoring

## 🔧 Tool Categories

### Cryptographic Debugging 🔐
- **Kyber Algorithm Testing**: Comprehensive debugging for post-quantum cryptography
- **DECAP Testing**: Decapsulation algorithm validation
- **Algorithm Validation**: Cryptographic function verification
- **Performance Analysis**: Cryptographic performance testing

### System Monitoring 📊
- **Instance Status**: Real-time system status monitoring
- **Health Checks**: System health and performance validation
- **Resource Monitoring**: Memory, CPU, and network usage tracking
- **Error Detection**: Automated error detection and reporting

## 🚀 Usage

### Kyber Algorithm Debugging
```bash
# Basic Kyber debugging
python debug_kyber.py

# Detailed Kyber analysis
python debug_kyber_detailed.py

# Test Kyber fixes
python test_kyber_fix.py
```

### DECAP Algorithm Testing
```bash
# Debug DECAP implementation
python debug_decap.py
```

### System Status Monitoring
```bash
# Check MWRASP system status
python mwrasp_instance_status.py

# Continuous monitoring (with watch)
watch -n 5 python mwrasp_instance_status.py
```

## 🔍 Debugging Features

### Cryptographic Analysis ✅
- **Algorithm Validation**: Verify cryptographic implementations
- **Performance Testing**: Measure algorithm performance
- **Error Detection**: Identify implementation issues
- **Compliance Verification**: Ensure standards compliance

### System Diagnostics 📋
- **Status Reporting**: Real-time system status
- **Performance Metrics**: System performance analysis
- **Error Logging**: Comprehensive error tracking
- **Health Monitoring**: System health assessment

## 📊 Tool Output

### Debug Information
- **Algorithm Status**: Pass/fail status for cryptographic tests
- **Performance Metrics**: Timing and throughput measurements
- **Error Details**: Detailed error messages and stack traces
- **Validation Results**: Compliance and correctness validation

### System Status
- **Instance Health**: Overall system health status
- **Resource Usage**: CPU, memory, and network utilization
- **Agent Status**: Individual agent health and performance
- **Communication Status**: Inter-agent communication health

## 🔧 Development Workflow

### Testing New Features
1. **Use debugging tools** to validate new implementations
2. **Run cryptographic tests** to ensure correctness
3. **Monitor system status** during testing
4. **Analyze performance** and optimize as needed

### Troubleshooting Issues
1. **Check system status** with monitoring tools
2. **Run specific debug scripts** for affected components
3. **Analyze error logs** and debug output
4. **Validate fixes** with testing tools

### Performance Optimization
1. **Profile cryptographic functions** with debug tools
2. **Monitor resource usage** during operations
3. **Identify bottlenecks** and optimization opportunities
4. **Validate improvements** with testing suite

## 🏗️ Integration

### Main System Integration
These tools integrate with:
- **Core System Implementations**: Debug running systems
- **Validation Framework**: Support comprehensive testing
- **Monitoring Dashboard**: Provide real-time status data
- **CI/CD Pipeline**: Automated testing and validation

### Development Environment
- **IDE Integration**: Compatible with VS Code, PyCharm
- **Command Line**: Full command-line interface support
- **Logging**: Integrated with system logging framework
- **Reporting**: Generate detailed debugging reports

## 📈 Performance

### Debugging Efficiency
- **Fast Execution**: Optimized for quick debugging cycles
- **Comprehensive Coverage**: Test all critical components
- **Detailed Output**: Comprehensive debugging information
- **Error Isolation**: Quickly identify and isolate issues

### System Monitoring
- **Real-time Updates**: Live system status monitoring
- **Low Overhead**: Minimal impact on system performance
- **Scalable**: Monitor single instances or distributed systems
- **Alerting**: Automated alerts for critical issues

---
*Essential development tools for MWRASP Quantum Defense Platform development and maintenance.*