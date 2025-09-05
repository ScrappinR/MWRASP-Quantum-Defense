"""
Client SDK for Homomorphic Swarm
Easy-to-use interface for applications
"""

import asyncio
import aiohttp
from typing import List, Dict, Any, Optional, Union
import numpy as np
import tenseal as ts
from dataclasses import dataclass
import json
import time
from enum import Enum

class ComputationType(Enum):
    """Supported computation types"""
    ADD = "add"
    MULTIPLY = "multiply"
    BOOTSTRAP = "bootstrap"
    POLYNOMIAL = "polynomial"
    MATRIX_MULTIPLY = "matrix_multiply"
    COMPARISON = "comparison"

@dataclass
class SwarmConfig:
    """Client configuration"""
    queen_url: str = "https://localhost:8443"
    auth_token: Optional[str] = None
    tls_verify: bool = True
    ca_cert_path: Optional[str] = None
    timeout: int = 30
    retry_attempts: int = 3
    chunk_size: int = 1024 * 1024  # 1MB chunks

class SwarmClient:
    """Main client for interacting with homomorphic swarm"""
    
    def __init__(self, config: SwarmConfig = None):
        self.config = config or SwarmConfig()
        self._session: Optional[aiohttp.ClientSession] = None
        self._context: Optional[ts.Context] = None
        
    async def __aenter__(self):
        await self.connect()
        return self
        
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.close()
        
    async def connect(self):
        """Connect to swarm"""
        # Setup SSL
        ssl_context = None
        if self.config.ca_cert_path:
            import ssl
            ssl_context = ssl.create_default_context(cafile=self.config.ca_cert_path)
        elif not self.config.tls_verify:
            ssl_context = False
            
        # Create session
        connector = aiohttp.TCPConnector(ssl=ssl_context)
        self._session = aiohttp.ClientSession(
            connector=connector,
            headers={"Authorization": f"Bearer {self.config.auth_token}"} if self.config.auth_token else {}
        )
        
        # Get swarm configuration
        await self._get_swarm_config()
        
    async def close(self):
        """Close connection"""
        if self._session:
            await self._session.close()
            
    async def _get_swarm_config(self):
        """Get encryption parameters from swarm"""
        async with self._session.get(f"{self.config.queen_url}/config") as resp:
            if resp.status == 200:
                config = await resp.json()
                # Setup TenSEAL context
                self._context = ts.context(
                    ts.SCHEME_TYPE.CKKS,
                    poly_modulus_degree=config.get("poly_modulus_degree", 8192),
                    coeff_mod_bit_sizes=config.get("coeff_modulus", [60, 40, 40, 60])
                )
                self._context.global_scale = config.get("scale", 2**40)
                self._context.generate_galois_keys()
                
    async def encrypt(self, data: Union[float, List[float], np.ndarray]) -> 'EncryptedTensor':
        """Encrypt data for homomorphic computation"""
        if isinstance(data, (int, float)):
            data = [float(data)]
        elif isinstance(data, np.ndarray):
            data = data.flatten().tolist()
            
        # Encrypt using context
        encrypted = ts.ckks_vector(self._context, data)
        
        return EncryptedTensor(
            data=encrypted.serialize(),
            shape=len(data),
            client=self
        )
    
    async def decrypt(self, encrypted_tensor: 'EncryptedTensor') -> np.ndarray:
        """Decrypt result"""
        # Deserialize
        vector = ts.lazy_ckks_vector_from(encrypted_tensor.data)
        vector.link_context(self._context)
        
        # Decrypt
        result = vector.decrypt()
        
        # Reshape if needed
        if hasattr(encrypted_tensor, 'original_shape'):
            result = np.array(result).reshape(encrypted_tensor.original_shape)
            
        return np.array(result)
    
    async def compute(self, 
                     operation: ComputationType,
                     operands: List['EncryptedTensor'],
                     **kwargs) -> 'EncryptedTensor':
        """Execute computation on encrypted data"""
        # Prepare request
        request_data = {
            "operation": operation.value,
            "operands": [op.to_dict() for op in operands],
            "params": kwargs
        }
        
        # Send to swarm with retry
        for attempt in range(self.config.retry_attempts):
            try:
                async with self._session.post(
                    f"{self.config.queen_url}/compute",
                    json=request_data,
                    timeout=aiohttp.ClientTimeout(total=self.config.timeout)
                ) as resp:
                    if resp.status == 200:
                        result = await resp.json()
                        return EncryptedTensor(
                            data=bytes.fromhex(result["data"]),
                            shape=result.get("shape"),
                            client=self
                        )
                    else:
                        error = await resp.text()
                        if attempt == self.config.retry_attempts - 1:
                            raise Exception(f"Computation failed: {error}")
                        await asyncio.sleep(2 ** attempt)  # Exponential backoff
            except asyncio.TimeoutError:
                if attempt == self.config.retry_attempts - 1:
                    raise
                    
        raise Exception("Max retries exceeded")

class EncryptedTensor:
    """Represents encrypted data with operations"""
    
    def __init__(self, data: bytes, shape: Union[int, tuple], client: SwarmClient):
        self.data = data
        self.shape = shape
        self.client = client
        
    def to_dict(self) -> Dict:
        return {
            "data": self.data.hex(),
            "shape": self.shape
        }
    
    # Operator overloading for natural syntax
    async def __add__(self, other: 'EncryptedTensor') -> 'EncryptedTensor':
        return await self.client.compute(ComputationType.ADD, [self, other])
    
    async def __mul__(self, other: 'EncryptedTensor') -> 'EncryptedTensor':
        return await self.client.compute(ComputationType.MULTIPLY, [self, other])
    
    async def bootstrap(self) -> 'EncryptedTensor':
        """Refresh ciphertext noise"""
        return await self.client.compute(ComputationType.BOOTSTRAP, [self])

