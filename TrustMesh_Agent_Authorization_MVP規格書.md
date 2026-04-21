# TrustMesh

## Agent Authorization Layer MVP 規格書

為 B2B API 團隊打造的 AI Agent 授權與驗證層  
v1.0 · 2026 年 4 月

---

## 一、產品定義

### 一句話產品定義

**TrustMesh 是給 B2B SaaS / API 團隊的 Agent Authorization Layer：讓第三方 AI agents 帶著可驗證授權來呼叫你的 API，你能驗證它是誰、被誰授權、可以做什麼。**

### 為什麼這個方向比前兩版更有競爭力

第一版的問題是「agent identity」概念完整，但付費動機太弱。多數開發者不會為了「讓 agent 有 DID」付錢。

第二版的問題是「agent spend guard」痛點夠強，但競品很多，而且很容易被 observability 與 gateway 產品包掉。

這一版把兩者的優勢結合：

- 保留第一版的身份與憑證能力
- 吸收第二版的規則、限制、撤銷、稽核思路
- 不把產品賣成 generic identity，也不賣成 generic cost guard
- 直接對準一個更容易付費的場景：**讓 B2B API 安全接受第三方 agent 執行操作**

### 目標客群

最優先客群：

- 有公開 API 的 B2B SaaS 團隊
- 已經看到客戶開始用 AI agent 呼叫他們的 API
- 需要知道呼叫方是不是合法 agent、是否被授權、是否超出範圍

典型客戶：

- 支付 / 採購 / 報銷 / CRM / support SaaS
- 有「建立訂單、退款、查資料、修改設定」等高風險操作的 API
- 想開放 agent automation，但不想只靠傳統 API key

### 不先打的客群

- 單純想看 token 成本的團隊
- 純內部 side project 開發者
- 只需要 tracing / observability 的團隊
- 要完整企業 IAM / SSO / OPA policy engine 的大公司

---

## 二、核心價值與使用情境

### 核心價值

TrustMesh 回答四個問題：

1. 這個呼叫 API 的 agent 是誰？
2. 它是被誰授權的？
3. 它可以做哪些動作？
4. 它這次的請求是否超出授權範圍？

### Day 1 使用情境

情境：`Acme Procurement API` 想安全接受客戶的採購 agent 下單。

客戶公司 `Alice Corp` 有一個採購 agent，想代表採購經理去 Acme 下單。Acme 不想只收一組 API key，因為它需要知道：

- 這是哪個 agent
- 這個 agent 是否被 Alice Corp 授權
- 它是否只能買某個品類
- 它是否只能在某個金額上限內操作

TrustMesh 的流程：

1. Alice 在 TrustMesh 註冊她的 agent
2. Alice 發一張 capability credential 給她的 agent
3. Agent 呼叫 Acme API 時夾帶該 credential
4. Acme 的 API middleware 呼叫 TrustMesh verify API 或 SDK
5. TrustMesh 回傳：`allow / deny`，以及明確原因

### Demo 故事

```python
from trustmesh import TrustMesh

tm = TrustMesh(api_key="tm_sk_xxx")

agent = tm.agents.create(
    name="Alice Procurement Agent",
    operator="alice@alicecorp.com",
)

credential = tm.credentials.issue(
    issuer=agent.did,
    subject=agent.did,
    claims={
        "authorized_by": "alice@alicecorp.com",
        "audience": "acme-procurement-api",
        "allowed_actions": ["purchase.create", "catalog.read"],
        "resource_scope": {
            "vendor_id": "acme"
        },
        "spending_limit_usd": 500,
    },
    expires_in=86400,
)

result = tm.credentials.verify(
    jwt=credential.jwt,
    action="purchase.create",
    resource={
        "vendor_id": "acme"
    },
    amount_usd=180,
    audience="acme-procurement-api",
)

if result.allowed:
    print("allow")
else:
    print(result.reason)
```

重點不是「驗證一張 VC」，而是 **用 credential 做實際授權決策**。

---

## 三、MVP 範圍

### In Scope

MVP 只做 5 件事：

1. Agent 註冊
2. Capability credential 簽發
3. Credential 驗證
4. Policy check
5. Audit log

### Out of Scope

以下功能全部不做：

- 通用 DID 方法支援（先只做 `did:key`）
- JSON-LD VC
- Zero-knowledge proofs
- 複雜 delegation graph
- 即時 anomaly detection
- 即時 spend dashboard
- SSE 緊急停用
- 多語言 SDK
- Stripe 付費系統
- 企業 SSO
- OPA / Cedar policy engine

### MVP 成功標準

- 5 家 B2B API 團隊能跑通 demo
- 3 家明確表示這解決了 agent access control 問題
- 2 家把 TrustMesh 接到 staging 或 production
- 至少 1 家願意承諾試點或付費 PoC

---

## 四、產品介面與公開 API

### 核心物件

#### Agent

```json
{
  "id": "ag_xxx",
  "did": "did:key:z6Mk...",
  "name": "Alice Procurement Agent",
  "operator": "alice@alicecorp.com",
  "created_at": "2026-05-01T10:00:00Z",
  "status": "active"
}
```

