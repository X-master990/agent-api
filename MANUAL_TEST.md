# TrustMesh Week 1 Manual Test

這份文件用來手動驗證 `Week 1` 已完成的功能：

- PostgreSQL 啟動
- migration 套用
- API 啟動
- agent 建立 / 查詢
- Ed25519 JWT sign / verify spike

## 1. 啟動 PostgreSQL

```bash
~/Applications/Postgres.app/Contents/Versions/16/bin/pg_ctl \
  -D "$HOME/Library/Application Support/Postgres/var-16" \
  -l "$HOME/Library/Logs/Postgres/postgres-16.log" \
  start
```

確認 DB 已啟動：

```bash
~/Applications/Postgres.app/Contents/Versions/16/bin/pg_isready -h 127.0.0.1 -p 5432
```

預期結果：

```text
127.0.0.1:5432 - accepting connections
```

## 2. 套用 migration

```bash
cd "/Users/b/Desktop/ai agent security"
.venv/bin/alembic upgrade head
```

預期結果包含：

```text
Running upgrade  -> 20260420_2120, initial_trustmesh_week1
```

## 3. 啟動 API

```bash
cd "/Users/b/Desktop/ai agent security"
.venv/bin/python -m uvicorn app.main:app --host 127.0.0.1 --port 8000
```

也可以直接打開 Swagger：

- `http://127.0.0.1:8000/docs`

## 4. 健康檢查

```bash
curl http://127.0.0.1:8000/probe/live
```

預期結果：

```json
"ok"
```

## 5. 建立 agent

```bash
curl -X POST http://127.0.0.1:8000/v1/agents \
  -H 'Content-Type: application/json' \
  -d '{
    "name": "Alice Procurement Agent",
    "operator": "alice@alicecorp.com",
    "metadata": {
      "team": "procurement"
    }
  }'
```

預期結果類似：

```json
{
  "id": "f947ec5e-ebaf-45c5-ba6a-5f0a8fcc1ff0",
  "did": "did:key:z6Mk...",
  "name": "Alice Procurement Agent",
  "operator": "alice@alicecorp.com",
  "metadata": {
    "team": "procurement"
  },
  "created_at": "2026-04-20T13:40:14.623667Z",
  "status": "active"
}
```

注意：把回傳的 `id` 記下來，下一步會用到。

## 6. 查詢 agent

```bash
curl http://127.0.0.1:8000/v1/agents/<agent_id>
```

把 `<agent_id>` 換成上一個步驟拿到的 id。

預期結果：

- `id` 一致
- `did` 存在
- `status` 為 `active`

## 7. 測試 Ed25519 JWT sign

```bash
curl -X POST http://127.0.0.1:8000/v1/crypto/spike/sign \
  -H 'Content-Type: application/json' \
  -d '{
    "issuer": "did:key:zIssuer",
    "subject": "did:key:zSubject",
    "claims": {
      "audience": "acme-procurement-api"
    },
    "expires_in": 300
  }'
```

預期結果類似：

```json
{
  "jwt": "eyJhbGciOiJFZERTQSIsInR5cCI6IkpXVCJ9...",
  "public_key_pem": "-----BEGIN PUBLIC KEY-----\n...\n-----END PUBLIC KEY-----\n"
}
```

把 `jwt` 和 `public_key_pem` 記下來。

## 8. 測試 Ed25519 JWT verify

```bash
curl -X POST http://127.0.0.1:8000/v1/crypto/spike/verify \
  -H 'Content-Type: application/json' \
  -d '{
    "jwt": "<jwt>",
    "public_key_pem": "-----BEGIN PUBLIC KEY-----\n...\n-----END PUBLIC KEY-----\n"
  }'
```

預期結果：

```json
{
  "valid": true,
  "payload": {
    "iss": "did:key:zIssuer",
    "sub": "did:key:zSubject",
    "audience": "acme-procurement-api",
    "iat": 1776692352,
    "exp": 1776692652
  },
  "reason": null
}
```

## 9. 直接查資料庫

確認 `agents` 資料真的進 DB：

```bash
~/Applications/Postgres.app/Contents/Versions/16/bin/psql \
  -h 127.0.0.1 \
  -p 5432 \
  -d trustmesh \
  -c 'select id, did, name, operator from agents order by created_at desc limit 5;'
```

## 10. 停止 PostgreSQL

```bash
~/Applications/Postgres.app/Contents/Versions/16/bin/pg_ctl \
  -D "$HOME/Library/Application Support/Postgres/var-16" \
  stop
```

## Week 1 驗收重點

如果下面都成立，表示 `Week 1` 達標：

- `/probe/live` 正常
- `POST /v1/agents` 成功
- `GET /v1/agents/{id}` 成功
- 建立 agent 後 DB 查得到資料
- `/v1/crypto/spike/sign` 成功
- `/v1/crypto/spike/verify` 成功
