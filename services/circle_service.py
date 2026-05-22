import os
import uuid
import time
import httpx
from typing import Dict, Any

CIRCLE_API_KEY = os.environ.get("CIRCLE_API_KEY")
CIRCLE_API_BASE_URL = "https://api.circle.com/v1/w3s"

class CircleService:
    @staticmethod
    def _is_simulator() -> bool:
        return not bool(CIRCLE_API_KEY)
        
    @staticmethod
    def create_wallet(user_id: str) -> Dict[str, Any]:
        """Provisions a new Circle Programmable Wallet for a user."""
        if CircleService._is_simulator():
            print(f"[Circle Simulator] Provisioning new wallet for user: {user_id}")
            time.sleep(1) # Simulate network latency
            return {
                "wallet_id": str(uuid.uuid4()),
                "address": f"0x_mock_wallet_{user_id[:8]}",
                "blockchain": "ETH-SEPOLIA"
            }
            
        # Actual Circle API implementation
        headers = {
            "Authorization": f"Bearer {CIRCLE_API_KEY}",
            "Content-Type": "application/json"
        }
        # Simplified Circle Programmable Wallet creation payload
        payload = {
            "idempotencyKey": str(uuid.uuid4()),
            "blockchains": ["ETH-SEPOLIA"],
            "count": 1,
            "entitySecretCiphertext": "mock_secret" # Requires complex RSA encryption in production
        }
        
        try:
            response = httpx.post(f"{CIRCLE_API_BASE_URL}/developer/wallets", headers=headers, json=payload)
            response.raise_for_status()
            data = response.json()["data"]["wallets"][0]
            return {
                "wallet_id": data["id"],
                "address": data["address"],
                "blockchain": data["blockchain"]
            }
        except Exception as e:
            print(f"Circle API Error (falling back to simulator): {e}")
            return CircleService.create_wallet(user_id) # Loop back to simulator logic if it fails

    @staticmethod
    def escrow_bet(wallet_address: str, amount_usdc: float) -> str:
        """Transfers USDC from the user's wallet to the Agora Escrow."""
        if CircleService._is_simulator():
            print(f"[Circle Simulator] Escrowing {amount_usdc} USDC from {wallet_address}")
            time.sleep(0.5)
            return f"0x_sim_escrow_{uuid.uuid4().hex[:8]}"
            
        # Actual Circle API implementation
        headers = {
            "Authorization": f"Bearer {CIRCLE_API_KEY}",
            "Content-Type": "application/json"
        }
        payload = {
            "idempotencyKey": str(uuid.uuid4()),
            "destinationAddress": "0x_AGORA_MASTER_ESCROW_ADDRESS",
            "amounts": [str(amount_usdc)],
            "feeLevel": "MEDIUM",
            "tokenId": "mock_usdc_token_id",
            "walletId": "user_wallet_id"
        }
        
        try:
            response = httpx.post(f"{CIRCLE_API_BASE_URL}/developer/transactions/transfer", headers=headers, json=payload)
            response.raise_for_status()
            return response.json()["data"]["txHash"]
        except Exception as e:
            print(f"Circle API Error (falling back to simulator): {e}")
            return f"0x_sim_escrow_fallback_{uuid.uuid4().hex[:8]}"

    @staticmethod
    def payout_winnings(wallet_address: str, amount_usdc: float) -> str:
        """Transfers USDC from the Agora Escrow to the winning user."""
        if CircleService._is_simulator():
            print(f"[Circle Simulator] Paying out {amount_usdc} USDC to {wallet_address} from Escrow")
            time.sleep(0.5)
            return f"0x_sim_payout_{uuid.uuid4().hex[:8]}"
            
        # Actual Circle API implementation
        headers = {
            "Authorization": f"Bearer {CIRCLE_API_KEY}",
            "Content-Type": "application/json"
        }
        payload = {
            "idempotencyKey": str(uuid.uuid4()),
            "destinationAddress": wallet_address,
            "amounts": [str(amount_usdc)],
            "feeLevel": "MEDIUM",
            "tokenId": "mock_usdc_token_id",
            "walletId": "agora_master_escrow_wallet_id"
        }
        
        try:
            response = httpx.post(f"{CIRCLE_API_BASE_URL}/developer/transactions/transfer", headers=headers, json=payload)
            response.raise_for_status()
            return response.json()["data"]["txHash"]
        except Exception as e:
            print(f"Circle API Error (falling back to simulator): {e}")
            return f"0x_sim_payout_fallback_{uuid.uuid4().hex[:8]}"