#### Credential Claims

MVP 只支援以下 claims：

```json
{
  "authorized_by": "alice@alicecorp.com",
  "audience": "acme-procurement-api",
  "allowed_actions": ["purchase.create", "catalog.read"],
  "resource_scope": {
    "vendor_id": "acme"
  },
  "spending_limit_usd": 500
}
```

#### Verification Result

```json
{
  "valid": true,
  "allowed": true,
  "reason": null,
  "checks": {
    "signature": "valid",
    "expiry": "not_expired",
    "revocation": "not_revoked",
    "audience": "matched",
    "action": "allowed",
    "resource_scope": "matched",
    "amount_limit": "within_limit"
  },
  "issuer": "did:key:z6Mk...",
  "subject": "did:key:z6Mk...",
  "claims": {
    "authorized_by": "alice@alicecorp.com",
    "audience": "acme-procurement-api",
    "allowed_actions": ["purchase.create"],
    "resource_scope": {
      "vendor_id": "acme"
    },
    "spending_limit_usd": 500
  }
}
```

### REST API

所有 API 掛在 `https://api.trustmesh.dev/v1/...`

#### 1. `POST /v1/agents`

註冊 agent。

Request:

```json
{
  "name": "Alice Procurement Agent",
  "operator": "alice@alicecorp.com",
  "metadata": {
    "team": "procurement"
  }
}
```

#### 2. `POST /v1/credentials/issue`

簽發 capability credential。

Request:

```json
{
  "subject": "did:key:z6MkSubject",
  "issuer": "did:key:z6MkIssuer",
  "claims": {
    "authorized_by": "alice@alicecorp.com",
    "audience": "acme-procurement-api",
    "allowed_actions": ["purchase.create"],
    "resource_scope": {
      "vendor_id": "acme"
    },
    "spending_limit_usd": 500
  },
  "expires_in": 86400
}
```

#### 3. `POST /v1/credentials/verify`

驗證 credential 並做授權判斷。

Request:

```json
{
  "jwt": "eyJhbGciOiJFZERTQSIsInR5cCI6IkpXVCJ9...",
  "audience": "acme-procurement-api",
  "action": "purchase.create",
  "resource": {
    "vendor_id": "acme"
  },
  "amount_usd": 180
}
```

Response:

```json
{
  "valid": true,
  "allowed": true,
  "reason": null,
  "checks": {
    "signature": "valid",
    "expiry": "not_expired",
    "revocation": "not_revoked",
    "audience": "matched",
    "action": "allowed",
    "resource_scope": "matched",
    "amount_limit": "within_limit"
  }
}
```

拒絕時：

```json
{
  "valid": true,
  "allowed": false,
  "reason": "action_not_allowed",
  "checks": {
    "signature": "valid",
    "expiry": "not_expired",
    "revocation": "not_revoked",
    "audience": "matched",
    "action": "denied"
  }
}
```

#### 4. `POST /v1/credentials/{id}/revoke`

撤銷 credential。

#### 5. `GET /v1/audit-logs`

查最近的驗證與授權決策紀錄。

支援 query：

- `agent_id`
- `result`
- `from`
- `to`

### SDK 介面

```python
from trustmesh import TrustMesh

tm = TrustMesh(api_key="tm_sk_xxx")

tm.agents.create(...)
tm.credentials.issue(...)
tm.credentials.verify(...)
tm.credentials.revoke(...)
tm.audit_logs.list(...)
```

---

## 五、授權規則設計

### 規則檢查順序

每次 verify 固定按照以下順序：

1. JWT 格式是否合法
2. 簽章是否合法
3. 是否過期
4. 是否已撤銷
5. audience 是否匹配
6. action 是否在 `allowed_actions`
7. resource 是否符合 `resource_scope`
8. amount 是否小於等於 `spending_limit_usd`

任何一步失敗都直接拒絕。

### 規則語義

#### Audience

- 請求的 `audience` 必須和 claims 完全一致
- MVP 不做 wildcard

#### Allowed Actions

- `allowed_actions` 是字串陣列
- 只有精確匹配
- MVP 不做層級權限與 pattern matching

#### Resource Scope

- `resource_scope` 是 key-value 物件
- verify 時提供的 `resource` 必須包含相同值
- MVP 只做平面欄位比對

#### Spending Limit

- `amount_usd` 若未提供，則跳過金額檢查
- 若 claim 裡有 `spending_limit_usd` 且 request 帶了 `amount_usd`，則必須 `amount_usd <= spending_limit_usd`
- 這是單次操作上限，不是累積花費控管

---

## 六、技術架構

### 設計原則

- 用最少元件完成驗證
- 用標準加密函式庫，不自己寫密碼學
- 優先做可執行授權，不追求完整 DID/VC 標準覆蓋
- 把複雜 policy engine 延後

### 推薦技術棧

| 層級 | 選擇 | 理由 |
|---|---|---|
| API | FastAPI | 文件完整、開發快、OpenAPI 自動生成 |
| SDK | Python 3.9+ | 目標客群導入成本最低 |
| DB | Supabase PostgreSQL | 託管、足夠應付 MVP |
| Auth | Clerk | 不自己做使用者登入 |
| 部署 | Railway | 快速部署 |
| 錯誤監控 | Sentry | 上線第一天就需要 |
| 分析 | PostHog | 看 onboarding 與驗證用量 |
| Crypto | PyNaCl + PyJWT | 成熟、簡單 |