# High-level API functions
class HomomorphicCompute:
    """High-level computation API"""
    
    def __init__(self, client: SwarmClient):
        self.client = client
        
    async def linear_regression(self, 
                              X_encrypted: EncryptedTensor,
                              y_encrypted: EncryptedTensor,
                              iterations: int = 100,
                              learning_rate: float = 0.01) -> EncryptedTensor:
        """Encrypted linear regression"""
        # Initialize weights
        weights = await self.client.encrypt(np.random.randn(X_encrypted.shape[1]))
        
        for i in range(iterations):
            # Forward pass
            predictions = await self.client.compute(
                ComputationType.MATRIX_MULTIPLY,
                [X_encrypted, weights]
            )
            
            # Compute error
            error = await (predictions - y_encrypted)
            
            # Gradient descent
            gradient = await self.client.compute(
                ComputationType.MATRIX_MULTIPLY,
                [X_encrypted.transpose(), error],
                scale=learning_rate / X_encrypted.shape[0]
            )
            
            weights = await (weights - gradient)
            
            # Bootstrap periodically
            if i % 10 == 0:
                weights = await weights.bootstrap()
                
        return weights
    
    async def private_mean(self, encrypted_values: List[EncryptedTensor]) -> EncryptedTensor:
        """Compute mean of encrypted values"""
        # Sum all values
        total = encrypted_values[0]
        for value in encrypted_values[1:]:
            total = await (total + value)
            
        # Divide by count
        return await self.client.compute(
            ComputationType.MULTIPLY,
            [total],
            scalar=1.0 / len(encrypted_values)
        )
    
    async def secure_comparison(self, a: EncryptedTensor, b: EncryptedTensor) -> EncryptedTensor:
        """Compare encrypted values (returns encrypted 0 or 1)"""
        return await self.client.compute(ComputationType.COMPARISON, [a, b])

# Batch processing for efficiency
class BatchProcessor:
    """Process multiple operations in parallel"""
    
    def __init__(self, client: SwarmClient, batch_size: int = 10):
        self.client = client
        self.batch_size = batch_size
        self.pending_operations = []
        
    async def add_operation(self, operation: ComputationType, operands: List[EncryptedTensor], **kwargs):
        """Add operation to batch"""
        self.pending_operations.append((operation, operands, kwargs))
        
        if len(self.pending_operations) >= self.batch_size:
            return await self.flush()
            
    async def flush(self) -> List[EncryptedTensor]:
        """Execute all pending operations"""
        if not self.pending_operations:
            return []
            
        # Execute in parallel
        tasks = [
            self.client.compute(op, operands, **kwargs)
            for op, operands, kwargs in self.pending_operations
        ]
        
        results = await asyncio.gather(*tasks)
        self.pending_operations = []
        
        return results

# Example usage
async def example_usage():
    """Example of using the SDK"""
    # Connect to swarm
    config = SwarmConfig(
        queen_url="https://swarm.example.com",
        auth_token="your-auth-token"
    )
    
    async with SwarmClient(config) as client:
        # Encrypt sensitive data
        salary_data = [52000, 68000, 45000, 92000, 77000]
        encrypted_salaries = await client.encrypt(salary_data)
        
        # Compute average salary without decrypting
        compute = HomomorphicCompute(client)
        encrypted_avg = await compute.private_mean([encrypted_salaries])
        
        # Decrypt result
        avg_salary = await client.decrypt(encrypted_avg)
        print(f"Average salary: ${avg_salary[0]:,.2f}")
        
        # Machine learning on encrypted data
        X = np.random.randn(100, 5)  # Features
        y = np.random.randn(100)     # Labels
        
        X_enc = await client.encrypt(X)
        y_enc = await client.encrypt(y)
        
        # Train model on encrypted data
        encrypted_model = await compute.linear_regression(X_enc, y_enc)
        
        # The model remains encrypted - only authorized parties can decrypt

# JavaScript/TypeScript SDK
JS_SDK = """
// homomorphic-swarm-sdk.ts
export class SwarmClient {
    private config: SwarmConfig;
    private session: any;
    
    constructor(config: SwarmConfig) {
        this.config = config;
    }
    
    async encrypt(data: number[]): Promise<EncryptedTensor> {
        const response = await fetch(`${this.config.queenUrl}/encrypt`, {
            method: 'POST',
            headers: {
                'Authorization': `Bearer ${this.config.authToken}`,
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ data })
        });
        
        const result = await response.json();
        return new EncryptedTensor(result.data, result.shape, this);
    }
    
    async compute(operation: string, operands: EncryptedTensor[]): Promise<EncryptedTensor> {
        const response = await fetch(`${this.config.queenUrl}/compute`, {
            method: 'POST',
            headers: {
                'Authorization': `Bearer ${this.config.authToken}`,
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                operation,
                operands: operands.map(op => op.toJSON())
            })
        });
        
        const result = await response.json();
        return new EncryptedTensor(result.data, result.shape, this);
    }
}

// Example usage
const client = new SwarmClient({
    queenUrl: 'https://swarm.example.com',
    authToken: 'your-token'
});

const encrypted = await client.encrypt([1, 2, 3, 4, 5]);
const doubled = await client.compute('multiply', [encrypted], { scalar: 2 });
"""

if __name__ == "__main__":
    # Run example
    asyncio.run(example_usage())
