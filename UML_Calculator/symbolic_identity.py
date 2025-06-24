"""
Symbolic Identity and Fingerprint System for UML

This module implements the symbolic identity and fingerprinting system for the Universal Mathematical Language (UML).
It provides functionality for tracking TFID/MIF across recursion, detecting identity collisions or harmonics,
and defining symbolic entropy scores for recursive structures.
"""

import math
import hashlib
import time
from typing import Dict, Any, List, Tuple, Optional

# Import UML core functions if needed
try:
    from uml_core import recursive_compress, tfid_anchor
except ImportError:
    # If uml_core is not available, define simple versions here
    def recursive_compress(value):
        """Simple implementation of recursive compression"""
        if isinstance(value, (int, float)):
            return round(value * 100) / 100
        return value
    
    def tfid_anchor(value, timestamp=None):
        """Simple implementation of TFID anchoring"""
        if timestamp is None:
            timestamp = time.time()
        return {
            'value': value,
            'timestamp': timestamp,
            'phase_signature': 0,
            'tfid_hash': hash(str(value) + str(timestamp))
        }

class SymbolicIdentity:
    """
    Symbolic Identity class for tracking mathematical expressions across recursion levels.
    Provides TFID (Temporal Frequency Identity) across session boundaries, and maintains
    identity coherence using phase-locked anchoring.
    """
    
    def __init__(self, initial_value=None, timestamp=None):
        """
        Initialize a new symbolic identity.
        
        Args:
            initial_value: The initial value for this identity
            timestamp: The timestamp for anchoring (default: current time)
        """
        self.value = initial_value
        self.creation_time = timestamp if timestamp is not None else time.time()
        self.last_update = self.creation_time
        self.update_count = 0
        self.recursion_depth = 0
        self.fingerprints = []  # History of fingerprints for this identity
        self.mif_score = 0.0  # Memory Integration Factor score
        
        # Create initial fingerprint
        if initial_value is not None:
            self.update(initial_value)
    
    def update(self, value, recursion_depth=0):
        """
        Update this identity with a new value, creating a new fingerprint.
        
        Args:
            value: The new value for this identity
            recursion_depth: The current recursion depth
        """
        self.value = value
        self.recursion_depth = max(self.recursion_depth, recursion_depth)
        self.last_update = time.time()
        self.update_count += 1
        
        # Generate new fingerprint
        fingerprint = SymbolicFingerprint(value, self.last_update, recursion_depth)
        self.fingerprints.append(fingerprint)
        
        # Update MIF score based on fingerprint
        if len(self.fingerprints) > 1:
            self.mif_score = self._calculate_mif_score()
        
        return fingerprint
    
    def _calculate_mif_score(self):
        """Calculate the Memory Integration Factor score based on fingerprint history"""
        if not self.fingerprints:
            return 0.0
        
        # Calculate based on latest fingerprint and identity history
        latest = self.fingerprints[-1]
        
        # Time-based decay factor
        time_factor = math.exp(-0.1 * (time.time() - self.creation_time))
        
        # Complexity factor based on entropy
        complexity_factor = latest.entropy_score / 10.0
        
        # Update frequency factor
        frequency_factor = min(1.0, self.update_count / 100.0)
        
        return (time_factor + complexity_factor + frequency_factor) / 3.0
    
    def get_tfid(self):
        """Get the TFID anchor for this identity"""
        return tfid_anchor(self.value, self.last_update)
    
    def match_score(self, other_identity):
        """
        Calculate match score between this identity and another.
        Returns a value between 0.0 (no match) and 1.0 (perfect match).
        """
        if not self.fingerprints or not other_identity.fingerprints:
            return 0.0
        
        this_fp = self.fingerprints[-1]
        other_fp = other_identity.fingerprints[-1]
        
        return this_fp.similarity(other_fp)
    
    def to_dict(self):
        """Convert identity to dictionary for serialization"""
        return {
            'value': self.value,
            'creation_time': self.creation_time,
            'last_update': self.last_update,
            'update_count': self.update_count,
            'recursion_depth': self.recursion_depth,
            'mif_score': self.mif_score,
            'fingerprints': [fp.to_dict() for fp in self.fingerprints]
        }
    
    @classmethod
    def from_dict(cls, data):
        """Create identity from dictionary"""
        identity = cls(data['value'], data['creation_time'])
        identity.last_update = data['last_update']
        identity.update_count = data['update_count']
        identity.recursion_depth = data['recursion_depth']
        identity.mif_score = data['mif_score']
        identity.fingerprints = [SymbolicFingerprint.from_dict(fp) for fp in data['fingerprints']]
        return identity