### 系統架構

```text
Client SDK / Direct REST
        |
        v
  TrustMesh API (FastAPI)
        |
        +-- Agent Service
        +-- Credential Issuer
        +-- Verification Engine
        +-- Audit Log Service
        |
        v
  Supabase PostgreSQL
```

---

## 七、資料庫 Schema

### users

```sql
CREATE TABLE users (
    id UUID PRIMARY KEY,
    clerk_user_id TEXT UNIQUE NOT NULL,
    email TEXT NOT NULL,
    created_at TIMESTAMPTZ DEFAULT NOW()
);
```

### api_keys

```sql
CREATE TABLE api_keys (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES users(id),
    key_prefix TEXT NOT NULL,
    key_hash TEXT NOT NULL,
    name TEXT,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    last_used_at TIMESTAMPTZ,
    revoked_at TIMESTAMPTZ
);
```

### agents

```sql
CREATE TABLE agents (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES users(id),
    did TEXT UNIQUE NOT NULL,
    name TEXT NOT NULL,
    operator TEXT,
    public_key BYTEA NOT NULL,
    private_key_encrypted BYTEA,
    metadata JSONB DEFAULT '{}',
    created_at TIMESTAMPTZ DEFAULT NOW(),
    revoked_at TIMESTAMPTZ
);
```

### credentials

```sql
CREATE TABLE credentials (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    issuer_did TEXT NOT NULL,
    subject_did TEXT NOT NULL,
    claims JSONB NOT NULL,
    jwt TEXT NOT NULL,
    issued_at TIMESTAMPTZ DEFAULT NOW(),
    expires_at TIMESTAMPTZ,
    revoked_at TIMESTAMPTZ
);
```

### verification_logs

```sql
CREATE TABLE verification_logs (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    credential_id UUID REFERENCES credentials(id),
    agent_did TEXT,
    audience TEXT,
    action TEXT,
    resource JSONB,
    amount_usd NUMERIC(10,2),
    result TEXT NOT NULL,
    reason TEXT,
    verified_at TIMESTAMPTZ DEFAULT NOW(),
    verifier_ip TEXT,
    user_agent TEXT
);
```

### 索引

```sql
CREATE INDEX idx_agents_did ON agents(did);
CREATE INDEX idx_credentials_subject ON credentials(subject_did);
CREATE INDEX idx_credentials_issuer ON credentials(issuer_did);
CREATE INDEX idx_verification_logs_time ON verification_logs(verified_at DESC);
```

### 私鑰策略

MVP 先採用託管式私鑰：

- 私鑰加密後存資料庫
- README 與 docs 說明這是 MVP 權衡
- 後續版本再支援 self-custody / BYOK

---

## 八、30 天執行時程

### Week 1：技術可行性 + API 骨架

- 建 FastAPI 專案
- 建 DB schema
- 完成 agent create / get
- 完成 Ed25519 keypair、JWT sign、JWT verify spike
- production 首次部署

### Week 2：Credential 與驗證引擎

- 完成 credential issue
- 完成 credential revoke
- 完成 verify API
- 完成 policy checks：audience、action、resource、amount
- 寫基本 pytest

### Week 3：SDK + docs + demo

- 完成 Python SDK
- docs 網站上線
- 寫 Quickstart
- 寫 B2B procurement demo
- 加入 audit logs 查詢

### Week 4：Landing + beta + 用戶驗證

- trustmesh.dev 上線
- 找 5 家 target customer 試用
- 跑 1 對 1 訪談
- 修 onboarding 與錯誤訊息
- 發佈 beta

---

## 九、驗收標準

### 必過測試情境

1. 建立 agent 成功
2. issue credential 成功
3. verify 合法 request 成功
4. 過期 credential 被拒
5. revoked credential 被拒
6. audience 不符被拒
7. action 不在清單被拒
8. resource 不符被拒
9. amount 超過 `spending_limit_usd` 被拒
10. 每次驗證都留下 audit log

### Demo 成功標準

對外 demo 必須能完整展示：

- 一個 agent 被註冊
- 一張 capability credential 被簽發
- 一次合法的 API 操作被允許
- 一次越權操作被拒絕
- dashboard 或查詢 API 能看到 audit trail

---

## 十、競爭定位

### 我們不是什麼

- 不是 Langfuse / AgentOps 那種 observability 工具
- 不是 Portkey / Helicone / LiteLLM 那種 gateway
- 不是 generic DID 平台
- 不是 token 成本監控工具

### 我們是什麼

**TrustMesh 是讓 B2B API 能安全接受 AI agents 的授權層。**

它解決的是：

- 誰在呼叫我？
- 它被授權做什麼？
- 這次動作有沒有越權？
- 如果有問題，我能不能撤銷並留下稽核紀錄？

### 一句話對外 Pitch

**Let AI agents call your API with verifiable authorization, not just an API key.**

