#!/usr/bin/env python3
"""
Test script to verify all examples in the demo produce correct outputs.
Tests both formal logic and natural language examples.
"""

import json
import os
import sys
import requests
from typing import Dict, Any, List, Tuple

# API base URL - can be set via GPMSC_API_URL environment variable
API_BASE = os.getenv("GPMSC_API_URL", "https://gpmsc-api.onrender.com")
# For local testing, use: export GPMSC_API_URL=http://localhost:8001

# Test cases from the demo HTML
FORMAL_EXAMPLES = {
    "coverage": {
        "proposition": "((active_policy ∧ premium_paid) ∧ (valid_claim_date ∧ ¬excluded_condition)) → claim_approved",
        "expected_valid": True,
        "expected_paradox": False,
        "description": "Coverage → Approve"
    },
    "contradiction": {
        "proposition": "approved ∧ ¬approved",
        "expected_valid": False,  # Contradiction should be invalid
        "expected_paradox": False,  # Not a paradox, just a contradiction
        "description": "Contradiction"
    },
    "deductible": {
        "proposition": "(deductible_met ∧ service_covered) → (pay ∧ ¬copay_waived)",
        "expected_valid": True,
        "expected_paradox": False,
        "description": "Deductible Logic"
    },
    "circular": {
        "proposition": "∀p:Prop . V(p) ↔ ¬V(p)",
        "expected_valid": False,  # Paradox should be invalid
        "expected_paradox": True,  # This is a paradox
        "description": "Circular Dependency"
    }
}

NATURAL_EXAMPLES = {
    "coverage": {
        "statement": "If the patient has active coverage and the claim amount is within the annual limit, then the claim should be approved",
        "expected_valid": True,
        "expected_paradox": False,
        "description": "Coverage Check"
    },
    "contradiction": {
        "statement": "The claim is approved and the claim is denied",
        "expected_valid": False,  # Contradiction should be invalid
        "expected_paradox": False,  # Not a paradox, just a contradiction
        "description": "Contradiction"
    },
    "deductible": {
        "statement": "If the deductible is met and the service is covered, then pay the claim minus copay",
        "expected_valid": True,
        "expected_paradox": False,
        "description": "Deductible Logic"
    },
    "circular": {
        "statement": "This policy is valid if and only if this policy is not valid",
        "expected_valid": False,  # Paradox should be invalid
        "expected_paradox": True,  # This should be detected as a paradox
        "description": "Circular Rule"
    }
}


def test_formal_example(name: str, test_case: Dict[str, Any]) -> Tuple[bool, str]:
    """Test a formal logic example."""
    print(f"\n📋 Testing Formal: {test_case['description']}")
    print(f"   Input: {test_case['proposition']}")
    
    try:
        response = requests.post(
            f"{API_BASE}/verify",
            json={"proposition": test_case["proposition"]},
            headers={"Content-Type": "application/json"},
            timeout=10
        )
        
        if response.status_code != 200:
            return False, f"HTTP {response.status_code}: {response.text}"
        
        data = response.json()
        
        # Check expected results
        # For formal logic, compute logical validity same way as demo HTML does:
        # valid syntax AND no paradox AND satisfiable (not a contradiction)
        valid_syntax = data.get("valid", False)
        paradox = data.get("paradox_detected", False)
        smt_satisfiable = data.get("smt_satisfiable")
        # Python: None/True = OK, False = contradiction
        is_logically_valid = valid_syntax and not paradox and (smt_satisfiable is not False)
        
        valid_match = is_logically_valid == test_case["expected_valid"]
        paradox_match = paradox == test_case["expected_paradox"]
        
        print(f"   Expected: valid={test_case['expected_valid']}, paradox={test_case['expected_paradox']}")
        print(f"   Got:      valid={is_logically_valid}, paradox={paradox} (syntax={valid_syntax}, smt={smt_satisfiable})")
        
        if valid_match and paradox_match:
            return True, "✓ PASS"
        else:
            issues = []
            if not valid_match:
                issues.append(f"validity mismatch (expected {test_case['expected_valid']}, got {is_logically_valid})")
            if not paradox_match:
                issues.append(f"paradox mismatch (expected {test_case['expected_paradox']}, got {paradox})")
            return False, f"✗ FAIL: {', '.join(issues)}"
            
    except Exception as e:
        return False, f"✗ ERROR: {str(e)}"


def test_natural_example(name: str, test_case: Dict[str, Any]) -> Tuple[bool, str]:
    """Test a natural language example."""
    print(f"\n💬 Testing Natural: {test_case['description']}")
    print(f"   Input: {test_case['statement']}")
    
    try:
        response = requests.post(
            f"{API_BASE}/verify/natural",
            json={"statement": test_case["statement"]},
            headers={"Content-Type": "application/json"},
            timeout=10
        )
        
        if response.status_code != 200:
            return False, f"HTTP {response.status_code}: {response.text}"
        
        data = response.json()
        
        # Check expected results
        valid = data.get("is_logically_valid", False)
        paradox = data.get("is_paradox", False)
        
        valid_match = valid == test_case["expected_valid"]
        paradox_match = paradox == test_case["expected_paradox"]
        
        print(f"   Expected: valid={test_case['expected_valid']}, paradox={test_case['expected_paradox']}")
        print(f"   Got:      valid={valid}, paradox={paradox}")
        
        # Also print translation if available
        if "formal_translation" in data:
            print(f"   Translation: {data['formal_translation']}")
        if "confidence" in data:
            print(f"   Confidence: {data['confidence']:.2f}")
        
        if valid_match and paradox_match:
            return True, "✓ PASS"
        else:
            issues = []
            if not valid_match:
                issues.append(f"validity mismatch (expected {test_case['expected_valid']}, got {valid})")
            if not paradox_match:
                issues.append(f"paradox mismatch (expected {test_case['expected_paradox']}, got {paradox})")
            return False, f"✗ FAIL: {', '.join(issues)}"
            
    except Exception as e:
        return False, f"✗ ERROR: {str(e)}"


def main():
    """Run all tests."""
    print("=" * 80)
    print("Testing ProofPlay Compliance Demo Examples")
    print("=" * 80)
    
    results = []
    
    # Test formal examples
    print("\n" + "=" * 80)
    print("FORMAL LOGIC EXAMPLES")
    print("=" * 80)
    for name, test_case in FORMAL_EXAMPLES.items():
        passed, message = test_formal_example(name, test_case)
        results.append(("formal", name, passed, message))
        print(f"   Result: {message}")
    
    # Test natural language examples
    print("\n" + "=" * 80)
    print("NATURAL LANGUAGE EXAMPLES")
    print("=" * 80)
    for name, test_case in NATURAL_EXAMPLES.items():
        passed, message = test_natural_example(name, test_case)
        results.append(("natural", name, passed, message))
        print(f"   Result: {message}")
    
    # Summary
    print("\n" + "=" * 80)
    print("SUMMARY")
    print("=" * 80)
    
    total = len(results)
    passed = sum(1 for _, _, p, _ in results if p)
    failed = total - passed
    
    print(f"\nTotal tests: {total}")
    print(f"Passed: {passed}")
    print(f"Failed: {failed}")
    
    if failed > 0:
        print("\nFailed tests:")
        for mode, name, passed, message in results:
            if not passed:
                print(f"  {mode}/{name}: {message}")
        sys.exit(1)
    else:
        print("\n✓ All tests passed!")
        sys.exit(0)


if __name__ == "__main__":
    main()