class SymbolicFingerprint:
    """
    Symbolic Fingerprint for detecting mathematical identity collisions or harmonics.
    Provides entropy scoring and similarity comparison for recursive structures.
    """
    
    def __init__(self, value, timestamp=None, recursion_depth=0):
        """
        Initialize a new symbolic fingerprint.
        
        Args:
            value: The value to fingerprint
            timestamp: The timestamp for this fingerprint (default: current time)
            recursion_depth: The recursion depth at which this fingerprint was created
        """
        self.value = value
        self.timestamp = timestamp if timestamp is not None else time.time()
        self.recursion_depth = recursion_depth
        
        # Calculate fingerprint hash
        self.hash = self._calculate_hash(value)
        
        # Calculate entropy score
        self.entropy_score = self._calculate_entropy(value)
        
        # Create signature tuple (hash, entropy, recursion_depth)
        self.signature = (self.hash, self.entropy_score, self.recursion_depth)
    
    def _calculate_hash(self, value):
        """Calculate a hash for the value that's stable across sessions"""
        # For numeric values, we need a stable representation
        if isinstance(value, (int, float)):
            # Round to 10 decimal places for stability
            value_str = f"{value:.10g}"
        else:
            value_str = str(value)
        
        # Use SHA-256 for a stable, high-quality hash
        return hashlib.sha256(value_str.encode('utf-8')).hexdigest()[:16]
    
    def _calculate_entropy(self, value):
        """
        Calculate the symbolic entropy score for a value.
        Returns a value between 0.0 (minimum entropy) and 10.0 (maximum entropy).
        """
        # Convert to string for entropy calculation
        if isinstance(value, (int, float)):
            # For numeric values, look at the digits
            value_str = f"{value:.10g}"
            
            # Simple entropy based on number of decimal places and range
            if '.' in value_str:
                integer_part, decimal_part = value_str.split('.')
                decimal_entropy = min(len(decimal_part) / 10.0, 1.0) * 5.0
            else:
                integer_part = value_str
                decimal_entropy = 0.0
            
            # Integer complexity (higher for numbers that are not simple powers)
            int_val = int(integer_part)
            if int_val == 0:
                integer_entropy = 0.0
            else:
                # Check if it's a power of a small integer
                is_power = False
                for base in range(2, 11):
                    for exp in range(1, 10):
                        if int_val == base ** exp:
                            is_power = True
                            break
                    if is_power:
                        break
                
                integer_entropy = 5.0 if not is_power else 2.0
            
            return decimal_entropy + integer_entropy
        
        # For non-numeric values, use string length as proxy for complexity
        else:
            value_str = str(value)
            return min(len(value_str) / 20.0, 1.0) * 10.0
    
    def similarity(self, other_fingerprint):
        """
        Calculate similarity between this fingerprint and another.
        Returns a value between 0.0 (no similarity) and 1.0 (identical).
        """
        if self.hash == other_fingerprint.hash:
            return 1.0
        
        # Compare entropy scores (closer = more similar)
        entropy_diff = abs(self.entropy_score - other_fingerprint.entropy_score)
        entropy_similarity = max(0.0, 1.0 - entropy_diff / 10.0)
        
        # For numeric values, compare the actual values
        if isinstance(self.value, (int, float)) and isinstance(other_fingerprint.value, (int, float)):
            # Normalize the values for comparison
            self_val = abs(self.value)
            other_val = abs(other_fingerprint.value)
            
            if self_val == 0 and other_val == 0:
                value_similarity = 1.0
            else:
                # Use ratio for comparison
                ratio = min(self_val, other_val) / max(self_val, other_val) if max(self_val, other_val) > 0 else 0.0
                value_similarity = ratio
        else:
            # For non-numeric values, use simple string comparison
            value_similarity = 0.0
            
        # Weight the similarities
        return 0.5 * entropy_similarity + 0.5 * value_similarity
    
    def detect_harmonic(self, other_fingerprint):
        """
        Detect if this fingerprint forms a harmonic with another fingerprint.
        Returns a tuple (is_harmonic, harmonic_type).
        """
        # Simple harmonic detection: exact numeric ratio or recursion relation
        if isinstance(self.value, (int, float)) and isinstance(other_fingerprint.value, (int, float)):
            # Check for simple rational relationships
            if self.value != 0 and other_fingerprint.value != 0:
                ratio = self.value / other_fingerprint.value
                ratio_inverse = other_fingerprint.value / self.value
                
                # Check if ratio is close to a simple fraction
                for n in range(1, 10):
                    for d in range(1, 10):
                        if abs(ratio - n/d) < 0.001:
                            return True, f"{n}/{d}"
                        if abs(ratio_inverse - n/d) < 0.001:
                            return True, f"{d}/{n}"
                            
        # Check if recursion depths have a pattern
        if abs(self.recursion_depth - other_fingerprint.recursion_depth) == 1:
            return True, "Sequential Recursion"
            
        return False, None
    
    def to_dict(self):
        """Convert fingerprint to dictionary for serialization"""
        return {
            'value': self.value,
            'timestamp': self.timestamp,
            'recursion_depth': self.recursion_depth,
            'hash': self.hash,
            'entropy_score': self.entropy_score,
        }
    
    @classmethod
    def from_dict(cls, data):
        """Create fingerprint from dictionary"""
        fingerprint = cls(data['value'], data['timestamp'], data['recursion_depth'])
        fingerprint.hash = data['hash']
        fingerprint.entropy_score = data['entropy_score']
        fingerprint.signature = (fingerprint.hash, fingerprint.entropy_score, fingerprint.recursion_depth)
        return fingerprint


