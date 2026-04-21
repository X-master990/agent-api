# TrustMesh Week 2 Manual Test

這份文件用來驗證 Week 2 的完整授權流程：

- issue credential
- verify allowed request
- verify denied request
- revoke credential
- verify revoked credential denied
- audit log 查詢

以下範例假設 API 跑在 `http://127.0.0.1:8000`。

## 1. 啟動 API

```bash
cd "/Users/b/Desktop/ai agent security"
.venv/bin/python -m uvicorn app.main:app --host 127.0.0.1 --port 8000
```

如果 `8000` 被占用，改用 `8001` 或 `8002`，後面 URL 也要跟著改。

## 2. 建立 agent

```bash
curl -s -X POST http://127.0.0.1:8000/v1/agents \
  -H 'Content-Type: application/json' \
  -d '{
    "name": "Alice Procurement Agent",
    "operator": "alice@alicecorp.com",
    "metadata": {
      "team": "procurement"
    }
  }'
```

把回傳的 `did` 記下來，下面的 `<agent_did>` 都換成這個值。

## 3. 簽發 credential

```bash
curl -s -X POST http://127.0.0.1:8000/v1/credentials/issue \
  -H 'Content-Type: application/json' \
  -d '{
    "issuer": "<agent_did>",
    "subject": "<agent_did>",
    "claims": {
      "authorized_by": "alice@alicecorp.com",
      "audience": "acme-procurement-api",
      "allowed_actions": ["purchase.create", "catalog.read"],
      "resource_scope": {
        "vendor_id": "acme"
      },
      "spending_limit_usd": 500
    },
    "expires_in": 86400
  }'
```

把回傳的 `id` 和 `jwt` 記下來。

## 4. 驗證合法操作

```bash
curl -s -X POST http://127.0.0.1:8000/v1/credentials/verify \
  -H 'Content-Type: application/json' \
  -d '{
    "jwt": "<jwt>",
    "audience": "acme-procurement-api",
    "action": "purchase.create",
    "resource": {
      "vendor_id": "acme"
    },
    "amount_usd": 180
  }'
```

預期結果：

```json
{
  "valid": true,
  "allowed": true,
  "reason": null
}
```

## 5. 驗證 action 越權

```bash
curl -s -X POST http://127.0.0.1:8000/v1/credentials/verify \
  -H 'Content-Type: application/json' \
  -d '{
    "jwt": "<jwt>",
    "audience": "acme-procurement-api",
    "action": "purchase.delete",
    "resource": {
      "vendor_id": "acme"
    },
    "amount_usd": 180
  }'
```

預期結果：

```json
{
  "valid": true,
  "allowed": false,
  "reason": "action_not_allowed"
}
```

## 6. 驗證金額超限

```bash
curl -s -X POST http://127.0.0.1:8000/v1/credentials/verify \
  -H 'Content-Type: application/json' \
  -d '{
    "jwt": "<jwt>",
    "audience": "acme-procurement-api",
    "action": "purchase.create",
    "resource": {
      "vendor_id": "acme"
    },
    "amount_usd": 999
  }'
```

預期結果：

```json
{
  "valid": true,
  "allowed": false,
  "reason": "amount_limit_exceeded"
}
```

## 7. 撤銷 credential

```bash
curl -s -X POST http://127.0.0.1:8000/v1/credentials/<credential_id>/revoke
```

## 8. 驗證 revoked credential 被拒

```bash
curl -s -X POST http://127.0.0.1:8000/v1/credentials/verify \
  -H 'Content-Type: application/json' \
  -d '{
    "jwt": "<jwt>",
    "audience": "acme-procurement-api",
    "action": "purchase.create",
    "resource": {
      "vendor_id": "acme"
    },
    "amount_usd": 180
  }'
```

預期結果：

```json
{
  "valid": true,
  "allowed": false,
  "reason": "credential_revoked"
}
```

## 9. 查 audit logs

```bash
curl -s http://127.0.0.1:8000/v1/audit-logs
```

預期可以看到每次 verify 的紀錄，包含：

- `result`
- `reason`
- `audience`
- `action`
- `resource`
- `amount_usd`
- `verified_at`
