"""Check the DeepSeek account: balance and available models. Never prints the key."""
import adapters

try:
    bal = adapters._deepseek_request("/user/balance")
    print("API usable:", bal.get("is_available"))
    for b in bal.get("balance_infos", []):
        print(f"  {b.get('currency')}: total {b.get('total_balance')} | granted (free) {b.get('granted_balance')}"
              f" | topped up {b.get('topped_up_balance')}")
    models = adapters._deepseek_request("/models")
    print("models:", ", ".join(m.get("id", "?") for m in models.get("data", [])))
except Exception as e:  # noqa: BLE001
    print("check failed:", e)