# --- Test and demo functions ---

def demo_symbolic_identity():
    """Demonstrate the symbolic identity and fingerprint system"""
    # Create identities for some mathematical expressions
    id1 = SymbolicIdentity(3.14159)
    id2 = SymbolicIdentity(2.71828)
    id3 = SymbolicIdentity(3.14159)  # Same as id1
    
    # Update with new values to simulate recursive evolution
    id1.update(3.14159 * 2, recursion_depth=1)
    id2.update(2.71828 ** 2, recursion_depth=1)
    
    # Compare identities
    print(f"Match score between id1 and id2: {id1.match_score(id2):.4f}")
    print(f"Match score between id1 and id3: {id1.match_score(id3):.4f}")
    
    # Fingerprint comparisons
    fp1 = id1.fingerprints[-1]
    fp2 = id2.fingerprints[-1]
    fp3 = id3.fingerprints[-1]
    
    print(f"\nFingerprint for id1: {fp1.hash}, entropy: {fp1.entropy_score:.2f}")
    print(f"Fingerprint for id2: {fp2.hash}, entropy: {fp2.entropy_score:.2f}")
    
    # Check for harmonics
    is_harmonic, harmonic_type = fp1.detect_harmonic(fp2)
    print(f"\nHarmonic between fp1 and fp2: {is_harmonic}, type: {harmonic_type}")


if __name__ == "__main__":
    demo_symbolic_identity()
